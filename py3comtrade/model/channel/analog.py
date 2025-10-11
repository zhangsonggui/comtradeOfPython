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

import numpy as np
from pydantic import Field, field_validator

from py3comtrade.dispose.channel_name import analog_channel_classification
from py3comtrade.model.channel.channel import Channel
from py3comtrade.model.type.analog_enum import AnalogFlag, ElectricalUnit, PsType
from py3comtrade.model.type.types import IdxType, ValueType


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

    def clear(self) -> None:
        """清除模型中所有字段"""
        super().clear()
        for field in self.__class__.model_fields.keys():
            setattr(self, field, None)

    @classmethod
    @field_validator('secondary')
    def secondary_must_not_be_zero(cls, v):
        if v == 0:
            raise ValueError(f"secondary属性不能为0")
        return v

    def is_enable(self) -> bool:
        """根据通道名称和变比判断该通道是否使用"""
        return super().is_enable() and self.ratio > 1

    def channel_flag(self) -> AnalogFlag:
        """根据通道名称和单位判断通道类型"""
        return analog_channel_classification(self.name, self.unit)

    def is_selected(self, target: list = None, target_type: IdxType = IdxType.INDEX):
        """判断通道是否被选中"""
        if target is None:
            self.selected = self.is_enable()
            return self.selected
        return super().is_selected(target, target_type)

    def convert_values_type(self, target_value_type: ValueType) -> list:
        """原始采样值瞬时值间转换"""
        # 判断是否存在values属性,如果属性不存在或为空直接返回空列表
        if self.hasattr_values:
            if target_value_type == self.values_type:
                return self.values
            if target_value_type == ValueType.RAW:
                self.values = np.round(self.values).astype(int).tolist()
            else:
                self.values = [(v * self.a + self.b) for v in self.values]
            self.values_type = target_value_type
            return self.values
        return []

    def convert_values_ps(self, target_ps: PsType) -> list[float]:
        """一二次值转换"""
        self.convert_values_type(ValueType.INSTANT)
        if target_ps == self.ps:
            return self.values
        if target_ps == PsType.P:
            self.values = [v * self.ratio for v in self.values]
        else:
            self.values = [v / self.ratio for v in self.values]
        self.ps = target_ps
        return self.values

    def __str__(self):
        return (
                super().__str__()
                + f",{self.unit.code},{self.a},{self.b},{self.skew},{self.min_val},{self.max_val}"
                + f",{self.primary},{self.secondary},{self.ps.code}"
        )
