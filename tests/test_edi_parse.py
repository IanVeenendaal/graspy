from pathlib import Path
from graspy.edi import parse_edi_beamwidths, parse_edi_crosspol

dir = Path(__file__).parent.parent / "tests"
file = "test.edi"
filename = dir / file


bw_df = parse_edi_beamwidths(filename)
print(bw_df)

crosspol_df = parse_edi_crosspol(filename)
print(crosspol_df)
