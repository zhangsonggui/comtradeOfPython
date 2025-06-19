#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  Copyright (c) [2019] [name of copyright holder]
#  [py3comtrade] is licensed under Mulan PSL v2.
#  You can use this software according to the terms and conditions of the Mulan
#  PSL v2.
#  You may obtain a copy of Mulan PSL v2 at:
#           http://license.coscl.org.cn/MulanPSL2
#  THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY
#  KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
#  NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
#  See the Mulan PSL v2 for more details.
from ..model import Analog
from ..model.type import ElectricalUnit, PsType,PhaseCode


def analog_parser(line):
    # 去除字符串两端的空格，并按照逗号分割字符串
    line = line.strip().split(",")
    # 创建Analog对象，传入参数
    analog = Analog(idx_cfg=int(line[0]),
                    name=line[1],
                    phase=PhaseCode.from_string(line[2]),
                    ccbm=line[3],
                    unit=ElectricalUnit.from_string(line[4]),
                    a=float(line[5]),
                    b=float(line[6]),
                    skew=float(line[7]),
                    min_val=float(line[8]),
                    max_val=float(line[9]))
    # 如果分割后的字符串长度大于11，则传入更多参数
    if len(line) > 11:
        analog.primary = float(line[10])
        analog.secondary = float(line[11])
        analog.ps = PsType.from_string(line[12])
        analog.ratio = float(line[10]) / float(line[11]) if float(line[11]) != 0 else 1.0
    # 返回Analog对象
    return analog
