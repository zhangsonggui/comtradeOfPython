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

    def test_get_channels_analog_ssz(self):
        ch1_ssz = self.parser.get_analog_ssz(1, False, cycle_num=1)
        self.assertEqual(64, len(ch1_ssz[0]))
        ch2_ssz = self.parser.get_analog_ssz([5, 6, 7, 8], False, 0)
        self.assertEqual(4, len(ch2_ssz))


if __name__ == '__main__':
    unittest.main()
