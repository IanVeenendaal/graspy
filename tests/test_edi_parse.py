from pathlib import Path
from graspy.edi import (
    parse_edi_beamwidths,
    parse_edi_crosspol,
    parse_edi_efficiency,
    parse_edi_phase_centers,
)
import numpy as np

dir = Path(__file__).parent.parent / "tests"
file = "test.edi"
filename = dir / file


bw_df = parse_edi_beamwidths(filename)
print(bw_df)

crosspol_df = parse_edi_crosspol(filename)
print(crosspol_df)

pc_df = parse_edi_phase_centers(filename)
print(pc_df)

print(np.sum([float(f) ** 2 for f in pc_df["-3.0 dB Phase Center"].values]))

eff_df = parse_edi_efficiency(filename)
print(eff_df)
