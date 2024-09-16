import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize


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
        z = c - a / b * np.sqrt(b**2 + x**2 + y**2)
        # offset to match Zemax, so z=0 at x=y=0
        z -= c - a
        return z

    return _hyperbolic


def minim_func(params, x, y, z):
    a, c = params
    model = grasp_hyperbolic(a, c)
    return np.sum((model(x, y) - z) ** 2)


def main():

    radius = -1556.044 * 1e-3
    conic = -5.73622
    a = 557.7059244 * 1e-3
    c = 1335.72816 * 1e-3

    # Hyperbolic surface
    zmx_hyperbolic_surface = zmx_hyperbolic(radius, conic)

    # Test
    x = np.linspace(-2, 2, 100)
    y = np.linspace(-2, 2, 100)
    X, Y = np.meshgrid(x, y)
    Z1 = zmx_hyperbolic_surface(X, Y)

    # Fit parameters of grasp_hyperbolic_surface to match Z1
    params = np.array([a, c])
    minim_func(params, X, Y, Z1)
    result = minimize(
        minim_func,
        params,
        args=(X, Y, Z1),
        method="Nelder-Mead",
        tol=1e-14,
    )
    a_fit, c_fit = result.x
    print(f"Initial: a={a}, c={c}")
    print(f"Fit: a={a_fit}, c={c_fit}")

    Z2 = grasp_hyperbolic(a_fit, c_fit)(X, Y)

    # Surface plots
    fig, ax = plt.subplots(
        1, 2, figsize=(10, 5), subplot_kw={"projection": "3d"}
    )
    ax[0].plot_surface(X, Y, Z1)
    ax[0].set_title("Zemax")
    ax[1].plot_surface(X, Y, Z2)
    ax[1].set_title("Grasp")

    # plot the difference
    fig, ax = plt.subplots(1, 1, figsize=(5, 5))
    ax.contourf(X, Y, Z1 - Z2)
    ax.set_title("Difference")
    fig.colorbar(ax.contourf(X, Y, Z1 - Z2))


if __name__ == "__main__":
    main()
    plt.show()
