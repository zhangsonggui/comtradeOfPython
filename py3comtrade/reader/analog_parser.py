#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ..model.analog import Analog
from ..model.type.analog_enum import ElectricalUnit, PsType
from ..model.type.phase_code import PhaseCode


def analog_parser(line):
    line = line.strip().split(",")
    index = line[0]
    name = line[1]
    phase = PhaseCode.from_string(line[2])
    ccbm = line[3]
    unit = ElectricalUnit.from_string(line[4])
    a = line[5]
    b = line[6]
    skew = line[7]
    min_val = line[8]
    max_val = line[9]
    analog = Analog(index, name, phase, ccbm, unit, a, b, skew, min_val, max_val)
    if len(line) > 11:
        analog.primary = line[10]
        analog.secondary = line[11]
        analog.ps = PsType.from_string(line[12])
    return analog
