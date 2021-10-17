import unittest

from src.swhe import calc_conv_resistance


class TestSWHE(unittest.TestCase):

    def test_calc_conv_resistance(self):
        self.assertEqual(calc_conv_resistance(), 42)
