#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from comtradeParser.ComtradeParser import ComtradeParser


class testComtradeParser(unittest.TestCase):
    def setUp(self):
        file_name = r'data/xtz.cfg'
        self.parser = ComtradeParser(file_name)

    def test_get_channels_analog_ysz(self):
        ch1_ysz = self.parser.get_analog_ysz(1, 0)
        self.assertEqual(3077, len(ch1_ysz[0]))
        ch2_ysz = self.parser.get_analog_ysz([5, 6, 7, 8], 0)
        self.assertEqual(4, len(ch2_ysz))

    def test_get_analog_ssz(self):
        ch1_ssz = self.parser.get_analog_ssz(1, False, cycle_num=1)
        self.assertEqual(64, len(ch1_ssz[0]))
        ch2_ssz = self.parser.get_analog_ssz([5, 6, 7, 8], False, 0)
        self.assertEqual(4, len(ch2_ssz))

    def test_get_analog_yxz(self):
        ch1_yxz = self.parser.get_analog_yxz(ch_number=1,primary=False,start_point=0,cycle_num=1)
        self.assertEqual(60.189,ch1_yxz[0])
        ch9_yxz = self.parser.get_analog_yxz(ch_number=9,primary=False, start_point= 400,cycle_num=1)
        self.assertEqual(0.473,ch9_yxz[0])

    def test_get_analog_angle(self):
        ch9_angle = self.parser.get_analog_angle(ch_number=9, primary=False, start_point=400, cycle_num=1)
        self.assertEqual(-16.208, ch9_angle[0])

if __name__ == '__main__':
    unittest.main()
