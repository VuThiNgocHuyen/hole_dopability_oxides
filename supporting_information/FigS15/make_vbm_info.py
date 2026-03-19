from collections import defaultdict

from pymatgen.core import PeriodicSite
from pymatgen.electronic_structure.core import Spin
from pymatgen.io.vasp import Procar, Vasprun, Outcar

from huyen_vbm_Oh.vbm_info import VBMInfo

def make_vbm_info(procar: Procar, vasprun: Vasprun, outcar: Outcar):
    try:
        # vbm_data = vasprun.get_band_structure().get_vbm()
        # Validate and retrieve k-point index

        from vise.analyzer.vasp.band_edge_properties import VaspBandEdgeProperties

        bep = VaspBandEdgeProperties(vasprun=vasprun, outcar=outcar)
        vbm_data = bep.vbm_info

        vbm_kpt_index = vbm_data.kpoint_index

        # Handle band index for spin-polarized or non-spin cases
        if isinstance(vbm_data.band_index, dict):
            if Spin.up not in vbm_data.band_index:
                raise ValueError("Spin.up not found in VBM band index data.")
            band_indices = vbm_data.band_index[Spin.up]
            if not band_indices:
                raise ValueError("No band indices found for Spin.up in VBM data.")
            vbm_band_index = max(band_indices)
        else:
            vbm_band_index = vbm_data.band_index
        # Validate and retrieve PROCAR data
        if Spin.up not in procar.data:
            raise ValueError("Spin.up data not found in PROCAR.")
        if vbm_kpt_index >= len(procar.data[Spin.up]):
            raise IndexError("VBM k-point index is out of range for PROCAR data.")
        if vbm_band_index >= len(procar.data[Spin.up][vbm_kpt_index]):
            raise IndexError("VBM band index is out of range for PROCAR data.")
        vbm_projections = procar.data[Spin.up][vbm_kpt_index][vbm_band_index]

        # Process projections
        total_projection = defaultdict(lambda: defaultdict(float))
        structure = vasprun.structures[0]

        for elem, atom_projection in zip(structure, vbm_projections):
            if len(atom_projection) < 9:
                raise ValueError(f"Unexpected atom projection length: {len(atom_projection)}")
            elem_name = elem.species_string
            total_projection[elem_name]["s"] += atom_projection[0]
            total_projection[elem_name]["p"] += (atom_projection[1:4]).sum()
            total_projection[elem_name]["d"] += (atom_projection[4:9]).sum()

        orbitals = {k: dict(v) for k, v in total_projection.items()}

        return VBMInfo(formula=vasprun.structures[0].reduced_formula,
                       band_idx=vbm_band_index,
                       kpt_idx=vbm_kpt_index,
                       orbitals=orbitals)

    except Exception as e:
        raise ValueError(f"Error in make_vbm_info for formula {vasprun.structures[0].reduced_formula}: {e}")
