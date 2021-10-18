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
            }
        }
        self.swhe = SWHE(data)

    def test_calc_fluid_velocity(self):
        self.assertEqual(self.swhe.calc_fluid_velocity(1), 42)

    def test_calc_conv_resistance(self):
        self.assertEqual(self.swhe.calc_inside_conv_resistance(1), 42)
