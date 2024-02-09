import unittest
from pathlib import Path
from graspy.tor import TOR, CoordinateSystem


class TestTOR(unittest.TestCase):
    def setUp(self):
        self.file = Path("./tests/test.tor")
        self.tor = TOR(self.file)

    def tearDown(self):
        self.file.unlink()

    def test_set_frequency(self):
        frequency_list = [150]
        name = "frequency_test"
        self.tor.set_frequency(frequency_list, name)

        with open(self.file, "r") as f:
            lines = f.readlines()
            expected_lines = [
                "frequency_test\tfrequency\n",
                "(\n",
                "\tfrequency_list\t: sequence(150 GHz)\n",
                ")\n",
            ]
            self.assertEqual(lines, expected_lines)

    def test_set_coordinate_system(self):
        coordinate_system = CoordinateSystem(origin=(0, 0, 0), x_axis=(1, 0, 0))
        name = "coordinate_system_test"
        ref = "reference"
        self.tor.set_coordinate_system(coordinate_system, name, ref)

        with open(self.file, "r") as f:
            lines = f.readlines()
            expected_lines = [
                "coordinate_system_test\tcoor_sys\n",
                "(\n",
                "\torigin\t: struct(0, 0, 0)\n",
                "\tx_axis\t: struct(1, 0, 0)\n",
                "\tref\t: ref(reference)\n",
                ")\n",
            ]
            self.assertEqual(lines, expected_lines)

    def test_add_bor_mesh(self):
        name = "bor_mesh_test"
        mesh = [[0, 0], [1, 1], [2, 2]]
        ref = "reference"
        regions = [1, 2, 3]
        self.tor.add_bor_mesh(name, mesh, ref, regions)

        with open(self.file, "r") as f:
            lines = f.readlines()
            expected_lines = [
                "bor_mesh_test\tbor_mesh\n",
                "(\n",
                "\tcoor_sys\t: ref(reference)\n",
                "\tregions\t: table\n",
                "\t\t(\n",
                "\t\t\t1\t1\t2\t3\n",
                "\t\t)\n",
                "\tnodes\t: table\n",
                "\t\t(\n",
                "\t\t\t1\t0\t0\n",
                "\t\t\t2\t1\t1\n",
                "\t\t\t3\t2\t2\n",
                "\t\t)\n",
                ")\n",
            ]
            self.assertEqual(lines, expected_lines)


if __name__ == "__main__":
    unittest.main()
