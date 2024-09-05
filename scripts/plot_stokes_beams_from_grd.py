import matplotlib.pyplot as plt
import numpy as np
from souk import DATADIR, ASSETDIR
from graspy.data.grid import read_grd_file
from graspy.plot import plot_grd_data, plot_slice
import seaborn as sns

sns.set_style("whitegrid")

DIR = DATADIR / "external" / "grasp"
NORM = True
XRANGE = 2

SAVEFIGDIR = ASSETDIR / "figures" / "grasp"
SAVEFIGDIR.mkdir(exist_ok=True, parents=True)


if __name__ == "__main__":
    files = ("f150_y0.grd", "f150_y180.grd")
    name = files[0].split("_")[0]
    for f in files:
        souk_file = DIR / "beams" / f
        souk_data = read_grd_file(souk_file)

        # get I Q U beams
        souk_data["I"] = (
            souk_data["co"].values * souk_data["co"].values.conj()
            + souk_data["cx"].values * souk_data["cx"].values.conj()
        )
        souk_data["Q"] = (
            souk_data["co"].values * souk_data["co"].values.conj()
            - souk_data["cx"].values * souk_data["cx"].values.conj()
        )
        souk_data["U"] = 2 * np.real(
            souk_data["co"].values * souk_data["cx"].values.conj()
        )

        # normalize
        max_I = np.max(souk_data["I"].values)
        souk_data["I"] = souk_data["I"].values / max_I
        souk_data["Q"] = souk_data["Q"].values / max_I
        souk_data["U"] = souk_data["U"].values / max_I

        # plot IQU beams
        fig, ax = plt.subplots(1, 3, figsize=(15, 5))
        for i, pol in enumerate(["I", "Q", "U"]):
            ax[i].tricontourf(
                souk_data["x"].values,
                souk_data["y"].values,
                20 * np.log10(np.abs(souk_data[pol].values)),
            )
            ax[i].set_title(pol)
            ax[i].set_aspect("equal")

        # add colorbar for all plots
        fig.colorbar(ax[0].collections[0], ax=ax, location="right", shrink=0.5)

        # plot diagonal slice
        # rotate x y by 45 degrees
        x = souk_data["x"].values
        y = souk_data["y"].values
        x_rot = x * np.cos(np.pi / 4) - y * np.sin(np.pi / 4)
        y_rot = x * np.sin(np.pi / 4) + y * np.cos(np.pi / 4)
        souk_data["x_rot"] = x_rot
        souk_data["y_rot"] = y_rot

        # find peak of I beam
        I = souk_data["I"].values
        peak_idx = np.argmax(I)
        peak_x = souk_data["x_rot"].values[peak_idx]
        peak_y = souk_data["y_rot"].values[peak_idx]
        slice_ = souk_data[np.isclose(souk_data["y_rot"].values, peak_y)]

        # plot diagonal slice
        fig, ax = plt.subplots(1, 3, figsize=(15, 5))
        for i, pol in enumerate(["I", "Q", "U"]):
            ax[i].plot(
                slice_["x_rot"].values,
                20 * np.log10(np.abs(slice_[pol].values)),
            )
            ax[i].set_title(pol)
            ax[i].set_xlabel("Diagonal (deg)")
            ax[i].set_ylabel("Intensity (dB)")
            ax[i].set_ylim(-100, 0)
            ax[i].set_xlim(-2 + peak_x, 2 + peak_x)

        fig.tight_layout()

    plt.show()
