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
from pydantic import BaseModel, Field, model_validator
from typing_extensions import Self


class ChannelNum(BaseModel):
    """
    cfg文件通道数量
    """

    total_num: int = Field(default=0, description="采样通道总数")
    analog_num: int = Field(default=0, description="模拟量通道数")
    digital_num: int = Field(default=0, description="开关量通道数")

    def clear(self):
        """清除模型中所有字段"""
        for field in self.model_fields.keys():
            setattr(self, field, 0)

    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if name in ['analog_num', 'digital_num']:
            super().__setattr__('total_num', self.analog_num + self.digital_num)

    @model_validator(mode="after")
    def validate_and_update_totals(self):
        """自动更新total_num为analog_num和digital_num的和"""
        self.total_num = self.analog_num + self.digital_num
        return self

    def validate_num(self, cfg_line_num: int) -> Self:
        pass

    def __str__(self):
        return f"{self.total_num},{self.analog_num}A,{self.digital_num}D"
