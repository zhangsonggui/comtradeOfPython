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

from typing import Union

from pydantic import BaseModel, Field


class ChannelNum(BaseModel):
    """
    cfg文件通道数量
    """

    total_num: int = Field(default=0, description="采样通道总数")
    analog_num: int = Field(default=0, description="模拟量通道数")
    digital_num: int = Field(default=0, description="开关量通道数")

    def __init__(self, total_num: Union[str, int], analog_num: Union[str, int], digital_num: Union[str, int]):
        super().__init__()
        self.total_num = self.__format_channel_num(total_num)
        self.analog_num = self.__format_channel_num(analog_num)
        self.digital_num = self.__format_channel_num(digital_num)

    def clear(self):
        """清除模型中所有字段"""
        for field in self.__fields__.keys():
            setattr(self, field, None)

    def __format_channel_num(self, value: Union[str, int]) -> int:
        if isinstance(value, str):
            return int("".join(filter(str.isdigit, value)))
        if isinstance(value, int):
            return self.__total_num
        return 0

    def __str__(self):
        return f"{self.total_num},{self.analog_num}A,{self.digital_num}D"
