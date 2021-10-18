import unittest

from src.pipe import Pipe


class TestPipe(unittest.TestCase):

    def setUp(self) -> None:
        data = {
            "outer-dia": 0.02667,
            "inner-dia": 0.0215392,
            "length": 100,
            "density": 950,
            "conductivity": 0.4
        }

        self.pipe = Pipe(data)

    def test_bad_init(self):
        with self.assertRaises(ValueError):
            bad_data = {
                "outer-dia": 1,
                "inner-dia": 2
            }
            Pipe(bad_data)

    def test_inner_cx_area(self):
        self.assertAlmostEqual(self.pipe.calc_inner_cross_sectional_area(), 3.643e-4, delta=1e-4)

    def test_outer_cx_area(self):
        self.assertAlmostEqual(self.pipe.calc_outer_cross_sectional_area(), 5.5586e-4, delta=1e-4)

    def test_inner_surf_area(self):
        self.assertAlmostEqual(self.pipe.calc_inner_surface_area(), 6.76, delta=1e-2)

    def test_outer_surf_area(self):
        self.assertAlmostEqual(self.pipe.calc_outer_surface_area(), 8.37, delta=1e-2)

    def test_cond_resistance(self):
        self.assertAlmostEqual(self.pipe.calc_cond_resistance(), 8.5014e-4, delta=1e-4)
