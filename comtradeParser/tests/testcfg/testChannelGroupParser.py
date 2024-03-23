#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from comtradeParser.cfg.CFGParser import CFGParser
from comtradeParser.dmf.ChannelGroupParser import ChannelGroupParser
from comtradeParser.dmf.DMFParser import DMFParser


class TestGroupCase(unittest.TestCase):
    def setUp(self):
        cfg_name = '../data/xtz.cfg'
        dmf_name = '../data/xtz.dmf'
        cfg = CFGParser(cfg_name)
        dmf = DMFParser(dmf_name)
        self.cgp = ChannelGroupParser(cfg, dmf)

    def test_get_lines_name(self):
        parsed_data = self.cgp.get_lines_name()[0]
        expected_output = "xyx"
        self.assertEqual(parsed_data, expected_output,
                         msg="get_lines_index函数的输出与预期不符")

    def test_get_lines_model(self):
        test_data = 0
        expected_output = {'accchn': [13, 14, 15, 16],
                           'acvchn': [1, 2, 3, 4],
                           'bus_idx': 1,
                           'bus_name': '220kV I母线',
                           'idx': 4,
                           'isUse': True,
                           'name': 'xyx',
                           'rx': {'r0': '0.2717', 'r1': '0.0893', 'x0': '0.6384', 'x1': '0.3074'},
                           'stachn': [33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44],
                           'type': 'A'}
        parsed_data = self.cgp.get_lines_model()[test_data]
        self.assertEqual(parsed_data.get('name'), expected_output.get('name'),
                         msg="get_lines_index函数的输出与预期不符")
        self.assertEqual(parsed_data.get('bus_name'), expected_output.get('bus_name'),
                         msg="get_lines_index函数的输出与预期不符")
        self.assertEqual(parsed_data.get('rx'), expected_output.get('rx'), msg="get_lines_index函数的输出与预期不符")

    def test_get_buses_name(self):
        test_data = 0
        parsed_data = self.cgp.get_buses_name()[test_data]
        expected_output = "220kV I母线"
        self.assertEqual(parsed_data, expected_output,
                         msg="get_lines_index函数的输出与预期不符")

    def test_get_buses_model(self):
        test_data = 0
        parsed_data = self.cgp.get_buses_model()[test_data]
        expected_output = {
            'acvchn': [1, 2, 3, 4],
            'bus_idx': 1,
            'name': '220kV I母线',
            'idx': 1,
        }
        self.assertEqual(parsed_data.get('name'), expected_output.get('name'),
                         msg="get_lines_index函数的输出与预期不符")
        self.assertEqual(parsed_data.get('bus_idx'), expected_output.get('bus_idx'),
                         msg="get_lines_index函数的输出与预期不符")
        self.assertEqual(parsed_data.get('idx'), expected_output.get('idx'), msg="get_lines_index函数的输出与预期不符")
        self.assertEqual(parsed_data.get('acvchn'), expected_output.get('acvchn'),
                         msg="get_lines_index函数的输出与预期不符")


if __name__ == '__main__':
    unittest.main()
