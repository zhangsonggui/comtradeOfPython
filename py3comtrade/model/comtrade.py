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
from typing import Union, Optional

import numpy as np
from pydantic import BaseModel, Field

from py3comtrade.model.analog import Analog
from py3comtrade.model.configure import Configure
from py3comtrade.model.digital import Digital
from py3comtrade.model.type.analog_enum import PsType
from py3comtrade.reader.data_reader import DataReader


class Comtrade(BaseModel):
    file_path: dict = Field(default=None, description="录波文件路径")
    configure: Configure = Field(default=None, description="Comtrade配置对象")
    data: DataReader = Field(default=None, description="Comtrade数据对象")
    digital_change: list = Field(default_factory=[], description="变位开关量通道记录")

    def get_raw_by_index(self, index: int, start_point: int = 0,
                         end_point: int = None) -> np.ndarray:
        """
        获取指定通道、指定采样点的原始采样值
        :param index: 通道索引值
        :param start_point: 采样点开始位置
        :param end_point: 采样点结束位置
        :return: 原始采样值numpy数组
        """
        if index < self.configure.channel_num.analog_num:
            return self.get_analog_raw_by_index(index, start_point, end_point)
        elif index < self.configure.channel_num.digital_num:
            return self.get_digital_raw_by_index(index, start_point, end_point)
        else:
            return self.get_digital_raw_by_index(index - self.configure.channel_num.analog_num, start_point, end_point)

    def get_analog_raw_by_index(self, index: int, start_point: int = 0, end_point: int = None) -> np.ndarray:
        """
        获取指定模拟量通道、指定采样点的原始采样值
        :param index: 模拟量通道索引值
        :param start_point: 采样点开始位置
        :param end_point: 采样点结束位置
        :return: 原始采样值numpy数组
        """
        index = self.index_validate(index)
        start_point, end_point = self.sample_point_validate(start_point, end_point)
        return self.data.analog_value.T[index:index + 1, start_point:end_point + 1]

    def get_digital_raw_by_index(self, index: int, start_point: int = 0, end_point: int = None) -> np.ndarray:
        """
        获取指定开关量、指定采样点的原始采样值
        :param index: 开关量通道索引值
        :param start_point: 采样点开始位置,默认为0
        :param end_point: 采样点结束位置,默认为None,代表全部采样点
        :return: 原始采样numpy数组
        """
        index = self.index_validate(index)
        start_point, end_point = self.sample_point_validate(start_point, end_point)
        return self.data.digital_value.T[index:index + 1, start_point:end_point + 1]

    def get_instant_by_channel(self, channel: Union[Analog, Digital], start_point: int = 0,
                               end_point: int = None, cycle_num: float = None, mode: int = 1,
                               primary: bool = False) -> np.ndarray:
        """
        获取指定通道、指定采样点的瞬时采样值
        :param channel: 通道对象
        :param start_point: 采样点开始位置,默认为0
        :param end_point: 采样点结束位置,默认为None,代表全部采样点
        :param cycle_num: 采样周期数,默认为None,代表全部采样周期
        :param mode: 模式,默认为1,代表向后取值,0为前后取值,1为向前取值
        :param primary: 是否输出主变比值,默认为False,代表输出变比值
        :param end_point: 采样点结束位置,默认为None,代表全部采样点
        :param cycle_num: 采样周期数,默认为None,代表全部采样周期
        :param mode: 模式,默认为1,代表向后取值,0为前后取值,1为向前取值
        :param primary: 是否输出主变比值,默认为False,代表输出变比值
        :return: 瞬时值采样值numpy数组
        """
        if isinstance(channel, Analog):
            return self.get_instant_by_analog(channel, start_point, end_point, cycle_num, mode, primary)
        elif isinstance(channel, Digital):
            return self.get_instant_by_digital(channel, start_point, end_point, cycle_num, mode)
        else:
            raise TypeError("channel must be Analog or Digital")

    def get_instant_by_analog(self, analog: Analog, start_point: int = 0, end_point: int = None,
                              cycle_num: float = None, mode: int = 1, primary: bool = False) -> np.ndarray:
        """
        获取指定通道、指定采样点的瞬时采样值
        :param analog: 通道对象
        :param start_point: 采样点开始位置,默认为0
        :param end_point: 采样点结束位置,默认为None,代表全部采样点
        :param cycle_num: 采样周期数,默认为None,代表全部采样周期
        :param mode: 模式,默认为1,代表向后取值,0为前后取值,1为向前取值
        :param primary: 是否输出主变比值,默认为False,代表输出变比值
        :return: 瞬时值采样值numpy数组
        """
        start_point, end_point, _ = self.configure.get_cursor_sample_range(start_point, end_point, cycle_num, mode)
        # 获取原始值
        values = self.get_analog_raw_by_index(analog.index, start_point, end_point)
        values = values[0] * analog.a + analog.b
        if primary:
            values = values if analog.ps == PsType.P else values * analog.ratio
        else:
            values = values / analog.ratio if analog.ps == PsType.P else values
        return np.around(values, 3)

    def get_instant_by_digital(self, digital: Digital, start_point: int = 0, end_point: int = None,
                               cycle_num: float = None, mode: int = 1) -> np.ndarray:
        """
        获取指定通道、指定采样点的瞬时采样值
        :param digital: 通道对象
        :param start_point: 采样点开始位置,默认为0
        :param end_point: 采样点结束位置,默认为None,代表全部采样点
        :param cycle_num: 采样周期数,默认为None,代表全部采样周期
        :param mode: 模式,默认为1,代表向后取值,0为前后取值,1为向前取值
        """
        start_point, end_point, _ = self.configure.get_cursor_sample_range(start_point, end_point, cycle_num, mode)
        return self.get_digital_raw_by_index(digital.index, start_point, end_point)

    def get_instant_by_index(self, index: int, start_point: int = 0, end_point: int = None,
                             cycle_num: float = None, mode: int = 1, primary: bool = False) -> np.ndarray:
        """
        获取指定通道索引、指定采样点的瞬时采样值
        :param index: 通道索引值
        :param start_point: 采样点开始位置,默认为0
        :param end_point: 采样点结束位置,默认为None,代表全部采样点
        :param cycle_num: 采样周期数,默认为None,代表全部采样周期
        :param mode: 模式,默认为1,代表向后取值,0为前后取值,1为向前取值
        :param primary: 是否输出主变比值,默认为False,代表输出变比值
        :return: 瞬时值采样值numpy数组
        """

        if index < self.configure.channel_num.analog_num:
            analog = self.configure.get_analog_by_index(index)
            return self.get_instant_by_analog(analog, start_point, end_point, cycle_num, mode, primary)
        elif index < self.configure.channel_num.digital_num:
            digital = self.configure.get_digital_by_index(index)
            return self.get_instant_by_digital(digital, start_point, end_point, cycle_num, mode)
        else:
            digital = self.configure.get_digital_by_index(index - self.configure.channel_num.analog_num)
            return self.get_instant_by_digital(digital, start_point, end_point, cycle_num, mode)

    def analyze_digital_change_status(self):
        """
        获取发生变位的开关量对象列表
        """
        for ch in range(self.data.digital_value.shape[1]):
            col = self.data.digital_value[:, ch]
            if col.min() != col.max():
                digital = self.configure.digitals[ch]
                self.digital_change.append(self.configure.digitals[ch])
                # 找出变化点：当前值与前一个值不同
                change_indices = np.where(col[:-1] != col[1:])[0] + 1
                # 获取变化后的值
                change_values = col[change_indices]
                digital.change_status = {
                    "indices": change_indices,
                    "values": change_values
                }
                self.digital_change.append(digital)

    def get_instant_by_analogs(self, analogs: list[Analog], start_point: int = 0, end_point: int = None,
                               cycle_num: float = None, mode: int = 1, primary: bool = False) -> np.ndarray:
        """
        获取指定通道列表、指定采样点的瞬时采样值
        :param analogs: 通道对象列表
        :param start_point: 采样点开始位置,默认为0
        :param end_point: 采样点结束位置,默认为None,代表全部采样点
        :param cycle_num: 采样周期数,默认为None,代表全部采样周期
        :param mode: 模式,默认为1,代表向后取值,0为前后取值,1为向前取值
        :param primary: 是否输出主变比值,默认为False,代表输出变比值
        """
        start_point, end_point, _ = self.configure.get_cursor_sample_range(start_point, end_point, cycle_num, mode)
        instant_samples = []
        for analog in analogs:
            values = self.get_analog_raw_by_index(analog.index, start_point, end_point)
            values = values * analog.a + analog.b
            if primary:
                instant_samples.append(values if analog.ps == PsType.P else values * analog.ratio)
            else:
                instant_samples.append(values / analog.ratio if analog.ps == PsType.P else values)
        return np.array(instant_samples)

    def get_instant_samples_by_segment(self, segment_index, primary: bool = False,
                                       analog: Union[Analog, list[Analog]] = None):
        """
        获取指定采样段、指定通道的瞬时采样值
        :param segment_index: 分段索引
        :param primary: 是否输出主变比值,默认为False,代表输出变比值
        :param analog: 通道对象,默认为None,代表输出全部通道
        :return: 瞬时值采样值numpy数组
        """
        segment = self.configure.sample.nrates[segment_index]
        if isinstance(analog, Analog):
            return self.get_instant_by_analog(analog, segment.start_point, segment.end_point, primary)
        if isinstance(analog, list):
            return self.get_instant_by_analogs(analog, segment.start_point, segment.end_point, primary)
        if analog is None:
            return self.get_instant_by_analogs(self.configure.analogs, segment.start_point, segment.end_point,
                                               primary)

    def index_validate(self, index: int) -> int:
        """
        模拟量通道索引值合法性检测
        """
        if not isinstance(index, int):
            raise TypeError(f"模拟通道索引值类型错误！需要 int 类型，但收到 {type(index).__name__}。")
        channel_num = self.configure.channel_num
        max_index = channel_num.total_num
        if not (0 <= index < max_index):
            raise ValueError(f"模拟量通道索引值超出范围！当前索引值: {index}, 允许范围: [0, {max_index})")
        return index

    def sample_point_validate(self, start_point: int, end_point: Optional[int]) -> tuple[int, int]:
        """
        采样点选取合法性检测
        """
        count = self.configure.sample.count
        if not isinstance(start_point, int):
            raise TypeError(f"采样点开始位置类型错误！需要 int 类型，但收到 {type(start_point).__name__}。")
        if not (0 <= start_point < count):
            raise ValueError(f"采样点开始位置超出录波采样范围！当前采样点位置: {start_point}, 允许范围: [0, {count})")
        if end_point is not None:
            if not isinstance(end_point, int):
                raise TypeError(f"采样点结束位置类型错误！需要 int 类型，但收到 {type(end_point).__name__}。")
            if not (start_point < end_point < count):
                raise ValueError(
                    f"采样点结束位置超出录波采样范围！当前采样点位置: {end_point}, 允许范围: ({start_point}, {count})")
        end_point = self.configure.sample.count - 1 if end_point is None else end_point
        return start_point, end_point
