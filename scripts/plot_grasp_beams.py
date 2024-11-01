"""
Plot data from a GRASP .grd file

Data is of format:
VERSION: TICRA-EM-FIELD-V0.1
Field data in grid
SOURCE_FIELD_NAME: po_aperture_in_screen
FREQUENCY_RANGE_NAME: frequency_range
FREQUENCIES [GHz]:
  0.1450000000E+03
++++
 1
           1           3           2           4
           0           0
 -0.2000000000E+02 -0.2500000000E+01 -0.1500000000E+02  0.2500000000E+01
         101         101           1
          51           1
  0.1817489167E-01  0.8116596614E+01  0.6384502793E+00  0.1952216186E+01
          42          19
  0.2778726958E+01 -0.2040362962E+01 -0.4384717320E-01 -0.3362171024E+00
  0.1066929435E+01  0.9461805190E-01  0.1582468239E+00 -0.2224679630E+00
  ...
          37          29
  0.2849406322E+01 -0.4560159498E+01  0.3222188231E+00 -0.2710026995E+00
  0.3675201883E+01 -0.5481211360E+01  0.1275904571E+00 -0.2718529333E+00
  ...
"""

import matplotlib.pyplot as plt
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
    # sonom_file = DIR / "so_nom_145ghz_wide.grd"
    # sonom_data = read_grd_file(sonom_file)
    # plot_grd_data(sonom_data, norm=NORM, name="SO Nominal Edge Pixel 150 GHz")

    # # Plot slice
    # plot_slice(
    #     sonom_data,
    #     norm=True,
    #     direction="y",
    #     name="SO Nominal Edge Pixel 150 GHz",
    # )

    files = ("f150_y0.grd", "f150_y180.grd")

    name = "f150"
    for f in files:
        souk_file = DIR / "beams" / f

        souk_data = read_grd_file(souk_file)
        plot_grd_data(souk_data, norm=NORM, name="SO UK Edge Pixel 150 GHz")

        xrange = XRANGE
        for direction in ["x", "y", "diagonal"]:
            save_fig_file = SAVEFIGDIR / f"{name}_{direction}_{xrange}deg.png"
            for pol in ["co", "cx"]:
                plot_slice(
                    souk_data,
                    norm=True,
                    direction=direction,
                    name=souk_file.name,
                    pol=pol,
                    xrange=xrange,
                    fignum=f"{name}_{direction}_{xrange}deg",
                )

                plt.ylim(-100, 0)
                plt.xlabel(f"{direction} (deg)")
                plt.ylabel("Intensity (dB)")
                plt.legend()
                plt.tight_layout()

                # Save figure
                plt.savefig(save_fig_file, dpi=300)

    # Close figure
    # plt.close()
