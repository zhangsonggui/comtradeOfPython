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

from py3comtrade.computation.calcium import Calcium
from py3comtrade.model.analog import Analog
from py3comtrade.model.configure import Configure
from py3comtrade.model.type.analog_enum import PsType
from py3comtrade.reader.data_reader import DataReader


class Comtrade(BaseModel):
    file_path: dict = Field(default=None, description="录波文件路径")
    configure: Configure = Field(default=None, description="Comtrade配置对象")
    data: DataReader = Field(default=None, description="Comtrade数据对象")

    def get_raw_samples_by_index(self, index: int, start_point: int = 0, end_point: int = None) -> np.ndarray:
        """
        获取指定通道、指定采样点的原始采样值
        :param index: 通道索引值
        :param start_point: 采样点开始位置
        :param end_point: 采样点结束位置
        :return: 原始采样值numpy数组
        """
        index = self.index_validate(index)
        start_point, end_point = self.sample_point_validate(start_point, end_point)
        return self.data.analog_value.T[index:index + 1, start_point:end_point + 1]

    def get_instant_samples_by_analog(self, analog: Analog, start_point: int = 0, end_point: int = None,
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
        values = self.get_raw_samples_by_index(analog.index, start_point, end_point)
        values = values[0] * analog.a + analog.b
        if primary:
            values = values if analog.ps == "P" else values * analog.ratio
        else:
            values = values / analog.ratio if analog.ps == "P" else values
        return np.around(values, 3)

    def get_instant_samples_by_index(self, index: int, start_point: int = 0, end_point: int = None,
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
        index = self.index_validate(index)
        analog = self.configure.get_analog_by_index(index)
        return self.get_instant_samples_by_analog(analog, start_point, end_point, cycle_num, mode, primary)

    def get_instant_samples_by_analogs(self, analogs: list[Analog], start_point: int = 0, end_point: int = None,
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
            values = self.get_raw_samples_by_index(analog.index, start_point, end_point)
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
            return self.get_instant_samples_by_analog(analog, segment.start_point, segment.end_point, primary)
        if isinstance(analog, list):
            return self.get_instant_samples_by_analogs(analog, segment.start_point, segment.end_point, primary)
        if analog is None:
            return self.get_instant_samples_by_analogs(self.configure.analogs, segment.start_point, segment.end_point,
                                                       primary)

    def calc_channel_data(self, analog: Analog, site_point: int = 0, cycle_num: float = 1.0, mode: int = 1) -> Calcium:
        vs = self.get_instant_samples_by_analog(analog, start_point=site_point, cycle_num=cycle_num, mode=mode)
        calcium = Calcium(vs[0])
        return calcium

    def index_validate(self, index: int) -> int:
        """
        模拟量通道索引值合法性检测
        """
        analog_num = self.configure.channel_num.analog_num
        if not isinstance(index, int):
            raise TypeError(f"模拟通道索引值类型错误！需要 int 类型，但收到 {type(index).__name__}。")
        if not (0 <= index < analog_num):
            raise ValueError(f"模拟量通道索引值超出范围！当前索引值: {index}, 允许范围: [0, {analog_num})")
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
