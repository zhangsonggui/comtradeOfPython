#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from py3comtrade.parser.comtrade_parser import ComtradeParser


class testComtradeParser(unittest.TestCase):
    def setUp(self):
        file_name = r'../data/xtz.cfg'
        self.parser = ComtradeParser(file_name).comtrade

    def test_get_channels_analog_ysz(self):
        ch_number = 1
        analog_channel = self.parser.cfg.get_analog_obj(ch_number)
        ch1_ysz = self.parser.get_analog_ysz(analog_channel, 0)
        self.assertEqual(3077, len(ch1_ysz[0]))

    def test_get_analog_ssz(self):
        ch_number = 1
        analog_channel = self.parser.cfg.get_analog_obj(ch_number)
        ch1_ssz = self.parser.get_analog_ssz(analog_channel, primary=False, cycle_num=1)
        self.assertEqual(64, len(ch1_ssz[0]))

    def test_get_analog_yxz(self):
        ch_number = 1
        analog_channel = self.parser.cfg.get_analog_obj(ch_number)

        ch1_yxz = self.parser.get_analog_yxz(analog_channels=analog_channel, primary=False, start_point=0, cycle_num=1)
        self.assertAlmostEquals(60.189, ch1_yxz[0], places=1)
        ch_number9 = 9
        analog_channel9 = self.parser.cfg.get_analog_obj(ch_number9)
        ch9_yxz = self.parser.get_analog_yxz(analog_channels=analog_channel9, primary=False, start_point=400,
                                             cycle_num=1)
        self.assertAlmostEquals(0.473, ch9_yxz[0], places=1)

    def test_get_analog_angle(self):
        ch_number = 9
        analog_channel = self.parser.cfg.get_analog_obj(ch_number)
        ch9_angle = self.parser.get_analog_angle(analog_channels=analog_channel, primary=False, start_point=400,
                                                 cycle_num=1)
        self.assertAlmostEquals(-16.212, ch9_angle[0])


if __name__ == '__main__':
    unittest.main()
