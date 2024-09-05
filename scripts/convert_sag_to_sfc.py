from graspy.helpers.surface import Surface, BiconicSurface, surface_to_sfc
import numpy as np


def lb_f2p2():
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


def lb_mcd_biconic():
    r1x = 4.083856047979213e003
    k1x = -9.607372527061693e-001
    r1y = 4.866544322532473e003
    k1y = 2.405459138204333e000
    primary_mirror = BiconicSurface([r1x, r1y], [k1x, k1y])
    semidia = 1000
    x = np.linspace(-semidia, semidia, 100)
    y = np.linspace(-semidia, semidia, 100)
    surface_to_sfc(primary_mirror, x, y, "mcd_biconic_m1", biconic=True)

    r2x = -2.816392848316889e003
    k2x = -4.941380606171586e000
    r2y = -2.964279718181585e003
    k2y = -8.720916308527041e-001
    secondary_mirror = BiconicSurface([r2x, r2y], [k2x, k2y])
    semidia = 1000
    x = np.linspace(-semidia, semidia, 100)
    y = np.linspace(-semidia, semidia, 100)
    surface_to_sfc(secondary_mirror, x, y, "mcd_biconic_m2", biconic=True)


def main():
    lb_mcd_biconic()


if __name__ == "__main__":
    main()
