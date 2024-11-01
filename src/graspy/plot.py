import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import griddata


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


def plot_slice(
    data,
    norm=False,
    direction="x",
    name="",
    pol="co",
    xrange="full",
    fignum=None,
):
    data["co_abs"] = np.abs(data["co"])
    data["cx_abs"] = np.abs(data["cx"])

    if norm:
        co_max = np.max(data["co_abs"])
        data["co_abs"] /= co_max
        data["cx_abs"] /= co_max

    data["co_db"] = 20 * np.log10(data["co_abs"])
    data["cx_db"] = 20 * np.log10(data["cx_abs"])

    data["Intensity"] = data["co_abs"] ** 2 + data["cx_abs"] ** 2
    data["Intensity_db"] = 10 * np.log10(data["Intensity"])

    # Find peak of co-pol
    peak = np.argmax(data["co_db"].values)
    peak_x = data["x"].values[peak]
    peak_y = data["y"].values[peak]
    print(f"Peak at {peak_x}, {peak_y}")

    # Plot slice at peak
    plt.figure(figsize=(5, 5), num="Slice")
    if direction == "x":
        slice_ = data.iloc[peak_y == data["y"].values]
        x_axis = "x"
        peak_loc = peak_x
    elif direction == "y":
        slice_ = data.iloc[peak_x == data["x"].values]
        x_axis = "y"
        peak_loc = peak_y
    elif direction == "diagonal":
        xp = np.linspace(-1, 1, 10001)
        yp = np.linspace(-1, 1, 10001)

        scale = (data["x"].max() - data["x"].min()) / 2
        xp *= scale
        yp *= scale

        x_axis = np.sqrt(xp**2 + yp**2) * np.sign(xp - peak_x)
        peak_loc = 0

        xp += peak_x
        yp += peak_y

        if pol == "co":
            interp2d = griddata(
                (data["x"].values, data["y"].values),
                data["co_db"].values,
                xi=(xp, yp),
                method="linear",
            )
        elif pol == "cx":
            interp2d = griddata(
                (data["x"].values, data["y"].values),
                data["cx_db"].values,
                xi=(xp, yp),
                method="linear",
            )
        elif pol == "intensity":
            interp2d = griddata(
                (data["x"].values, data["y"].values),
                data["Intensity"].values,
                xi=(xp, yp),
                method="linear",
            )
        else:
            raise ValueError("Polarization must be 'co' or 'cx'")
        plt.figure(fignum)
        plt.plot(x_axis, interp2d, label=f"{name}-{pol}-{direction}")

    else:
        raise ValueError("Direction must be 'x' or 'y'")

    if pol == "co":
        y_axis = "co_db"
    elif pol == "cx":
        y_axis = "cx_db"
    elif pol == "intensity":
        y_axis = "Intensity_db"
    else:
        raise ValueError("Polarization must be 'co' or 'cx'")

    if direction != "diagonal":
        plt.figure(fignum)
        plt.plot(
            slice_[x_axis].values,
            slice_[y_axis].values,
            label=f"{name}-{pol}-{direction}",
        )

    if xrange != "full":
        plt.xlim([peak_loc - xrange, peak_loc + xrange])
