#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from py3comtrade.parser.cfg_parser import CfgParser
from py3comtrade.parser.dat_parser import DatParser


class TestDATCase(unittest.TestCase):
    def setUp(self):
        cfg_name = r'../data/xtz.cfg'
        dat_name = r'../data/xtz.dat'
        self.cfg = CfgParser(cfg_name).cfg
        self.dat = DatParser(dat_name, self.cfg.fault_header, self.cfg.sample_info).dat

    def test_get_analog_ysz(self):
        ch_number = 1
        analog_channel = self.cfg.get_analog_obj(ch_number)
        ch1_ysz = self.dat.get_analog_ysz_from_channel(analog_channel)
        ch1_ysz_num = len(ch1_ysz)
        self.assertEqual(3077, ch1_ysz_num)

    def test_get_analog_ssz(self):
        ch_number1 = 1
        analog_channel = self.cfg.get_analog_obj(ch_number1)
        ch1_ssz = self.dat.get_analog_ssz_from_channel(analog_channel, primary=False)
        self.assertEqual(-84.691, ch1_ssz[0])
        self.assertEqual(65.465, ch1_ssz[602])
        self.assertEqual(85.316, ch1_ssz[1282])

        ch_number11 = 11
        analog_channel = self.cfg.get_analog_obj(ch_number11)
        ch11_ssz = self.dat.get_analog_ssz_from_channel(analog_channel, primary=False)
        self.assertEqual(0.136, ch11_ssz[0])
        self.assertEqual(0.327, ch11_ssz[600])
        self.assertEqual(0.682, ch11_ssz[1281])

    def test_get_digital_ssz_from_channel(self):
        ch_number = 53
        digital_channel = self.cfg.get_digital_obj(ch_number)
        ch_digital_data = self.dat.get_digital_ssz_from_channel(digital_channel)
        ch_digital_data_num = len(ch_digital_data)
        self.assertEqual(3077, ch_digital_data_num)
        self.assertEqual(1, ch_digital_data[722])
        self.assertEqual(0, ch_digital_data[700])
        self.assertEqual(0, ch_digital_data[865])


if __name__ == '__main__':
    unittest.main()
