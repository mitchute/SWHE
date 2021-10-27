import unittest

from src.swhe import SWHE


class TestSWHE(unittest.TestCase):

    def setUp(self) -> None:
        data = {
            "pipe": {
                "outer-dia": 0.02667,
                "inner-dia": 0.0215392,
                "length": 100,
                "density": 950,
                "conductivity": 0.4
            },
            "fluid": {
                "fluid-name": "PG",
                "concentration": 20
            },
            "diameter": 1.2,
            "horizontal-spacing": 0.05,
            "vertical-spacing": 0.05,
        }
        self.swhe = SWHE(data)

    def test_calc_v_dot(self):
        self.assertAlmostEqual(self.swhe.calc_v_dot(1, 20), 9.85e-4, delta=1e-6)

    def test_calc_fluid_velocity(self):
        self.assertAlmostEqual(self.swhe.calc_fluid_velocity(1, 20), 2.704, delta=1e-3)

    def test_calc_inside_conv_resistance(self):
        self.assertAlmostEqual(self.swhe.calc_inside_conv_resistance(0.01, 20), 1.616e-3, delta=1e-6)
        self.assertAlmostEqual(self.swhe.calc_inside_conv_resistance(0.1, 20), 2.535e-4, delta=1e-7)
        self.assertAlmostEqual(self.swhe.calc_inside_conv_resistance(0.14, 20), 1.254e-4, delta=1e-7)
        self.assertAlmostEqual(self.swhe.calc_inside_conv_resistance(1, 20), 2.203e-5, delta=1e-8)

    def test_calc_outside_conv_resistance(self):
        self.assertAlmostEqual(self.swhe.calc_outside_conv_resistance(1000, 20, 25), 1.1559e-3, delta=1e-5)
        self.assertAlmostEqual(self.swhe.calc_outside_conv_resistance(1000, 20, 15), 8.619e-4, delta=1e-6)

    def test_calc_inside_fouling_resistance(self):
        self.assertEqual(self.swhe.calc_inside_fouling_resistance(False), 0.0)
        self.assertAlmostEqual(self.swhe.calc_inside_fouling_resistance(True), 2.586e-5, delta=1e-8)

    def test_calc_outside_fouling_resistance(self):
        self.assertEqual(self.swhe.calc_outside_fouling_resistance(False), 0.0)
        self.assertAlmostEqual(self.swhe.calc_outside_fouling_resistance(True), 6.325e-5, delta=1e-8)

    def test_simulate(self):
        outlet_temp = self.swhe.simulate(1, 20, 15)
        self.assertAlmostEqual(outlet_temp, 19.26, delta=0.01)

        outlet_temp = self.swhe.simulate(1, 10, 15)
        self.assertAlmostEqual(outlet_temp, 10.55, delta=0.01)
