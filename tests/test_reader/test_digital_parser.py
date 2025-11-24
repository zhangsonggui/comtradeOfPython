#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from py3comtrade.model.channel.digital import Digital
from py3comtrade.model.type.phase_code import Phase


class TestDigitalParser(unittest.TestCase):

    def test_digital_parser(self):
        line_digital_a = "1,220kV hh1x_211开关_A相断路器合位,A,,0"
        digital_a = Digital.from_string(line_digital_a)
        self.assertEqual('220kV hh1x_211开关_A相断路器合位', digital_a.name)
        self.assertEqual(Phase.A_PHASE, digital_a.phase)
        self.assertEqual(line_digital_a, str(digital_a))

        line_digital_n = "1,220kV hh1x_211开关_A相断路器合位,,,0"
        digital_n = Digital.from_string(line_digital_n)
        self.assertEqual('220kV hh1x_211开关_A相断路器合位', digital_n.name)
        self.assertEqual(Phase.NO_PHASE, digital_n.phase)
        self.assertEqual('', digital_n.ccbm)
        self.assertEqual(line_digital_n, str(digital_n))
