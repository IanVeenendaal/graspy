# %%  Imports
import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from dataclasses import dataclass

DIR = Path(
    r"C:\Users\Ian Veenendaal\OneDrive - Cardiff University\Projects\SOUK\data\external\horn"
)

# %% Comsol


def load_comsol(filename):
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


# %% CHAMPS 3D
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


@dataclass
class CutData:
    params: CutParams
    data: pd.DataFrame


def load_champs(filename):
    cuts = []
    with open(filename, "r") as f:
        while True:
            description = f.readline()
            if not description:
                break
            line = f.readline().split()
            params = CutParams(
                description,
                filename,
                v_ini=float(line[0]),
                v_inc=float(line[1]),
                v_num=int(line[2]),
                c=float(line[3]),
                icomp=int(line[4]),
                icut=int(line[5]),
                ncomp=int(line[6]),
            )
            columns = ["Re(E_co)", "Im(E_co)", "Re(E_cx)", "Im(E_cx)"]
            # Read table
            table = [
                map(float, f.readline().split()) for _ in range(params.v_num)
            ]
            df = pd.DataFrame(table, columns=columns, dtype=float)
            cut = CutData(params, df)
            cuts.append(cut)
    return cuts


# %% Plotting

fig, ax = plt.subplots(1, 1)
comsol = load_comsol(DIR / "test_comsol.txt")
champs = load_champs(DIR / "test_champs.cut")

field = comsol["Far-field norm"].values
field_db = 20 * np.log10(field / np.max(field))
ax.plot(comsol["angle"], field_db, label="Comsol")
for cut in champs:
    e_field = np.abs(
        cut.data["Re(E_co)"].values + 1j * cut.data["Im(E_co)"].values
    )
    intensity_db = 20 * np.log10(e_field / np.max(e_field))

    # Normalize
    # e_field /= np.max(e_field)
    # e_field = 10 * np.log10(e_field)
    # intensity_db -= np.max(intensity_db)

    ax.plot(
        np.arange(
            cut.params.v_ini,
            cut.params.v_ini + cut.params.v_inc * cut.params.v_num,
            cut.params.v_inc,
        ),
        intensity_db,
        label=f"{cut.params.description} {cut.params.c:.2f} deg",
    )
ax.legend()
ax.set(
    yscale="linear",
    xlabel="Angle (deg)",
    ylabel="Normalized Intensity (dB)",
    xlim=(-90, 90),
    ylim=(-50, 10),
)
plt.show()
