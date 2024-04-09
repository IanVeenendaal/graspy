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

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from souk import DATADIR

DIR = DATADIR / "external" / "grasp"
NORM = True


# Function to read GRD file
def read_grd_file(file_path):
    with open(file_path, "r") as file:
        # Read title
        version = file.readline().strip().split(":")[-1].strip()
        name = file.readline().strip()
        source_field_name = file.readline().strip().split(":")[-1].strip()
        frequency_range_name = file.readline().strip().split(":")[-1].strip()
        assert file.readline().strip() == "FREQUENCIES [GHz]:"
        frequency = float(file.readline().strip())
        assert file.readline().strip() == "++++"

        # Read grid data
        data = []
        ktype = int(file.readline().strip())
        nset, icomp, ncomp, igrid = [int(x) for x in file.readline().split()]
        for i in range(nset):
            # center of the grid
            ix, iy = [int(x) for x in file.readline().split()]
            assert ix == 0 and iy == 0
            # grid limits
            xs, ys, xe, ye = [float(x) for x in file.readline().split()]
            nx, ny, klimit = [int(x) for x in file.readline().split()]

            for j in range(ny):
                if klimit == 1:
                    i_s, i_n = [int(x) for x in file.readline().split()]
                else:
                    i_s, i_n = 0, nx
                y = ys + (j) * (ye - ys) / (ny - 1)
                for k in range(i_n):
                    x = xs + (i_s + k) * (xe - xs) / (nx - 1)
                    line = [float(s) for s in file.readline().split()]
                    co = line[0] + 1j * line[1]
                    cx = line[2] + 1j * line[3]
                    data.append([x, y, co, cx])

        # convert to pandas dataframe
        df = pd.DataFrame(data, columns=["x", "y", "co", "cx"])
        return df


# Function to plot data
def plot_grd_data(data, norm=False, name=""):

    co_abs = np.abs(data["co"].values)
    cx_abs = np.abs(data["cx"].values)

    # normalize from max co
    if norm:
        max_co = np.max(co_abs)
        co_abs /= max_co
        cx_abs /= max_co

    co_db = 20 * np.log10(co_abs)
    cx_db = 20 * np.log10(cx_abs)
    plt.figure(figsize=(10, 5), num=name)
    plt.subplot(1, 2, 1, aspect="equal")
    plt.title("CoPol")
    plt.tricontourf(
        data["x"].values,
        data["y"].values,
        co_db,
    )
    plt.colorbar()

    plt.subplot(1, 2, 2, aspect="equal")
    plt.title("CxPol")
    plt.tricontourf(
        data["x"].values,
        data["y"].values,
        cx_db,
    )
    plt.colorbar()


def plot_slice(data, norm=False, direction="x", name=""):
    data["co_abs"] = np.abs(data["co"])
    data["cx_abs"] = np.abs(data["cx"])

    if norm:
        co_max = np.max(data["co_abs"])
        data["co_abs"] /= co_max
        data["cx_abs"] /= co_max

    data["co_db"] = 20 * np.log10(data["co_abs"])
    data["cx_db"] = 20 * np.log10(data["cx_abs"])

    # Find peak of co-pol
    peak = np.argmax(data["co_db"].values)
    peak_x = data["x"].values[peak]
    peak_y = data["y"].values[peak]
    print(f"Peak at {peak_x}, {peak_y}")

    # Plot slice at peak
    plt.figure(figsize=(5, 5), num="Slice")
    if direction == "x":
        slice_ = data.iloc[peak_y == data["y"].values]
        plt.plot(slice_["x"].values, slice_["co_db"].values, label=name)
    elif direction == "y":
        slice_ = data.iloc[peak_x == data["x"].values]
        plt.plot(slice_["y"].values, slice_["co_db"].values, label=name)
    else:
        raise ValueError("Direction must be 'x' or 'y'")


if __name__ == "__main__":
    sonom_file = DIR / "so_nom_145ghz_wide.grd"
    souk_file = DIR / "so_uk_150ghz_wide.grd"
    sonom_data = read_grd_file(sonom_file)
    plot_grd_data(sonom_data, norm=NORM, name="SO Nominal Edge Pixel 150 GHz")
    souk_data = read_grd_file(souk_file)
    plot_grd_data(souk_data, norm=NORM, name="SO UK Edge Pixel 150 GHz")

    # Plot slice
    plot_slice(
        sonom_data,
        norm=True,
        direction="y",
        name="SO Nominal Edge Pixel 150 GHz",
    )
    plot_slice(
        souk_data, norm=True, direction="y", name="SO UK Edge Pixel 150 GHz"
    )
    plt.legend()
    plt.show()
