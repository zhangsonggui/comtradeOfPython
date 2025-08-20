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
from py3comtrade.model.type.base_enum import BaseEnum


class ElectricalUnit(BaseEnum):
    KV = ('kV', '千伏')
    V = ('V', '伏特')
    KA = ('kA', '千安')
    A = ('A', '安培')
    NONE = ('', '无')  # 表示无单位的情况


class Multiplier(BaseEnum):
    K = ('k', "千")
    M = ('m', "百万")
    N = ('n', "无")


class PsType(BaseEnum):
    P = ('P', "一次值")
    S = ('S', "二次值")


class AnalogType(BaseEnum):
    AC = ('A', "交流通道")
    DC = ('D', "直流通道")
    OTHER = ('O', "其他通道")


class AnalogFlag(BaseEnum):
    ACV = ('ACV', "交流电压")
    DCV = ('DCV', "直流电压")
    ACC = ('ACC', "交流电流")
    DCC = ('DCC', "直流电流")
    HF = ('HF', "高频")
    FQ = ('FQ', "频率")
    AG = ('AG', "相位")
    AMP = ('AMP', "幅值")
    PW = ('PW', "功率")
    ZX = ('ZX', "阻抗")
    CONST = ('CONST', "常量")


class BranNum(BaseEnum):
    B1 = (1, "普通线路或3/2接线和电流测量模式")
    B2 = (2, "2/3接线分电流测量模式")


class TvInstallation(BaseEnum):
    BUS = ("bus", "母线侧")
    LINE = ("line", "线路侧")


class CtDirection(BaseEnum):
    POS = ("pos", "正向")
    NEG = ("neg", "反向")
    UNC = ("unc", "未知")


class TransWindLocation(BaseEnum):
    HIGH = ("high", "高压侧")
    MEDIUM = ("medium", "中压侧")
    LOW = ("low", "低压侧")
    COMMON = ("common", "公共绕组")


class WGFlag(BaseEnum):
    Y = ('y', "星形")
    YN = ('yn', "星形接地")
    D = ('d', "三角形")
