import unittest

from src.system import System


class TestPipe(unittest.TestCase):

    def setUp(self) -> None:
        data = {
            "hp": {
                "cop": 3.0
            },
            "swhe": {
                "pipe": {
                    "outer-dia": 0.02667,
                    "inner-dia": 0.0215392,
                    "length": 100,
                    "density": 950,
                    "conductivity": 0.4
                },
                "diameter": 1.2,
                "horizontal-spacing": 0.05,
                "vertical-spacing": 0.05,
            },
            "fluid": {
                "fluid-name": "PG",
                "concentration": 20
            }
        }

        self.system = System(data)

    def test_simulate(self):
        self.assertAlmostEqual(self.system.simulate(-1000.0, 0.5, 15), 2.00, delta=0.01)
        self.assertAlmostEqual(self.system.simulate(1000.0, 0.5, 15), -1.27, delta=0.01)
