#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from py3comtrade.model.exceptions import InvalidIndexException
from py3comtrade.model.type.types import ChannelType, IdxType
from py3comtrade.reader.comtrade_reader import comtrade_reader
from tests import project_root


class TestComtrade(unittest.TestCase):

    def setUp(self):
        file_name = f"{project_root}/tests/data/xtz.dat"
        self.xtz = comtrade_reader(file_name)

    def test_get_channel_data_range(self):
        ch1_ysz = self.xtz.get_channel_data_range(1)

    def test_get_raw_by_analog_index(self):
        ch1_ysz = self.xtz.get_channel_raw_data_range(1)
        self.assertEqual(3077, len(ch1_ysz[0].values))
        ch2_ysz = self.xtz.get_channel_raw_data_range(2, start_point=0, end_point=3076, idx_type=IdxType.INDEX)
        self.assertEqual(3077, len(ch2_ysz[0].values))
        with self.assertRaises(InvalidIndexException):
            self.xtz.get_channel_raw_data_range(48)

    def test_get_raw_by_analog_indices(self):
        ysz1 = self.xtz.get_channel_raw_data_range([0, 1, 2])
        self.assertEqual(7940, ysz1[2].values[4])
        self.assertEqual(3, len(ysz1))

    def test_get_instant_by_analog(self):
        ch1_ssz = self.xtz.get_channel_instant_data_range(0)[0].values
        self.assertEqual(-84.691, ch1_ssz[0])
        self.assertEqual(65.465, ch1_ssz[602])
        self.assertEqual(85.316, ch1_ssz[1282])

        ch11_ssz = self.xtz.get_channel_instant_data_range(11, idx_type=IdxType.CFGAN)[0].values
        self.assertEqual(0.136, ch11_ssz[0])
        self.assertEqual(0.327, ch11_ssz[600])
        self.assertEqual(0.682, ch11_ssz[1281])

    def test_get_instant_by_multi_analog(self):
        instants = self.xtz.get_channel_instant_data_range()
        self.assertEqual(48, len(instants))
        self.assertEqual(0.136, instants[10].values[0])

    def test_get_raw_by_digital_index(self):
        d1 = self.xtz.get_channel_raw_data_range(0, channel_type=ChannelType.DIGITAL)
        self.assertEqual(3077, len(d1[0].values))

    def test_get_instant_by_digital_indices(self):
        d1 = self.xtz.get_channel_raw_data_range(channel_type=ChannelType.DIGITAL)
        self.assertEqual(3077, len(d1[0].values))
        self.assertEqual(0, d1[0].values[0])
        self.assertEqual(96, len(d1))

    def test_get_instant_by_digital(self):
        digital = self.xtz.get_channel_raw_data_range(1, idx_type=IdxType.CFGAN, channel_type=ChannelType.DIGITAL)
        self.assertEqual(3077, len(digital[0].values))

    def test_get_digital_change(self):
        digitals = self.xtz.get_digital_change()
        self.assertEqual(12, len(digitals))
