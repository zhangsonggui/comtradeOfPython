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
from py3comtrade.model.channel_num import ChannelNum
from py3comtrade.model.exceptions import ComtradeDataFormatException


def channel_num_from_str(_cn_str: str):
    """从字符串生成通道数量对象"""
    total_num, analog_num, digital_num = _cn_str.strip().split(",")
    total_num = int(total_num)
    analog_num = str_to_int(analog_num)
    digital_num = str_to_int(digital_num)
    if total_num != analog_num + digital_num:
        raise ComtradeDataFormatException(
            F"通道数量校验错误,通道总数{total_num}不等于模拟量数量:{analog_num},开关量数量:{digital_num}之和")
    return ChannelNum(total_num=total_num, analog_num=analog_num, digital_num=digital_num)


def str_to_int(string):
    digits = "".join([char for char in string if char.isdigit()])
    return int(digits) if digits else 0


def channel_num_from_dict(_cn_dict: dict):
    """从字典生成通道数量对象"""
    total_num = _cn_dict.get("total_num", 0)
    analog_num = _cn_dict.get("analog_num", 0)
    digital_num = _cn_dict.get("digital_num", 0)
    if total_num != analog_num + digital_num:
        raise ComtradeDataFormatException(
            F"通道数量校验错误,通道总数{total_num}不等于模拟量数量:{analog_num},开关量数量:{digital_num}之和")
    return ChannelNum(total_num=total_num, analog_num=analog_num, digital_num=digital_num)
