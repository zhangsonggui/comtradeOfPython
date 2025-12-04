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
# Copyright (C) 2024 - 2024 张松贵, Inc. All Rights Reserved
# 故障采样段信息类，包含该段采样频率、采样点数、采样点开始位置、采样点结束位置、采样点用时、采样点结束位置、采样点原始采样值
# @FileName  :nrate.py
# @Time      :2024/07/05 13:56:30
# @Author    :张松贵
from typing import List

from pydantic import BaseModel, Field

from py3comtrade.model.channel_num import ChannelNum
from py3comtrade.model.nrate import Nrate
from py3comtrade.model.type.data_file_type import DataFileType
from py3comtrade.model.type.types import ValueType


class ConfigSample(BaseModel):
    """
    采样信息
    """
    freg: float = Field(default=50.00, description="电网频率")
    nrate_num: int = Field(default=0, description="采样段个数")
    nrates: List[Nrate] = Field(default_factory=list, description="采样段列表")
    count: int = Field(default=0, description="总采样点数")
    size:int = Field(default=0, description="DAT文件大小")
    data_file_type: DataFileType = Field(default=DataFileType.BINARY, description="数据文件类型")
    value_type: ValueType = Field(default=ValueType.INSTANT, description="采样值类型")
    analog_word: int = Field(default=2, description="模拟量字数")
    digital_word: int = Field(default=2, description="开关量字数")
    analog_sampe_word: int = Field(default=2, description="每采样点模拟量占用的字节数")
    digital_sampe_word: int = Field(default=2, description="每采样点开关量占用的字节数")
    total_sampe_word: int = Field(default=8, description="每采样点占用的字节数")
    channel_num: ChannelNum = Field(default=None, description="通道数量")

    def clear(self):
        self.freg = 50.00
        self.nrate_num = 1
        self.nrates = []
        self.count = 0
        self.data_file_type = DataFileType.BINARY
        self.analog_sampe_word = 2
        self.digital_sampe_word = 2

    def __iter__(self):
        return iter(self.nrates)

    def __getitem__(self, index: int):
        return self.nrates[index]

    def __len__(self):
        return len(self.nrates)

    def __str__(self):
        sample_str = f"{str(self.freg)}\n{str(self.nrate_num)}"
        for nrate in self.nrates:
            sample_str += "\n" + nrate.__str__()
        return sample_str

    def calc_sampling(self):
        """
        计算采样段信息
        """
        if self.freg == 0:
            raise ValueError("电网频率不能为0")
        time_per_cycle = 20  # 每个周波的时间，单位为毫秒
        # 计算各采样段隐含信息
        for i, nrate in enumerate(self.nrates):
            nrate.index = i
            # 更新每个周波采多少个点数
            nrate.cycle_point = float(nrate.samp / self.freg)
            # 每段包含多少个采样点数
            nrate.count = (
                nrate.end_point
                if i == 0
                else nrate.end_point - self.nrates[i - 1].end_point
            )
            # 每段开始的采样点号
            nrate.start_point = 0 if i == 0 else self.nrates[i - 1].end_point

            # 计算采样段一共用了多少时间
            if nrate.cycle_point == 0:
                nrate.cycle_point = 0.5
            nrate.duration = float(nrate.count / nrate.cycle_point * time_per_cycle)
            # 计算每个采样段结束是的时间
            nrate.end_time = (
                nrate.duration
                if i == 0
                else nrate.duration + self.nrates[i - 1].end_time
            )
        # 更新总采样点数
        self.count = self.nrates[-1].end_point
        self.nrate_num = len(self.nrates)
        self.__calc_sample_words()
        self.size = self.count * self.total_sampe_word

    def __calc_sample_words(self):
        """
        根据文件格式计算每采样点占用字节数
        """
        if self.data_file_type.BINARY32 in ("BINARY32", "FLOAT32"):
            self.analog_word = 4
        self.analog_sampe_word = self.analog_word * self.channel_num.analog_num
        self.digital_sampe_word = (self.digital_word * self.channel_num.digital_num) // 16
        self.total_sampe_word = self.analog_sampe_word + self.digital_sampe_word + 8

    def add_nrate(self, nrate: Nrate):
        """添加采样段信息"""
        self.nrates.append(nrate)

    def __setitem__(self, value: Nrate, index: int = None):
        if index is None:
            self.nrates.append(value)
        else:
            self.nrates.insert(index, value)

    @classmethod
    def from_dict(cls, data_dict: dict):
        if not data_dict or not isinstance(data_dict, dict):
            raise TypeError(f"期望字典类型输入，实际得到: {type(data_dict).__name__}")
        freq = data_dict.get("freq", 50.0)
        nrate_num = data_dict.get("nrate_num", 0)
        count = data_dict.get("count", 0)
        data_file_type = DataFileType.from_string(data_dict.get("data_file_type", "BINARY"),
                                                  default=DataFileType.BINARY)
        value_type = ValueType.from_string(data_dict.get("value_type", "INSTANT"), default=ValueType.INSTANT)
        analog_word = data_dict.get("analog_word", 2)
        digital_word = data_dict.get("digital_word", 2)
        analog_sampe_word = data_dict.get("analog_sampe_word", 2)
        digital_sampe_word = data_dict.get("digital_sampe_word", 2)
        total_sampe_word = data_dict.get("total_sampe_word", 2)
        sample = cls(
            freg=freq,
            nrate_num=nrate_num,
            count=count,
            data_file_type=data_file_type,
            value_type=value_type,
            analog_word=analog_word,
            digital_word=digital_word,
            analog_sampe_word=analog_sampe_word,
            digital_sampe_word=digital_sampe_word,
            total_sampe_word=total_sampe_word
        )
        for nrate in data_dict.get("nrates", []):
            nrate = Nrate.from_dict(nrate)
            if nrate is None:
                continue
            sample.nrates.append(nrate)

    def delete_sampling_nrate(self, index: int):
        """删除采样段信息"""
        self.nrates.pop(index)
