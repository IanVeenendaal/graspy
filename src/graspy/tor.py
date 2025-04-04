from pathlib import Path
from dataclasses import dataclass
from typing import Any


class struct(dict):
    def __init__(self, *args, unit="", **kwargs):
        super().__init__(*args, **kwargs)
        self.unit = unit

        # check unit type
        if not isinstance(self.unit, (str, list, dict, type(None))):
            raise ValueError("unit must be a string, list or dict")

    def __repr__(self):
        if self.unit == "" or self.unit is None:
            return f"struct({', '.join(f'{k}: {v}' for k, v in self.items())})"
        elif isinstance(self.unit, dict):
            struct_data = {}
            for k, v in self.items():
                if k in self.unit:
                    struct_data[k] = f"{v} {self.unit[k]}"
                else:
                    struct_data[k] = f"{v}"
            return f"struct({', '.join(f'{k}: {v}' for k, v in struct_data.items())})"
        elif isinstance(self.unit, list):
            return f"struct({', '.join(f'{k}: {v} {self.unit[i]}' for i, (k, v) in enumerate(self.items()))})"
        elif isinstance(self.unit, str):
            return f"struct({', '.join(f'{k}: {v} {self.unit}' for k, v in self.items())})"
        else:
            raise ValueError("unit must be a string, list or dict")


class sequence(list):
    def __init__(self, *args, unit="", **kwargs):
        super().__init__(*args, **kwargs)
        self.unit = unit

    def __repr__(self):
        if self.unit == "":
            return f"sequence({', '.join(f'{v}' for v in self)})"
        return f"sequence({', '.join(f'{v} {self.unit}' for v in self)})"


class table(list):
    def __init__(self, *args, unit="", **kwargs):
        super().__init__(*args, **kwargs)
        self.unit = unit

    def __repr__(self):
        # TODO: Add string representation for table
        pass


class reference:
    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self):
        return f"ref({self.name})"


@dataclass
class CoordinateSystem:
    name: str
    origin: struct
    x_axis: struct
    y_axis: struct
    z_axis: struct
    reference: reference

    def __repr__(self) -> str:
        out = (
            f"{self.name}  coor_sys",
            f"(",
            f"{'  origin':19}: {self.origin},",
            f"{'  x_axis':19}: {self.x_axis},",
            f"{'  y_axis':19}: {self.y_axis},",
            f"{'  z_axis':19}: {self.z_axis},",
            f"{'  base':19}: {self.reference}",
            f")",
        )
        return "\n".join(out) + "\n"


@dataclass
class PlanarCut:
    coor_sys: reference
    rho_range: struct
    phi_range: struct
    name: str

    def __repr__(self) -> str:
        out = (
            f"{self.name}  planar_cut",
            f"(",
            f"{'  coor_sys':19}: {self.coor_sys},",
            f"{'  rho_range':19}: {self.rho_range},",
            f"{'  phi_range':19}: {self.phi_range}",
            f")",
        )
        return "\n".join(out) + "\n"


@dataclass
class SphericalCut:
    coor_sys: reference
    theta_range: struct
    phi_range: struct
    name: str

    def __repr__(self) -> str:
        out = (
            f"{self.name}  spherical_cut",
            f"(",
            f"{'  coor_sys':19}: {self.coor_sys},",
            f"{'  theta_range':19}: {self.theta_range},",
            f"{'  phi_range':19}: {self.phi_range}",
            f")",
        )
        return "\n".join(out) + "\n"


@dataclass
class Frequency:
    frequency_list: sequence
    name: str

    def __repr__(self) -> str:
        out = (
            f"{self.name}  frequency",
            f"(",
            f"{'  frequency_list':19}: {self.frequency_list}",
            f")",
        )
        return "\n".join(out) + "\n"


@dataclass
class XYGrid:
    name: str
    file_name: str
    xy_unit: str = "m"
    z_unit: str = "m"
    z_factor: float = 1.0
    list: bool = True

    def __repr__(self) -> str:
        list = "on" if self.list else "off"
        out = (
            f"{self.name}  regular_xy_grid",
            f"(",
            f"{'  file_name':19}: {self.file_name}.sfc,",
            f"{'  xy_unit':19}: {self.xy_unit},",
            f"{'  z_unit':19}: {self.z_unit},",
            f"{'  z_factor':19}: {self.z_factor}",
            f"{'  list':19}: {list}",
            f")",
        )
        return "\n".join(out) + "\n"


@dataclass
class RectangularRim:
    name: str
    centre: struct
    side_lengths: struct

    def __repr__(self) -> str:
        out = (
            f"{self.name}  rectangular_rim",
            f"(",
            f"{'  centre':19}: {self.centre},",
            f"{'  side_lengths':19}: {self.side_lengths}",
            f")",
        )
        return "\n".join(out) + "\n"


