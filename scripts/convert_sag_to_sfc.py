from graspy.helpers.surface import Surface, surface_to_sfc
import numpy as np


def main():
    primary_mirror = Surface(2251.277008, -1.0)
    semidia = 1000
    x = np.linspace(-semidia, semidia, 100)
    y = np.linspace(-semidia, semidia, 100)
    surface_to_sfc(primary_mirror, x, y, "f2p2_m1")

    secondary_mirror = Surface(-1556.0444710621, -5.736218)
    semidia = 1000
    x = np.linspace(-semidia, semidia, 100)
    y = np.linspace(-semidia, semidia, 100)
    surface_to_sfc(secondary_mirror, x, y, "f2p2_m2")


if __name__ == "__main__":
    main()
