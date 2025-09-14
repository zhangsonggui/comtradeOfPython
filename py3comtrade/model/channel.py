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
from typing import Any, List, Optional, Union

from pydantic import BaseModel, Field

from py3comtrade.model.type.analog_enum import AnalogFlag
from py3comtrade.model.type.phase_code import Phase
from py3comtrade.model.type.types import IdxType
from py3comtrade.utils.channel_dispose import match_channel_name, analog_channel_classification


class ChannelIdx(BaseModel):
    """
    通道索引类
    """
    idx_cfg: int = Field(..., description="通道索引号，必选，数字，整数")
    selected: bool = Field(default=False, description="通道是否被选中")

    def __str__(self):
        return f"{self.idx_cfg}"


class Channel(ChannelIdx):
    """
    通道类
    """
    name: str = Field(..., description="通道标识符，必选，字符串，最大长度128个字符")
    phase: Phase = Field(default=Phase.NO_PHASE,
                         description="通道相别标识，可选，字母、数字，最小0个字符，最大长度2个字符")
    ccbm: str = Field(default="", description="被监视的电路元件，可选，字母、数字，最小0个字符，最大长度64个字符")
    index: int = Field(default=0, description="通道索引号")
    values: Optional[List[Union[float, int]]] = Field(default_factory=list, description="通道数值")

    @property
    def self(self) -> 'Channel':
        """返回类本身实例，支持链式调用"""
        return self

    def remove_fields(self, fields: Union[str, List[str]]) -> 'Channel':
        """
        移除指定的属性字段

        :param fields: 要移除的字段名或字段名列表
        :return: 类本身实例，支持链式调用
        """
        if isinstance(fields, str):
            fields = [fields]

        for field in fields:
            if field in self.model_fields:
                setattr(self, field, None)
        return self

    def clear(self) -> None:
        """清除模型中所有字段"""
        for field in self.model_fields.keys():
            setattr(self, field, None)

    def is_enable(self):
        """通过名称判定该通道是否使用"""
        return not match_channel_name(self.name)

    def channel_flag(self) -> AnalogFlag:
        """根据通道名称和单位判断通道类型"""
        return analog_channel_classification(self.name)

    def is_selected(self,target:list, target_type:IdxType= IdxType.INDEX) -> bool:
        """判断通道是否被选中"""
        if target_type == IdxType.INDEX:
            self.selected = True if self.index in target else False
        else:
            self.selected = True if self.idx_cfg in target else False
        return self.selected

    def __str__(self):
        return super().__str__() + f",{self.name},{self.phase.code},{self.ccbm}"
