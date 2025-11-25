#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from py3comtrade.model.header import Header


class TestHeaderParser(unittest.TestCase):

    def test_header_parser(self):
        header_str = "测试变电站,测试录波器,1999"
        header = Header.from_string(header_str)
        self.assertEqual('测试变电站', header.station_name)
        self.assertEqual('测试录波器', header.recorder_name)
        self.assertEqual(1999, header.version)

        header_str = "测试变电站,测试录波器"
        header = Header.from_string(header_str)
        self.assertEqual('测试变电站', header.station_name)
        self.assertEqual('测试录波器', header.recorder_name)
        self.assertEqual(1991, header.version)
