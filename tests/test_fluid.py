import unittest

from src.fluid import Fluid


class TestPipe(unittest.TestCase):

    def test_water(self):
        f = Fluid({"fluid": "water"})
        self.assertAlmostEqual(f.density(20), 998.2, delta=0.1)
        self.assertAlmostEqual(f.specific_heat(20), 4184.0, delta=0.1)
        self.assertAlmostEqual(f.viscosity(20), 1.00159e-3, delta=1e-6)

    def test_pg(self):
        f = Fluid({"fluid": "pg", "concentration": 20})
        self.assertAlmostEqual(f.density(20), 1014.7, delta=0.1)
        self.assertAlmostEqual(f.specific_heat(20), 3976.7, delta=0.1)
        self.assertAlmostEqual(f.viscosity(20), 2.0300e-3, delta=1e-6)
