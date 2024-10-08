import numpy as np
from typing import Optional
from dataclasses import dataclass

# Convert a zemax asphere surface definition into a best fit
# spline interpolation for a body of revolution mesh in GRASP


class LensSchema:
    lens_number = "Lens"
    surface_number = "Surface"
    radius = "Radius"
    conic = "Conic"
    a2 = "2nd Order Term"
    a4 = "4th Order Term"
    a6 = "6th Order Term"


@dataclass
class Surface:
    radius: float
    conic: float
    even_asphere: Optional[list[float]] = None

    def __post_init__(self):
        self.curvature = 1 / self.radius

    def tabulate(self, r: np.ndarray) -> np.ndarray:
        """Generate sag table of surface.

        Args:
            r: The radial coordinate of the asphere.

        Returns:
            Sag table.
        """
        c = self.curvature
        k = self.conic
        sag = c * r**2 / (1 + np.sqrt(1 - (1 + k) * c**2 * r**2))
        if self.even_asphere:
            for i, a in enumerate(self.even_asphere):
                sag += a * r ** (2 * i + 2)
        return sag


@dataclass
class BiconicSurface:
    radius: list[float]
    conic: list[float]
    even_asphere: Optional[list[list[float]]] = None

    def __post_init__(self):
        if len(self.radius) != 2:
            raise ValueError("BiconicSurface must have exactly 2 radii")
        if len(self.conic) != 2:
            raise ValueError("BiconicSurface must have exactly 2 conics")

        self.curvature = [1 / r for r in self.radius]

    def tabulate_xy(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        """Generate sag table of surface.

        Args:
            x: The x coordinate of the surface.
            y: The y coordinate of the surface.

        Returns:
            Sag table.
        """
        cx, cy = self.curvature
        kx, ky = self.conic
        sag = (cx * x**2 + cy * y**2) / (
            1
            + np.sqrt(1 - (1 + kx) * cx**2 * x**2)
            + np.sqrt(1 - (1 + ky) * cy**2 * y**2)
        )
        if self.even_asphere:
            raise NotImplementedError(
                "Even asphere not implemented for biconic surfaces"
            )
        return sag


@dataclass
class Lens:
    name: str
    surface: list[Surface]
    aperture: float
    thickness: float

    def __post_init__(self):
        if len(self.surface) != 2:
            raise ValueError("Lens must have exactly 2 surfaces")


def asphere_to_rsf(lens: Lens, wavelength: float, prefix: Optional[str] = None):
    spacing = wavelength / 10
    n = int(lens.aperture / spacing) + 1

    # Generate the asphere
    x = np.linspace(0, lens.aperture, n)

    for i, s in enumerate(lens.surface):
        y = s.tabulate(x)
        if i % 2 == 1:
            y *= -1  # Invert back surface sag tables

        # save x and y to file as rho and z
        save_file = f"{prefix}L{lens.name}-S{i+1}.rsf"
        with open(save_file, "w+") as f:
            f.write(f"Lens: {lens.name}, Surface: {i+1}\n")
            f.write(f"{len(x)}\t1\t0\n")
            for i in range(len(x)):
                f.write(f"{x[i]}\t{y[i]}\n")


def surface_to_sfc(
    surface: Surface,
    x: np.ndarray,
    y: np.ndarray,
    name: Optional[str] = None,
    biconic=False,
) -> None:
    """Convert a surface to a rectangular grid file for GRASP.

    Args:
        surface: The surface to convert.
        x: The x coordinate of the grid.
        y: The y coordinate of the grid.

    Returns:
        The rectangular grid.
    """
    xx, yy = np.meshgrid(x, y)
    if biconic:
        grid = surface.tabulate_xy(xx, yy)
    else:
        r = np.sqrt(xx**2 + yy**2)
        grid = surface.tabulate(r)

    save_file = f"{name}.sfc"
    with open(save_file, "w") as f:
        f.write(f"Surface: {name}\n")
        f.write(f"{min(x)}\t{min(y)}\t{max(x)}\t{max(y)}\n")
        f.write(f"{len(x)}\t{len(y)}\n")
        for i in range(len(x)):
            line = ""
            for j in range(len(y)):
                line += f"{grid[i,j]}\t"
            f.write(line + "\n")
