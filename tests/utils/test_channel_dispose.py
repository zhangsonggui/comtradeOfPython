#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from py3comtrade.dispose.channel_name import analog_channel_classification, match_channel_name
from py3comtrade.model.type.analog_enum import AnalogFlag


class TestChannelDispose(unittest.TestCase):

    def setUp(self):
        pass

    def test_match_channel_name(self):
        self.assertEqual(True, match_channel_name("模拟量"))
        self.assertEqual(True, match_channel_name("模拟量1"))
        self.assertEqual(True, match_channel_name("模拟量  1"))

        self.assertEqual(True, match_channel_name("电压"))
        self.assertEqual(True, match_channel_name("电压1"))
        self.assertEqual(True, match_channel_name("电压1 Ua"))
        self.assertEqual(False, match_channel_name("220kV母线Ⅱ_Ua"), msg="正常名称")
        self.assertEqual(False, match_channel_name("220kV母线Ⅱ电压_Ua"), msg="正常名称")
        self.assertEqual(False, match_channel_name("220kV母线Ⅱ电压 Ua"), msg="正常名称")

    def test_analog_channel_classification(self):
        self.assertEqual(AnalogFlag.ACV, analog_channel_classification("220kV母线Ⅰ_Ua"))
        self.assertEqual(AnalogFlag.ACV, analog_channel_classification("220kV母线Ⅰ_3U0"))
        self.assertEqual(AnalogFlag.ACV, analog_channel_classification("220kV母线Ⅰ_3U0"))
        self.assertEqual(AnalogFlag.ACC, analog_channel_classification("1号变_高压侧_Ia"))
        self.assertEqual(AnalogFlag.ACC, analog_channel_classification("1号变_高压侧_3I0"))
        self.assertEqual(AnalogFlag.ACC, analog_channel_classification("220kV母联_200开关_Ia"))
        self.assertEqual(AnalogFlag.ACC, analog_channel_classification("220kV亭仁I线_215开关_I Ia"))
        self.assertEqual(AnalogFlag.DCV, analog_channel_classification("220kV亭仁I线高频通道"))
