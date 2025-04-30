#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from py3comtrade.reader.comtrade_reader import ReadMode, comtrade_reader


class TestComtrade(unittest.TestCase):

    def setUp(self):
        file_name = r'../data/xtz.dat'
        self.comtrade = comtrade_reader(file_name, ReadMode.DAT)

    def test_index_validate_ValidIndex_ReturnsIndex(self):
        index = 3
        result = self.comtrade.index_validate(index)
        self.assertEqual(result, index)

    def test_index_validate_NonIntIndex_RaisesTypeError(self):
        with self.assertRaises(TypeError):
            self.comtrade.index_validate("3")  # 非整数索引

    def test_index_validate_IndexLessThanZero_RaisesValueError(self):
        with self.assertRaises(ValueError):
            self.comtrade.index_validate(-1)

    def test_index_validate_IndexEqualToAnalogNum_RaisesValueError(self):
        with self.assertRaises(ValueError):
            self.comtrade.index_validate(48)  # 等于analog_num

    def test_index_validate_IndexGreaterThanAnalogNum_RaisesValueError(self):
        with self.assertRaises(ValueError):
            self.comtrade.index_validate(49)

    def test_sample_point_validate_ValidStartAndEndPoints_ReturnsPoints(self):
        start_point = 10
        end_point = 20
        result = self.comtrade.sample_point_validate(start_point, end_point)
        self.assertEqual(result, (start_point, end_point))

    def test_sample_point_validate_ValidStartPointAndNoneEnd_ReturnsPoints(self):
        start_point = 10
        result = self.comtrade.sample_point_validate(start_point, None)
        self.assertEqual(result, (start_point, self.comtrade.configure.sample.count - 1))

    def test_sample_point_validate_NonIntegerStartPoint_RaisesTypeError(self):
        with self.assertRaises(TypeError):
            self.comtrade.sample_point_validate("not an int", 20)

    def test_sample_point_validate_NonIntegerEndPoint_RaisesTypeError(self):
        with self.assertRaises(TypeError):
            self.comtrade.sample_point_validate(10, "not an int")

    def test_sample_point_validate_StartPointOutOfRange_RaisesValueError(self):
        with self.assertRaises(ValueError):
            self.comtrade.sample_point_validate(-1, 20)

    def test_sample_point_validate_EndPointOutOfRange_RaisesValueError(self):
        with self.assertRaises(ValueError):
            self.comtrade.sample_point_validate(0, 3077)

    def test_sample_point_validate_EndPointLessThanOrEqualToStartPoint_RaisesValueError(self):
        with self.assertRaises(ValueError):
            self.comtrade.sample_point_validate(20, 10)

    def test_get_raw_samples_by_index(self):
        ch1_ysz = self.comtrade.get_analog_raw_by_index(1)
        self.assertEqual(3077, len(ch1_ysz[0]))
        ch2_ysz = self.comtrade.get_analog_raw_by_index(2, 0, 3076)
        self.assertEqual(3077, len(ch2_ysz[0]))

    def test_get_instant_samples_by_analog(self):
        analog = self.comtrade.configure.get_analog_by_an(1)
        ch1_ssz = self.comtrade.get_instant_by_analog(analog, primary=False)
        self.assertEqual(-84.691, ch1_ssz[0])
        self.assertEqual(65.465, ch1_ssz[602])
        self.assertEqual(85.316, ch1_ssz[1282])

        analog = self.comtrade.configure.get_analog_by_an(11)
        ch11_ssz = self.comtrade.get_instant_by_analog(analog, primary=False)
        self.assertEqual(0.136, ch11_ssz[0])
        self.assertEqual(0.327, ch11_ssz[600])
        self.assertEqual(0.682, ch11_ssz[1281])

    def test_get_instant_samples_by_index(self):
        ch1_ssz = self.comtrade.get_instant_by_index(0, primary=False)
        self.assertEqual(-84.691, ch1_ssz[0])
        self.assertEqual(65.465, ch1_ssz[602])
        self.assertEqual(85.316, ch1_ssz[1282])

        ch11_ssz = self.comtrade.get_instant_by_index(10, primary=False)
        self.assertEqual(0.136, ch11_ssz[0])
        self.assertEqual(0.327, ch11_ssz[600])
        self.assertEqual(0.682, ch11_ssz[1281])
    #
    # def test_calcius(self):
    #     self.comtrade.read(ReadMode.DAT)
    #     analog = self.comtrade.cfg.get_analog_by_an(1)
    #     calcius = self.comtrade.calc_channel_data(analog, site_point=0, cycle_num=1, mode=1)
    #     self.assertEqual(complex(-5.93, -59.897), calcius.phasor)
    #     self.assertEqual(60.19, calcius.effective)
    #     self.assertEqual(-95.654, calcius.angle)
