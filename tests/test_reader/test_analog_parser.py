#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from py3comtrade.model.type.analog_enum import AnalogFlag, ElectricalUnit, PsType
from py3comtrade.model.type.phase_code import Phase
from py3comtrade.reader.analog_parser import analog_from_str


class TestAnalogParser(unittest.TestCase):

    def test_analog_parser(self):
        line_analog_a = ("1,220kV母线_Ua,A,220kV母线_,V,0.007854353,0.000000000,0.000000000,-32767,32767,127017.000000000,"
                         "57.735000000,S")
        analog_a = analog_from_str(line_analog_a)
        self.assertEqual('220kV母线_Ua', analog_a.name)
        self.assertEqual(ElectricalUnit.V, analog_a.unit)
        self.assertEqual(Phase.A_PHASE, analog_a.phase)
        self.assertEqual(PsType.S, analog_a.ps)
        self.assertEqual(True, analog_a.is_enable())
        self.assertEqual(AnalogFlag.ACV, analog_a.channel_flag())

        line_analog_c = ("3,220kV母线_Uc,C,220kV母线_,V,0.007854353,0.000000000,0.000000000,-32767,32767,127017.000000000,"
                         "57.735000000,S")
        analog_c = analog_from_str(line_analog_c)
        self.assertEqual('220kV母线_Uc', analog_c.name)
        self.assertEqual(ElectricalUnit.V, analog_c.unit)
        self.assertEqual(Phase.C_PHASE, analog_c.phase)
        self.assertEqual(PsType.S, analog_c.ps)
