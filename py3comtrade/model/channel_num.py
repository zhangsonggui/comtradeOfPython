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

from py3comtrade.model.exceptions import ComtradeDataFormatException


class ChannelNum(BaseModel):
    """
    cfg文件通道数量
    """

    total_num: int = Field(default=0, description="采样通道总数")
    analog_num: int = Field(default=0, description="模拟量通道数")
    digital_num: int = Field(default=0, description="开关量通道数")


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

    @staticmethod
    def str_to_int(string: str) -> int:
        digits = "".join([char for char in string if char.isdigit()])
        return int(digits) if digits else 0

    @classmethod
    def from_string(cls, data_str: str) -> 'ChannelNum':
        """
        从字符串中解析通道数量
        :param data_str: 输入的字符串
        :return: ChannelNum对象
        """
        if not data_str or not isinstance(data_str, str):
            raise ComtradeDataFormatException(f"输入字符串不能为空或不是字符串类型")
        total_num, analog_num, digital_num = data_str.strip().split(",")
        total_num = int(total_num)
        analog_num = cls.str_to_int(analog_num)
        digital_num = cls.str_to_int(digital_num)
        if total_num != analog_num + digital_num:
            raise ComtradeDataFormatException(
                F"通道数量校验错误,通道总数{total_num}不等于模拟量数量:{analog_num},开关量数量:{digital_num}之和")
        return cls(total_num=total_num, analog_num=int(analog_num), digital_num=int(digital_num))

    @classmethod
    def from_dict(cls, data_dict: dict) -> 'ChannelNum':
        """
        从字典中解析通道数量
        :param data_dict: 输入的字典
        :return: ChannelNum对象
        """
        if not data_dict or not isinstance(data_dict, dict):
            raise ComtradeDataFormatException(f"输入字典不能为空或不是字典类型")
        total_num = data_dict.get("total_num", 0)
        analog_num = data_dict.get("analog_num", 0)
        digital_num = data_dict.get("digital_num", 0)
        if total_num != analog_num + digital_num:
            raise ComtradeDataFormatException(
                F"通道数量校验错误,通道总数{total_num}不等于模拟量数量:{analog_num},开关量数量:{digital_num}之和")
        return cls(total_num=total_num, analog_num=analog_num, digital_num=digital_num)

    def __str__(self):
        return f"{self.total_num},{self.analog_num}A,{self.digital_num}D"
