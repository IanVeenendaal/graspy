from pathlib import Path


class CoordinateSystem:
    origin: list[float]
    x_axis: list[float]


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

    def set_coordinate_system(
        self,
        coordinate_system: CoordinateSystem,
        name: str,
        ref: str,
    ) -> None:
        obj_str = [
            f"{name}\tcoor_sys",
            f"(",
            f"\torigin\t: struct({coordinate_system.origin})",
            f"\tx_axis\t: struct({coordinate_system.x_axis})",
            f"\tref\t: ref({ref})",
            f")",
        ]

        self._append_lines_to_file(obj_str)

    def add_bor_mesh(
        self, name: str, mesh: list[list[float]], ref: str, regions: list[float]
    ) -> None:
        obj_str = [
            f"{name}\tbor_mesh",
            f"(",
            f"\tcoor_sys\t: ref({ref})",
            f"\tregions\t: table",
            f"\t\t(",
            f"\t\t\t1\t{regions[0]}\t{regions[1]}\t{regions[2]}",
            f"\t\t)",
            f"\tnodes\t: table",
            f"\t\t(",
            f"\t\t\t1\t{mesh[0][0]}\t{mesh[0][1]}",
            # repeat for rest of mesh
            f"\t\t)",
            f")",
        ]

        self._append_lines_to_file(obj_str)
