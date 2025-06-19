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


class ChannelFlag(BaseEnum):
    GENERAL = ("general", "一般开关量")


class RelayFlag(BaseEnum):
    TR = ("Tr", "保护跳闸")
    TR_PHS_A = ("TrPhsA", "跳A")
    TR_PHS_B = ("TrPhsB", "跳B")
    TR_PHS_C = ("TrPhsC", "跳C")
    OP_TP = ("OPTP", "三跳信号")
    REC_OP_CLS = ("RecOpCls", "重合闸")
    BLK_REC = ("BlkRec", "永跳信号")
    PROT_TX = ("ProtTx", "发信")
    PROT_RV = ("ProtRv", "收信")


class BreakerFlag(BaseEnum):
    HWJ = ("HWJ", "不分相断路器合位")
    TWJ = ("TWJ", "不分相断路器跳位")
    HWJ_PHS_A = ("HWJPhsA", "断路器A相合位")
    HWJ_PHS_B = ("HWJPhsB", "断路器B相合位")
    HWJ_PHS_C = ("HWJPhsC", "断路器C相合位")
    TWJ_PHS_A = ("TWJPhsA", "断路器A相跳位")
    TWJ_PHS_B = ("TWJPhsB", "断路器B相跳位")
    TWJ_PHS_C = ("TWJPhsC", "断路器C相跳位")
    HWJ_HIGHT = ("HWJHight", "变压器高压侧断路器合位")
    HWJ_MEDIUM = ("HWJMedium", "变压器中压侧断路器合位")
    HWJ_LOW = ("HWJLow", "变压器低压侧断路器合位")
    TWJ_HIGHT = ("TWJHight", "变压器高压侧断路器跳位")
    TWJ_MEDIUM = ("TWJMedium", "变压器中压侧断路器跳位")
    TWJ_LOW = ("TWJLow", "变压器低压侧断路器跳位")


class WarningFlag(BaseEnum):
    WARN_VT = ("WarnVt", "TV断线")
    WARN_CT = ("WarnCt", "CT断线")
    WARN_COMM = ("WarnComm", "通道告警")
    WARN_GENERAL = ("WarnGeneral", "其他告警")


class Contact(BaseEnum):
    NORMALLY_OPEN = (0, "常开节点")
    NORMALLY_CLOSED = (1, "常闭节点")
