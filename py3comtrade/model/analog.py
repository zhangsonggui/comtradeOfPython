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

from pydantic import Field

from .channel import Channel
from .type import ElectricalUnit, PsType, AnalogFlag
from ..utils.channel_dispose import analog_channel_classification


class Analog(Channel):
    unit: ElectricalUnit = Field(default=ElectricalUnit.NONE, description="通道单位")
    a: float = Field(default=1.0, description="通道增益系数")
    b: float = Field(default=0.0, description="通道偏移系数")
    skew: float = Field(default=0.0, description="通道时滞（us）")
    min_val: float = Field(default=0.0, description="通道最小值")
    max_val: float = Field(default=0.0, description="通道最大值")
    primary: float = Field(default=1.0, description="通道互感器变比一次系数")
    secondary: float = Field(default=1.0, description="通道互感器变比二次系数")
    ps: PsType = Field(default=PsType.P, description="一次还是二次值标识")
    ratio: float = Field(default=1.0, description="通道比率")
    y: list[float] = Field(default_factory=list, description="通道数值")

    def clear(self) -> None:
        """清除模型中所有字段"""
        super().clear()
        for field in self.model_fields.keys():
            setattr(self, field, None)

    def is_enable(self) -> bool:
        """根据通道名称和变比判断该通道是否使用"""
        return super().is_enable() and self.ratio > 1

    def channel_flag(self) -> AnalogFlag:
        """根据通道名称和单位判断通道类型"""
        return analog_channel_classification(self.name, self.unit)

    def __str__(self):
        return (
                super().__str__()
                + f",{self.unit.code},{self.a},{self.b},{self.skew},{self.min_val},{self.max_val}"
                + f",{self.primary},{self.secondary},{self.ps.code}"
        )
