from pathlib import Path
from dataclasses import dataclass
import pandas as pd
import numpy as np
from souk import DATADIR
import matplotlib.pyplot as plt

DIR = DATADIR / "external" / "beam"


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


def load_grasp(filename):
    with open(filename, "r") as f:
        name = f.readline().strip()
        params = f.readline().strip().split()
        params = [float(p) for p in params]

        angles = np.arange(
            params[0],
            params[2] * params[1] + params[0],
            params[1],
        )

        data = f.readlines()[0 : len(angles)]
        data = [list(map(float, line.split())) for line in data]

        df = pd.DataFrame(
            data, columns=["Re(E_co)", "Im(E_co)", "Re(E_cx)", "Im(E_cx)"]
        )

    df["angle"] = angles
    df["E_co"] = np.abs(df["Re(E_co)"] + 1j * df["Im(E_co)"])
    return df


def main():
    comsol = load_comsol(DIR / "20240207_comsol_150ghz.txt")
    grasp = load_grasp(DIR / "20240207_grasp_150ghz.txt")

    plt.figure()
    plt.plot(comsol["angle"], comsol["Far-field norm 2"], label="COMSOL")
    plt.plot(grasp["angle"], grasp["E_co"], label="GRASP")
    plt.xlabel("Angle (deg)")
    plt.ylabel("E_co (V/m)")
    plt.xlim(-3, 3)
    plt.title("150 GHz")
    plt.legend()

    plt.figure("Power")
    cp = comsol["Far-field norm"] ** 2
    gp = grasp["E_co"] ** 2
    cp_db = 10 * np.log10(cp / cp.max())
    gp_db = 10 * np.log10(gp / gp.max())
    plt.plot(comsol["angle"] * 60, cp_db, label="COMSOL")
    plt.plot(grasp["angle"] * 60, gp_db, label="GRASP")
    plt.xlabel("Angle (arcmin)")
    plt.ylabel("Intensity (dB)")
    plt.xlim(0, 180)
    plt.title("150 GHz")
    plt.legend()


if __name__ == "__main__":
    main()
    plt.show()
