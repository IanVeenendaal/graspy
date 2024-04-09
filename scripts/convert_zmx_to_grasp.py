import numpy as np
import matplotlib.pyplot as plt


def zmx_hyperbolic(radius, conic):
    """Creates callable function for hyperbolic surface"""

    def _hyperbolic(x, y):
        curvature = 1 / radius
        r = np.sqrt(x**2 + y**2)
        return (
            curvature
            * r**2
            / (1 + np.sqrt(1 - (1 + conic) * curvature**2 * r**2))
        )

    return _hyperbolic


def grasp_hyperbolic(a, c):
    """Creates callable function for hyperbolic surface"""

    def _hyperbolic(x, y):
        b = np.sqrt(c**2 - a**2)
        return c - a / b * np.sqrt(b**2 + x**2 + y**2)

    return _hyperbolic


def main():

    radius = -1556.044 * 1e-3
    conic = -5.73622
    a = 557.7059244 * 1e-3
    c = 1335.72816 * 1e-3

    # Hyperbolic surface
    zmx_hyperbolic_surface = zmx_hyperbolic(radius, conic)
    grasp_hyperbolic_surface = grasp_hyperbolic(a, c)

    # Test
    x = np.linspace(-2, 2, 100)
    y = np.linspace(-2, 2, 100)
    X, Y = np.meshgrid(x, y)
    Z1 = zmx_hyperbolic_surface(X, Y)
    Z2 = grasp_hyperbolic_surface(X, Y)

    # Offset Z2 to match Z1
    f = c - a
    Z2 -= f

    # Surface plots
    fig, ax = plt.subplots(
        1, 2, figsize=(10, 5), subplot_kw={"projection": "3d"}
    )
    ax[0].plot_surface(X, Y, Z1)
    ax[0].set_title("Zemax")
    ax[1].plot_surface(X, Y, Z2)
    ax[1].set_title("Grasp")

    if not np.allclose(Z1, Z2, rtol=1e-5, atol=1e-5):
        # plot the difference
        fig, ax = plt.subplots(
            1, 1, figsize=(5, 5), subplot_kw={"projection": "3d"}
        )
        ax.plot_surface(X, Y, Z1 - Z2)
        ax.set_title("Difference")


if __name__ == "__main__":
    main()
    plt.show()
