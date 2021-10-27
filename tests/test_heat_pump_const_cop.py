import unittest

from src.heat_pump import HeatPumpConstCOP


class TestSWHE(unittest.TestCase):

    def setUp(self) -> None:
        d = {
            "cop": 3.0,
            "fluid": {
                "fluid-name": "PG",
                "concentration": 20
            },
        }

        self.hp = HeatPumpConstCOP(d)

    def test_simulate_heating(self):
        self.assertAlmostEqual(self.hp.simulate(1000, 0.5, 10), 9.66, delta=0.01)

    def test_simulate_cooling(self):
        self.assertAlmostEqual(self.hp.simulate(-1000, 0.5, 10), 10.67, delta=0.01)
