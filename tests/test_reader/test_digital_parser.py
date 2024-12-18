#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from py3comtrade.model.type.phase_code import PhaseCode
from py3comtrade.reader.digital_parser import digital_parser


class TestDigitalParser(unittest.TestCase):

    def test_digital_parser(self):
        line_digital_a = "1,220kV hh1x_211开关_A相断路器合位,A,,0"
        digital_a = digital_parser(line_digital_a)
        self.assertEqual('220kV hh1x_211开关_A相断路器合位', digital_a.name)
        self.assertEqual(PhaseCode.A_PHASE, digital_a.phase)

        line_digital_n = "1,220kV hh1x_211开关_A相断路器合位,,,0"
        digital_n = digital_parser(line_digital_n)
        self.assertEqual('220kV hh1x_211开关_A相断路器合位', digital_n.name)
        self.assertEqual(PhaseCode.NO_PHASE, digital_n.phase)
        self.assertEqual('', digital_n.ccbm)
