import unittest

from src.utilities import smoothing_function


class TestUtilities(unittest.TestCase):

    def test_smoothing_function(self):
        x_min = 0
        x_max = 1
        y_min = 0
        y_max = 1

        self.assertAlmostEqual(smoothing_function(-10, x_min, x_max, y_min, y_max), 0.0, delta=1e-4)
        self.assertAlmostEqual(smoothing_function(0.0, x_min, x_max, y_min, y_max), 0.0, delta=1e-4)
        self.assertAlmostEqual(smoothing_function(0.5, x_min, x_max, y_min, y_max), 0.5, delta=1e-4)
        self.assertAlmostEqual(smoothing_function(1.0, x_min, x_max, y_min, y_max), 1.0, delta=1e-4)
        self.assertAlmostEqual(smoothing_function(10.0, x_min, x_max, y_min, y_max), 1.0, delta=1e-4)
