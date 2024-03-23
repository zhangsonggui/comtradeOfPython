#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from comtradeParser.cfg.CFGParser import CFGParser
from comtradeParser.dat.DATParser import DATParser


class TestDATCase(unittest.TestCase):
    def setUp(self):
        cfg_name = '../data/xtz.cfg'
        dat_name = '../data/xtz.dat'
        self.cfg = CFGParser(cfg_name)
        self.dat = DATParser(self.cfg, dat_name)

    def test_get_analog_ysz(self):
        ch_number = 1
        ch1_ysz = self.dat.get_analog_ysz_from_channel(ch_number)
        ch1_ysz_num = len(ch1_ysz)
        self.assertEqual(3077, ch1_ysz_num)

    def test_get_analog_ssz(self):
        ch_number1 = 1
        ch1_ssz = self.dat.get_analog_ssz_from_channel(ch_number1, False)
        self.assertEqual(-84.691, ch1_ssz[0])
        self.assertEqual(65.465, ch1_ssz[602])
        self.assertEqual(85.316, ch1_ssz[1282])

        ch_number11 = 11
        ch11_ssz = self.dat.get_analog_ssz_from_channel(ch_number11, False)
        self.assertEqual(0.136, ch11_ssz[0])
        self.assertEqual(0.327, ch11_ssz[600])
        self.assertEqual(0.682, ch11_ssz[1281])

    def test_get_digital_ssz_from_channel(self):
        ch_number = 53
        ch_digital_data = self.dat.get_digital_ssz_from_channel(ch_number)
        ch_digital_data_num = len(ch_digital_data)
        self.assertEqual(3077, ch_digital_data_num)
        self.assertEqual(1, ch_digital_data[722])
        self.assertEqual(0, ch_digital_data[700])
        self.assertEqual(0, ch_digital_data[865])

    def test_get_digital_shift_stat_channel(self):
        ch_45 = self.dat.get_digital_shift_stat_channel(45)
        self.assertEqual(857, ch_45[2].get("index"))
        self.assertEqual(0, ch_45[2].get("value"))


if __name__ == '__main__':
    unittest.main()
