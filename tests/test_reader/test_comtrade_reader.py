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
        result = self.comtrade._validate_index(index)
        self.assertEqual(result, index)

    def test_index_validate_NonIntIndex_RaisesTypeError(self):
        with self.assertRaises(TypeError):
            self.comtrade._validate_index("3")  # 非整数索引

    def test_index_validate_IndexLessThanZero_RaisesValueError(self):
        with self.assertRaises(ValueError):
            self.comtrade._validate_index(-1)

    def test_index_validate_IndexEqualToAnalogNum_RaisesValueError(self):
        with self.assertRaises(ValueError):
            self.comtrade._validate_index(48)  # 等于analog_num

    def test_index_validate_IndexGreaterThanAnalogNum_RaisesValueError(self):
        with self.assertRaises(ValueError):
            self.comtrade._validate_index(49)

    def test_get_raw_by_analog_index(self):
        ch1_ysz = self.comtrade.get_raw_by_analog_index(1)
        self.assertEqual(3077, len(ch1_ysz[0]))
        ch2_ysz = self.comtrade.get_raw_by_analog_index(2, 0, 3076)
        self.assertEqual(3077, len(ch2_ysz[0]))
        with self.assertRaises(ValueError):
            self.comtrade.get_raw_by_analog_index(48)

    def test_get_raw_by_analog_indices(self):
        ysz1 = self.comtrade.get_raw_by_analog_indices([0, 1, 2])
        self.assertEqual(3077, len(ysz1[0]))
        self.assertEqual(3, ysz1.shape[0])

    def test_get_instant_by_analog(self):
        analog = self.comtrade.cfg.get_analog_by_an(1)
        ch1_ssz = self.comtrade.get_instant_by_analog(analog, primary=False)
        self.assertEqual(-84.691, ch1_ssz[0])
        self.assertEqual(65.465, ch1_ssz[602])
        self.assertEqual(85.316, ch1_ssz[1282])

        analog = self.comtrade.cfg.get_analog_by_an(11)
        ch11_ssz = self.comtrade.get_instant_by_analog(analog, primary=False)
        self.assertEqual(0.136, ch11_ssz[0])
        self.assertEqual(0.327, ch11_ssz[600])
        self.assertEqual(0.682, ch11_ssz[1281])

    def test_get_instant_by_multi_analog(self):
        instants = self.comtrade.get_instant_by_multi_analog()
        self.assertEqual(48, instants.shape[0])
        self.assertEqual(0.136, instants[10][0])

    def test_get_raw_by_digital_index(self):
        d1 = self.comtrade.get_instant_by_digital_index(0)
        self.assertEqual(3077, len(d1[0]))

    def test_get_instant_by_digital_indices(self):
        d1 = self.comtrade.get_instant_by_digital_indices()
        self.assertEqual(3077, len(d1[0]))
        self.assertEqual(0, d1[0][0])
        self.assertEqual(96, d1.shape[0])

    def test_get_instant_by_digital(self):
        digital = self.comtrade.cfg.get_digital_by_dn(1)
        d1 = self.comtrade.get_instant_by_digital(digital)
        self.assertEqual(3077, len(d1[0]))

    def test_get_instant_by_multi_digital(self):
        digitals = self.comtrade.get_instant_by_multi_digital()
        self.assertEqual(96, digitals.shape[0])
        self.assertEqual(0, digitals[0][0])
