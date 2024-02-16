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
    even_asphere: Optional[list[float]]

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
class Lens:
    name: str
    surface: list[Surface]
    aperture: float

    def __post_init__(self):
        if len(self.surface) != 2:
            raise ValueError("Lens must have exactly 2 surfaces")


def asphere_to_rsf(lens: Lens, wavelength: float):
    spacing = wavelength / 10
    n = int(lens.aperture / spacing) + 1

    # Generate the asphere
    x = np.linspace(0, lens.aperture, n)

    for i, s in enumerate(lens.surface):
        y = s.tabulate(x)
        if i % 2 == 1:
            y *= -1  # Invert back surface sag tables

        # save x and y to file as rho and z
        save_file = f"L{lens.name}-S{i+1}.rsf"
        with open(save_file, "w+") as f:
            f.write(f"Lens: {lens.name}, Surface: {i+1}\n")
            f.write(f"{len(x)}\t1\t0\n")
            for i in range(len(x)):
                f.write(f"{x[i]*1e-3}\t{y[i]*1e-3}\n")
