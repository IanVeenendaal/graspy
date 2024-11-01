import matplotlib.pyplot as plt
from souk import DATADIR, ASSETDIR
from graspy.data.grid import read_grd_file
from graspy.plot import plot_grd_data, plot_slice
import seaborn as sns
import numpy as np

sns.set_style("whitegrid")

DIR = DATADIR / "external" / "horn"
NORM = True
XRANGE = 90

SAVEFIGDIR = ASSETDIR / "figures" / "grasp"
SAVEFIGDIR.mkdir(exist_ok=True, parents=True)

FILE = DIR / "test_horn_150ghz.grd"


def main():
    name = FILE.name
    data = read_grd_file(FILE)
    plot_grd_data(data, norm=NORM, name=name)

    data["Intensity"] = np.abs(data["co"]) ** 2 + np.abs(data["cx"]) ** 2
    max_int = np.max(data["Intensity"])
    data["Intensity_db"] = 10 * np.log10(data["Intensity"] / max_int)

    plt.figure("Combined Co and Cx Pol")
    plt.tricontourf(
        data["x"].values,
        data["y"].values,
        data["Intensity_db"].values,
    )
    plt.colorbar()

    xrange = XRANGE
    for direction in ["x", "y", "diagonal"]:
        save_fig_file = SAVEFIGDIR / f"{name}_{direction}_{xrange}deg.png"
        # for pol in ["co", "cx", "intensity"]:
        for pol in ["intensity"]:
            plot_slice(
                data,
                norm=True,
                direction=direction,
                name=name,
                pol=pol,
                xrange=xrange,
                fignum=f"{name}_{xrange}deg",
            )

            # Save figure
            plt.savefig(save_fig_file, dpi=300)


if __name__ == "__main__":
    main()
    plt.show()
