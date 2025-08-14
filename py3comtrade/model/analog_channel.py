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
from typing import Optional

from pydantic import Field

from .channel import ChannelIdx
from .type import AnalogFlag, AnalogType, ElectricalUnit
from .type.analog_enum import Multiplier, PsType


class AnalogChannel(ChannelIdx):
    idx_org: Optional[int] = Field(description="装置端子号")
    type: AnalogType = Field(default=AnalogType.AC, description="通道类型")
    flag: AnalogFlag = Field(default=AnalogFlag.ACV, description="通道标志")
    p_min: Optional[float] = Field(description="通道一次测量量程最小值，仅对直流类型有效")
    p_max: Optional[float] = Field(description="通道一次测量量程最大值，仅对直流类型有效")
    s_min: Optional[float] = Field(description="通道二次测量量程最小值，仅对直流类型有效")
    s_max: Optional[float] = Field(description="通道二次测量量程最大值，仅对直流类型有效")
    freq: float = Field(default=50.0, description="通道频率")
    au: float = Field(default=1.0, description="直流通道实际物理值的斜率")
    bu: float = Field(default=0.0, description="直流通道实际物理值的截距")
    s_i_unit: ElectricalUnit = Field(default=ElectricalUnit.NONE, description="基本单位")
    multiplier: Multiplier = Field(default=Multiplier.N, description="单位量级")
    primary: float = Field(default=1.0, description="一次系数")
    secondary: float = Field(default=1.0, description="二次系数")
    ps: PsType = Field(default=PsType.S, description="一、二次数据标识")
    phase: str = Field(default="N", description="相别")
