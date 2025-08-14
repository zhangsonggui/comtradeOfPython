#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  Copyright (c) [2019] [name of copyright holder]
#  [py3comtrade] is licensed under Mulan PSL v2.
#  You can use this software according to the terms and conditions of the Mulan
#  PSL v2.
#  You may obtain a copy of Mulan PSL v2 at:
#           http://license.coscl.org.cn/MulanPSL2
#  THIS SOFTWARE IS PROVIDED ON CFGAN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY
#  KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
#  NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
#  See the Mulan PSL v2 for more details.
from ..model import ChannelNum


def channel_num_parser(line):
    total_num, analog_num, digital_num = line.strip().split(",")
    analog_num = str_to_int(analog_num)
    digital_num = str_to_int(digital_num)
    return ChannelNum(total_num=total_num, analog_num=analog_num, digital_num=digital_num)


def str_to_int(string):
    return int("".join(filter(str.isdigit, string)))
