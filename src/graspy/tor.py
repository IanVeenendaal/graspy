from pathlib import Path
from dataclasses import dataclass


@dataclass
class CoordinateSystem:
    origin: dict[float]
    x_axis: dict[float]


class TOR:
    def __init__(self, file: Path) -> None:
        self.file = file

    def _append_lines_to_file(self, lines: list) -> None:
        with open(self.file, "a") as f:
            f.write("\n".join(lines) + "\n")

    def set_frequency(self, frequency_list: list[float], name: str) -> None:
        if len(frequency_list) == 1:
            f = frequency_list[0]
        obj_str = [
            f"{name}\tfrequency",
            "(",
            f"\tfrequency_list\t: sequence({f} GHz)",
            ")",
        ]

        self._append_lines_to_file(obj_str)
        return obj_str

    def set_coordinate_system(
        self,
        coordinate_system: CoordinateSystem,
        name: str,
        ref: str,
    ) -> None:
        origin = f"struct(x: {coordinate_system.origin['x']} m, y: {coordinate_system.origin['y']} m, z: {coordinate_system.origin['z']} m)"
        x_axis = f"struct(x: {coordinate_system.x_axis['x']}, y: {coordinate_system.x_axis['y']}, z: {coordinate_system.x_axis['z']})"
        obj_str = [
            f"{name}\tcoor_sys",
            f"(",
            f"\torigin\t: {origin},",
            f"\tx_axis\t: {x_axis},",
            f"\tbase\t: ref({ref})",
            f")",
        ]

        self._append_lines_to_file(obj_str)
        return obj_str

    def add_bor_mesh(
        self, name: str, mesh: list[list[float]], ref: str, regions: list[list[float]]
    ) -> None:

        regions_str = []
        for i, region in enumerate(regions):
            regions_str.append(f"\t\t\t{i+1}\t{region[0]}\t{region[1]}\t{region[2]}")

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
