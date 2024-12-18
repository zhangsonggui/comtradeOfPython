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


class SignalType(BaseEnum):
    RELAY = ("Relay", "保护动作出口")
    BREAKER = ("Breaker", "断路器位置")
    SWITCH = ("Switch", "开关位置")
    WARNING = ("Warning", "装置告警出口")
    OTHER = ("Other", "其他")

    @classmethod
    def from_string(cls, string: str):
        string = string.upper()
        for _type in cls:
            if _type == cls.OTHER:
                continue
            if _type.get_code() == string:
                return _type
        return cls.OTHER

    @staticmethod
    def get_flag_enum(_signal_type):
        if _signal_type == SignalType.RELAY:
            return RelayFlag
        elif _signal_type == SignalType.BREAKER:
            return BreakerFlag
        elif _signal_type == SignalType.WARNING:
            return WarningFlag
        else:
            return ChannelFlag


class ChannelFlag(BaseEnum):
    GENERAL = ("general", "一般开关量")

    @classmethod
    def from_string(cls, string: str):
        """
        尝试将给定的字符串转换为对应的枚举成员。

        :param string: 需要被解析的字符串
        :return: 对应的枚举成员或 None 如果没有匹配
        """
        string = string.upper()
        for _type in cls:
            if _type.get_code() == string:
                return _type
        return ''


class RelayFlag(BaseEnum):
    TR = ("Tr", "保护跳闸")
    TRPHSA = ("TrPhsA", "跳A")
    TRPHSB = ("TrPhsB", "跳B")
    TRPHSC = ("TrPhsC", "跳C")
    OPTP = ("OPTP", "三跳信号")
    RECOPCLS = ("RecOpCls", "重合闸")
    BLKREC = ("BlkRec", "永跳信号")
    PROTTX = ("ProtTx", "发信")
    PROTRV = ("ProtRv", "收信")

    @classmethod
    def from_string(cls, string: str):
        """
        尝试将给定的字符串转换为对应的枚举成员。

        :param string: 需要被解析的字符串
        :return: 对应的枚举成员或 None 如果没有匹配
        """
        string = string.upper()
        for _type in cls:
            if _type.get_code() == string:
                return _type
        return ''


class BreakerFlag(BaseEnum):
    HWJ = ("HWJ", "不分相断路器合位")
    TWJ = ("TWJ", "不分相断路器跳位")
    HWJPHSA = ("HWJPhsA", "断路器A相合位")
    HWJPHSB = ("HWJPhsB", "断路器B相合位")
    HWJPHSC = ("HWJPhsC", "断路器C相合位")
    TWJPHSA = ("TWJPhsA", "断路器A相跳位")
    TWJPHSB = ("TWJPhsB", "断路器B相跳位")
    TWJPHSC = ("TWJPhsC", "断路器C相跳位")
    HWJHIGHT = ("HWJHight", "变压器高压侧断路器合位")
    HWJMEDIUM = ("HWJMedium", "变压器中压侧断路器合位")
    HWJLOW = ("HWJLow", "变压器低压侧断路器合位")
    TWJHIGHT = ("TWJHight", "变压器高压侧断路器跳位")
    TWJMEDIUM = ("TWJMedium", "变压器中压侧断路器跳位")
    TWJLOW = ("TWJLow", "变压器低压侧断路器跳位")

    @classmethod
    def from_string(cls, string: str):
        """
        尝试将给定的字符串转换为对应的枚举成员。

        :param string: 需要被解析的字符串
        :return: 对应的枚举成员或 None 如果没有匹配
        """
        string = string.upper()
        for _type in cls:
            if _type.get_code() == string:
                return _type
        return ''


class WarningFlag(BaseEnum):
    WARNVT = ("WarnVt", "TV断线")
    WARNCT = ("WarnCt", "CT断线")
    WARNCOMM = ("WarnComm", "通道告警")
    WARNGENERAL = ("WarnGeneral", "其他告警")

    def __init__(self, code, descripton):
        self.code = code
        self.descripton = descripton

    def get_code(self) -> str:
        return self.code

    def get_description(self) -> str:
        return self.descripton

    @classmethod
    def from_string(cls, string: str):
        """
        尝试将给定的字符串转换为对应的枚举成员。

        :param string: 需要被解析的字符串
        :return: 对应的枚举成员或 None 如果没有匹配
        """
        string = string.upper()
        for _type in cls:
            if _type.get_code() == string:
                return _type
        return ''


class Contact(BaseEnum):
    NORMALLYOPEN = (0, "常开节点")
    NORMALLYCLOSED = (1, "常闭节点")

    @classmethod
    def from_string(cls, string: str):
        """
        尝试将给定的字符串转换为对应的枚举成员。

        :param string: 需要被解析的字符串
        :return: 对应的枚举成员或 None 如果没有匹配
        """
        string = string.upper()
        for _type in cls:
            if _type.get_code() == string:
                return _type
        return cls.NORMALLYOPEN


if __name__ == '__main__':
    signal_type = SignalType.RELAY
    flag_enum = SignalType.get_flag_enum(signal_type)
    if flag_enum:
        for flag in flag_enum:
            print(flag.name, flag.value[1])
