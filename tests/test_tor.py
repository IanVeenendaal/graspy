import unittest
from pathlib import Path
from graspy.tor import TOR, CoordinateSystem


class TestTOR(unittest.TestCase):
    def setUp(self):
        self.file = Path("./tests/test.tor")
        if self.file.exists():
            # Delete file if it exists
            self.file.unlink()
        self.file.touch()
        self.tor = TOR(self.file)

    def tearDown(self):
        # self.file.unlink()
        pass

    def test_set_frequency(self):
        frequency_list = [150]
        name = "frequency_test"
        lines = self.tor.set_frequency(frequency_list, name)
        expected_lines = [
            "frequency_test\tfrequency",
            "(",
            "\tfrequency_list\t: sequence(150 GHz)",
            ")",
        ]
        self.assertEqual(lines, expected_lines)

    def test_set_coordinate_system(self):
        origin = dict(x=0, y=0, z=0)
        x_axis = dict(x=1, y=0, z=0)
        name = "coordinate_system_test"
        ref = "reference"
        coordinate_system = CoordinateSystem(
            origin=origin,
            x_axis=x_axis,
            name=name,
            reference=ref,
        )
        lines = self.tor.set_coordinate_system(coordinate_system)

        expected_lines = [
            "coordinate_system_test\tcoor_sys",
            "(",
            "\torigin\t: struct(x: 0 m, y: 0 m, z: 0 m),",
            "\tx_axis\t: struct(x: 1, y: 0, z: 0),",
            "\tbase\t: ref(reference)",
            ")",
        ]
        self.assertEqual(lines, expected_lines)

    def test_add_bor_mesh(self):
        name = "bor_mesh_test"
        mesh = [[0, 0], [1, 1], [2, 2]]
        ref = "reference"
        regions = [[1, 2, 3]]
        lines = self.tor.add_bor_mesh(name, mesh, ref, regions)

        expected_lines = [
            "bor_mesh_test\tbor_mesh",
            "(",
            "\tcoor_sys\t: ref(reference),",
            "\tregions\t: table",
            "\t\t(",
            "\t\t\t1\t1\t2\t3",
            "\t\t),",
            "\tnodes\t: table",
            "\t\t(",
            "\t\t\t1\t0\t0",
            "\t\t\t2\t1\t1",
            "\t\t\t3\t2\t2",
            "\t\t)",
            ")",
        ]
        self.assertEqual(lines, expected_lines)


if __name__ == "__main__":
    unittest.main()
