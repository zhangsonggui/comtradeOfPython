import unittest

from py3comtrade.computation.calcium import Calcium


class TestCalcius(unittest.TestCase):
    def setUp(self):
        ssz = [-84.691, -85.198, -84.824, -83.715, -81.708, -78.662, -75.062, -70.744, -65.683, -60.217, -54.29,
               -47.527, -40.1, -32.525, -24.521, -16.524, -8.403, 0.141, 8.59, 16.805, 24.615, 32.291, 39.928,
               47.253, 54.063, 60.256, 65.621, 70.564, 74.836, 78.631, 81.466, 83.426, 84.73, 85.128, 84.816, 83.613,
               81.661, 78.709, 75.007, 70.744, 65.73, 60.186, 54.352, 47.48, 40.163, 32.564, 24.537, 16.657, 8.395,
               -0.031, -8.504, -16.798, -24.622, -32.33, -39.866, -47.207, -54.063, -60.186, -65.621, -70.564, -74.812,
               -78.646, -81.497, -83.394]
        self.cal = Calcium(instant=ssz)

    def test_calc_vector(self):
        self.assertEqual(complex(-5.93, -59.897), self.cal.vector)

    def test_calc_effective(self):
        self.assertEqual(60.19, self.cal.effective)

    def test_calc_angle(self):
        self.assertEqual(-95.654, self.cal.angle)

    def test_calc_dc_component(self):
        self.assertEqual(0.007, self.cal.dc_component)

    def test_calc_harmonics(self):
        self.assertEqual(0.012, self.cal.harmonics.get(2).amplitude)
        self.assertEqual(0.064, self.cal.harmonics.get(3).amplitude)


if __name__ == '__main__':
    unittest.main()