@dataclass
class Reflector:
    name: str
    coor_sys: reference
    surfaces: sequence
    rim: RectangularRim

    def __repr__(self) -> str:
        out = (
            f"{self.name}  reflector",
            f"(",
            f"{'  coor_sys':19}: {self.coor_sys},",
            f"{'  surfaces':19}: {self.surfaces},",
            f"{'  rim':19}: {self.rim}",
            f")",
        )
        return "\n".join(out) + "\n"


@dataclass
class EllipticalPattern:
    name: str
    frequency: reference
    coor_sys: reference
    taper: float
    taper_angles: struct
    polarisation_angle: float
    far_forced: bool

    def _on_off(self, value: bool) -> str:
        return "on" if value else "off"

    def __repr__(self) -> str:
        out = (
            f"{self.name}  elliptical_pattern",
            f"(",
            f"{'  frequency':19}: {self.frequency},",
            f"{'  coor_sys':19}: {self.coor_sys},",
            f"{'  taper':19}: {self.taper}",
            f"{'  taper_angles':19}: {self.taper_angles}",
            f"{'  polarisation_angle':21}: {self.polarisation_angle}",
            f"{'  far_forced':19}: {self._on_off(self.far_forced)}",
            f")",
        )
        return "\n".join(out) + "\n"


@dataclass
class TabulatedPattern:
    name: str
    frequency: reference
    coor_sys: reference
    file_name: Path

    def __post_init__(self) -> None:
        self.file_name = self._check_filename(self.file_name)

    def _check_filename(self, file_name: Path) -> Path:
        if not file_name.exists():
            raise FileNotFoundError(f"{file_name} does not exist")

        return file_name.name

    def __repr__(self) -> str:
        out = (
            f"{self.name}  tabulated_pattern",
            f"(",
            f"{'  frequency':19}: {self.frequency},",
            f"{'  coor_sys':19}: {self.coor_sys},",
            f"{'  file_name':19}: {str(self.file_name)}",
            f")",
        )
        return "\n".join(out) + "\n"


class TOR:
    def __init__(self, file: Path) -> None:
        self.file = file

    def _append_lines_to_file(self, lines: list) -> None:
        with open(self.file, "a") as f:
            f.write("\n".join(lines) + "\n")

    def _append_block_to_file(self, block: str) -> None:
        with open(self.file, "a") as f:
            f.write(block)

    def set_frequency(self, frequency: Frequency) -> str:
        self._append_block_to_file(str(frequency))
        return str(frequency)

    def set_coordinate_system(
        self,
        coordinate_system: CoordinateSystem,
    ) -> str:
        self._append_block_to_file(str(coordinate_system))
        return str(coordinate_system)

    def add_planar_cut(self, planar_cut: PlanarCut) -> str:
        self._append_block_to_file(str(planar_cut))
        return str(planar_cut)

    def add_spherical_cut(self, spherical_cut: SphericalCut) -> str:
        self._append_block_to_file(str(spherical_cut))
        return str(spherical_cut)

    def add_bor_mesh(
        self,
        name: str,
        mesh: list[list[float]],
        ref: str,
        regions: list[list[float]],
    ) -> None:

        regions_str = []
        for i, region in enumerate(regions):
            regions_str.append(
                f"\t\t\t{i+1}\t{region[0]}\t{region[1]}\t{region[2]}"
            )

        mesh_str = []
        for i, node in enumerate(mesh):
            mesh_str.append(f"\t\t\t{i+1}\t{node[0]}\t{node[1]}")
        obj_str = [
            f"{name}\tbor_mesh",
            f"(",
            f"\tcoor_sys\t: ref({ref}),",
            f"\tregions\t: table",
            f"\t\t(",
            *regions_str,
            f"\t\t),",
            f"\tnodes\t: table",
            f"\t\t(",
            *mesh_str,
            f"\t\t)",
            f")",
        ]

        self._append_lines_to_file(obj_str)
        return obj_str

    def add_elliptical_pattern(
        self,
        elliptical_pattern: EllipticalPattern,
    ) -> str:
        self._append_block_to_file(str(elliptical_pattern))
        return str(elliptical_pattern)

    def add_tabulated_pattern(
        self,
        tabulated_pattern: TabulatedPattern,
    ) -> str:
        # check if file exists, and change the file_name to be a relative path with respect to the TOR file
        tabulated_pattern.file_name = tabulated_pattern.file_name.relative_to(
            self.file.parent
        )
        self._append_block_to_file(str(tabulated_pattern))
        return str(tabulated_pattern)


def load_tor(file: Path) -> TOR:
    # check if file exists
    if not file.exists():
        raise FileNotFoundError(f"{file} does not exist")

    # read file and return TOR object
