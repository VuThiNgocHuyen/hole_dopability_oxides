from dataclasses import dataclass
from typing import Dict

from monty.json import MSONable
from vise.util.mix_in import ToJsonFileMixIn


@dataclass
class Condition:
    is_higher: bool
    element: str
    orbital: str
    criterion: float

    def satisfy_condition(self, band_edge_info: "VBMInfo"):
        target_val = band_edge_info.orbitals[self.element][self.orbital]
        if self.is_higher:
            return target_val > self.criterion
        else:
            return target_val < self.criterion



@dataclass
class VBMInfo(MSONable, ToJsonFileMixIn):
    formula: str
    band_idx: int
    kpt_idx: int
    orbitals: Dict[str, Dict[str, float]]



