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
from py3comtrade.model.type.base_enum import BaseEnum


class ElectricalUnit(BaseEnum):
    KILOVOLT = ('kV', '千伏')
    VOLT = ('V', '伏特')
    KILOAMPERE = ('kA', '千安')
    AMPERE = ('A', '安培')
    NO_UNIT = ('', '无')  # 表示无单位的情况

    @classmethod
    def from_string(cls, string: str):
        """
        尝试将给定的字符串转换为对应的枚举成员。

        :param string: 需要被解析的字符串
        :return: 对应的枚举成员或 None 如果没有匹配
        """
        string = string.upper()
        for unit in cls:
            if unit == cls.NO_UNIT:
                continue
            if string.endswith(unit.get_code().upper()):
                return unit
        return cls.NO_UNIT


class PsType(BaseEnum):
    P = ('P', "一次值")
    S = ('S', "二次值")

    @classmethod
    def from_string(cls, string: str):
        """
        尝试将给定的字符串转换为对应的枚举成员。
        :param string: 需要被解析的字符串
        """
        string = string.upper()
        for ps in cls:
            if string.endswith(ps.get_code()):
                return ps
        return cls.P


class AnalogType(BaseEnum):
    AC = ('A', "交流通道")
    DC = ('D', "直流通道")
    OTHER = ('O', "其他通道")

    @classmethod
    def from_string(cls, string: str):
        """
        尝试将给定的字符串转换为对应的枚举成员。
        :param string: 需要被解析的字符串
        """
        string = string.upper()
        for analog in cls:
            if string.endswith(analog.get_code()):
                return analog
        return cls.OTHER


class AnalogFlag(BaseEnum):
    ACV = ('ACV', "电压")
    ACC = ('ACC', "电流")
    HF = ('HF', "高频")
    FQ = ('FQ', "频率")
    AG = ('AG', "相位")
    AMP = ('AMP', "幅值")
    PW = ('PW', "功率")
    ZX = ('ZX', "阻抗")
    CONST = ('CONST', "常量")

    @classmethod
    def from_string(cls, string: str):
        """
        尝试将给定的字符串转换为对应的枚举成员。
        :param string: 需要被解析的字符串
        """
        string = string.upper()
        for analog in cls:
            if string.endswith(analog.get_code()):
                return analog
        return cls.CONST
