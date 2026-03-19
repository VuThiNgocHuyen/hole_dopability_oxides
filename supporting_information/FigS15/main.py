from pathlib import Path
import pandas as pd
from pymatgen.io.vasp import Vasprun, Procar, Outcar
from tqdm import tqdm
from huyen_vbm_Oh.make_vbm_info import make_vbm_info
from vbm_info import VBMInfo, Condition

#decoder = MontyDecoder()

#condition = Condition(is_higher=True, element="O", orbital="p", criterion=0.3)
# Setup
# since we use sshfs .........umount | grep ato.........umount ato
# sshfs ato:/storage/huyen/Pacman_oxides_ddhybrid ./ato
dirpath = Path("/Users/vuhuyen/ato")
output_folder = Path("vbm_info")
output_folder.mkdir(exist_ok=True)

def main():
    df_input = pd.read_csv("Data_formula_list_1st.csv", header=0)
    formulas_list = df_input["formula"].tolist()

    not_found = []

    for formula in tqdm(formulas_list):
        print(formula)

        # Construct path to DOS directory
        formula_dir = dirpath / f"{formula}_Oh" / "unitcell" / "dos"
        vasprun_path = formula_dir / "vasprun-finish.xml"
        procar_path = formula_dir / "PROCAR"
        outcar_path = formula_dir / "OUTCAR-finish"

        if not vasprun_path.exists() or not procar_path.exists():
            print(f"Missing files for {formula}")
            continue

        try:
            vasprun = Vasprun(vasprun_path)
            procar = Procar(procar_path)
            outcar = Outcar(outcar_path)
            vbm_info = make_vbm_info(procar=procar, vasprun=vasprun, outcar=outcar)
            output_path = output_folder / f"{formula}.json"
            vbm_info.to_json_file(output_path)

        except Exception as e:
            print(f"Error processing {formula}: {e}")
            not_found.append(formula)
            continue

    # Save missing entries
    if not_found:
        with open("missing_formulas.txt", "w") as f:
            for formula in not_found:
                f.write(formula + "\n")


if __name__ == "__main__":
    main()