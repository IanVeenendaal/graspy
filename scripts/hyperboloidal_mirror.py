import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# R = 2862.889 * 1e-3
# K = -4.274316085000

R = 1556.044471 * 1e-3
K = -5.736218


def zemax_sag(r, c, k):
    return c * r**2 / (1 + np.sqrt(1 - (1 + k) * c**2 * r**2))


def grasp_hyperboloidal_mirror(x, a, b):
    c = np.sqrt(b**2 + a**2)
    return c - a / b * np.sqrt(b**2 + x**2) - (c - a)


def main():
    # Define x and y coordinates
    x = np.linspace(-1, 1, 101)
    y = np.linspace(-1, 1, 101)
    # x, y = np.meshgrid(x, y)
    # r = np.sqrt(x**2 + y**2)
    r = x

    # Calculate sag
    z = zemax_sag(r, 1 / R, K)

    # fit with grasp hyperboloidal mirror
    popt, pcov = curve_fit(grasp_hyperboloidal_mirror, x, z, p0=[1, 1])

    a, b = popt

    e = np.sqrt(-K)
    c = e * a
    print(a, b, c)
    print(np.sqrt(c**2 - a**2))

    plt.figure()
    plt.plot(x, z)
    plt.plot(x, grasp_hyperboloidal_mirror(x, *popt))


if __name__ == "__main__":
    main()
    plt.show()
