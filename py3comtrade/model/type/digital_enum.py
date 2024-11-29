#!/usr/bin/env python
# -*- coding: utf-8 -*-
from enum import Enum


class SingnalType(Enum):
    RELAY = ("Relay", "保护动作出口")
    BREAKER = ("Breaker", "断路器位置")
    SWITCH = ("Switch", "开关位置")
    WARNING = ("Warning", "装置告警出口")
    OTHER = ("Other", "其他")

    @staticmethod
    def get_flag_enum(_signal_type):
        if _signal_type == SingnalType.RELAY:
            return RelayFlag
        elif _signal_type == SingnalType.BREAKER:
            return BreakerFlag
        elif _signal_type == SingnalType.WARNING:
            return WarningFlag
        else:
            return ChannelFlag


class ChannelFlag(Enum):
    GENERAL = ("general", "一般开关量")


class RelayFlag(Enum):
    TR = ("Tr", "保护跳闸")
    TRPHSA = ("TrPhsA", "跳A")
    TRPHSB = ("TrPhsB", "跳B")
    TRPHSC = ("TrPhsC", "跳C")
    OPTP = ("OPTP", "三跳信号")
    RECOPCLS = ("RecOpCls", "重合闸")
    BLKREC = ("BlkRec", "永跳信号")
    PROTTX = ("ProtTx", "发信")
    PROTRV = ("ProtRv", "收信")


class BreakerFlag(Enum):
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


class WarningFlag(Enum):
    WARNVT = ("WarnVt", "TV断线")
    WARNCT = ("WarnCt", "CT断线")
    WARNCOMM = ("WarnComm", "通道告警")
    WARNGENERAL = ("WarnGeneral", "其他告警")


class Contact(Enum):
    NORMALLYOPEN = (0, "常开节点")
    NORMALLYCLOSED = (1, "常闭节点")


if __name__ == '__main__':
    signal_type = SingnalType.RELAY
    flag_enum = SingnalType.get_flag_enum(signal_type)
    if flag_enum:
        for flag in flag_enum:
            print(flag.name, flag.value[1])
