#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from py3comtrade.parser.cfg_parser import CfgParser


class TestCFGCase(unittest.TestCase):

    def setUp(self):
        file_name = r'../data/xtz.cfg'
        self.cfg = CfgParser(file_name).cfg

    def test_get_station_name(self):
        self.assertEqual('xtz', self.cfg.fault_header.station_name)

    def test_get_channel_num(self):
        self.assertEqual(self.cfg.fault_header.channel_total_num, 144)

    def test_get_sample_num(self):
        self.assertEqual(self.cfg.sample_info.sample_total_num, 3077)

    def test_get_cursor_cycle_sample_num(self):
        self.assertEqual(self.cfg.get_cursor_cycle_sample_num(2780), 64)

    def test_get_point_between_segment(self):
        self.assertEqual([0], self.cfg.get_point_between_segment(0, 1000))
        self.assertEqual([0, 1], self.cfg.get_point_between_segment(0, 1290))
        self.assertEqual([1, 2, 3], self.cfg.get_point_between_segment(1290, 3070))

    def test_get_point_between_segment_sample_num(self):
        self.assertEqual([1000], self.cfg.get_point_between_segment_sample_num(0, 1000))
        self.assertEqual([1280, 10], self.cfg.get_point_between_segment_sample_num(0, 1290))
        self.assertEqual([26, 1472, 282], self.cfg.get_point_between_segment_sample_num(1290, 3070))

    def test_get_cursor_point_in_segment(self):
        self.assertEqual(self.cfg.get_cursor_point_in_segment(1), 0)

    def test_get_cursor_sample_range(self):
        # 测试只传递游标位置，获取全部采样点
        self.assertEqual((0, 3076, 3077), self.cfg.get_cursor_sample_range(0))
        # 测试传递游标位置和结束游标位置，获取游标范围内全部采样点，还可以增加不同采样段的游标位置
        self.assertEqual((0, 63, 64), self.cfg.get_cursor_sample_range(0, 63))
        # 测试传递游标位置和周波位置，获取周波范围内全部采样点
        self.assertEqual((0, 63, 64), self.cfg.get_cursor_sample_range(0, cycle_num=1))
        self.assertEqual((0, 95, 96), self.cfg.get_cursor_sample_range(0, cycle_num=1.5))
        self.assertEqual((0, 127, 128), self.cfg.get_cursor_sample_range(0, cycle_num=2))
        # 测试传递游标位置和周波位置，超越游标位置所在段的最后一个和点和第一个点
        self.assertEqual((1, 64, 64), self.cfg.get_cursor_sample_range(1, cycle_num=1))
        self.assertEqual((1216, 1279, 64), self.cfg.get_cursor_sample_range(1270, cycle_num=1, mode=1))
        self.assertEqual((0, 63, 64), self.cfg.get_cursor_sample_range(10, cycle_num=1, mode=-1))
        self.assertEqual((64, 127, 64), self.cfg.get_cursor_sample_range(127, cycle_num=1, mode=-1))
        self.assertEqual((0, 63, 64), self.cfg.get_cursor_sample_range(10, cycle_num=1, mode=0))
        self.assertEqual((69, 132, 64), self.cfg.get_cursor_sample_range(100, cycle_num=1, mode=0))

    def test_get_zero_time_from_cfg(self):
        self.assertEqual(199936, self.cfg.sample_info.fault_time.zero_time)

    def test_get_zero_in_cycle(self):
        self.assertEqual(self.cfg.get_zero_in_cycle(), 0)

    def test_get_zero_point(self):
        self.assertEqual(self.cfg.get_zero_point(), 640)

    def test_get_analog_num(self):
        self.assertEqual(48, self.cfg.fault_header.analog_channel_num)

    def test_get_channel_info(self):
        self.assertEqual("220kV母线II_Ub", self.cfg.get_channel_info(6, 'chid'))
        self.assertEqual("220kV母线II_U", self.cfg.get_channel_info(6, 'ccbm'))
        self.assertEqual("220kVfx2x_211开关_保护一_C相跳闸", self.cfg.get_channel_info(6, 'chid', _type='digital'))

    def test_is_analog_usage(self):
        self.assertEqual(True, self.cfg.analog_channels[6].ratio != 1)
        self.assertEqual(False, self.cfg.analog_channels[37].ratio != 1)

    def test_get_analog_ratio(self):
        self.assertEqual(2200.0, self.cfg.analog_channels[6].ratio)
        self.assertEqual(320.0, self.cfg.analog_channels[25].ratio)
        self.assertEqual(1.0, self.cfg.analog_channels[37].ratio)

    def test_is_primary_analog(self):
        self.assertEqual('S', self.cfg.analog_channels[6].ps)

    def test_get_digital_num(self):
        self.assertEqual(96, self.cfg.fault_header.digital_channel_num)


if __name__ == '__main__':
    unittest.main()
