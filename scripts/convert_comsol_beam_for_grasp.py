from pathlib import Path
from dataclasses import dataclass
import pandas as pd
import numpy as np
from souk import DATADIR


@dataclass
class CutParams:
    description: str
    filename: Path
    v_ini: float
    v_inc: float
    v_num: int
    c: float
    icomp: int
    icut: int
    ncomp: int


def load_comsol_horn(filename):
    df = pd.read_csv(
        filename,
        skiprows=8,
        delimiter="\s+",
        header=None,
        names=["theta", "Far-field norm"],
    )
    # split where change in theta is negative
    split = np.where(np.diff(df["theta"]) < 0)[0][0] + 1
    new_df = df.iloc[split:]
    new_df["Far-field norm 2"] = df.iloc[:split]["Far-field norm"].values

    new_df["angle"] = np.degrees(new_df["theta"].values) - 90

    return new_df


def convert_comsol_beam_for_grasp(filename: Path, output_file: Path, desc: str):
    df = load_comsol_horn(filename)
    min = -90
    max = 90

    df = df[(df["angle"] >= min) & (df["angle"] <= max)]
    ini = min
    inc = 2
    num = int((max - min) / inc + 1)

    assert len(df["angle"]) == num

    params = CutParams(
        description=desc,
        filename=output_file,
        v_ini=ini,
        v_inc=inc,
        v_num=num,
        c=0,  # constant value for phi angle
        icomp=3,  # Defines F1 and F2 polarized field components. 3: Linear E_co and E_cx (Ludwig's third definition)
        icut=1,  # 1: standard polar cut where phi is fixed and theta is varied
        ncomp=2,  # Number of field components
    )

    with open(output_file, "w+") as f:
        f.write(params.description + "\n")
        f.write(
            f" {params.v_ini:1.10E}  {params.v_inc:1.10E}  {params.v_num:d}  {params.c:1.10E}    {params.icomp:d}    {params.icut:d}    {params.ncomp:d}\n"
        )
        for i in range(len(df["angle"])):
            # 4 columns: E_co_real, E_co_imag, E_cx_real, E_cx_imag
            # Use exponential notation
            f.write(
                f" {df['Far-field norm'].iloc[i]: 1.10E}\t0.0000000000E+00\t0.0000000000E+00\t0.0000000000E+00\n"
            )
        f.write(params.description + "\n")
        f.write(
            f" {params.v_ini:1.10E}  {params.v_inc:1.10E}  {params.v_num:d}  {params.c + 90:1.10E}    {params.icomp:d}    {params.icut:d}    {params.ncomp:d}\n"
        )
        for i in range(len(df["angle"])):
            # 4 columns: E_co_real, E_co_imag, E_cx_real, E_cx_imag
            f.write(
                f" {df['Far-field norm'].iloc[i]: 1.10E}\t0.0000000000E+00\t0.0000000000E+00\t0.0000000000E+00\n"
            )
    return


if __name__ == "__main__":
    file = DATADIR / "external" / "horn" / "test.txt"
    output_file = DATADIR / "external" / "horn" / "test.cut"
    convert_comsol_beam_for_grasp(file, output_file, "150 GHz MF Horn")
    print(f"File {output_file} created")
