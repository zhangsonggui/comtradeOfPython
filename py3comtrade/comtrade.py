#!/usr/bin/python3
# _*_ coding: utf-8 _*_

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

#
#
# @Time    : 2024/3/23 11:27
# @Author  : 张松贵
# @File    : comtrade.py
# @IDE     : PyCharm
from typing import Union

import numpy as np

from py3comtrade.computation.calcium import Calcium
from py3comtrade.model.analog import Analog
from py3comtrade.model.configure import Configure
from py3comtrade.reader.comtrade_reader import ComtradeReader, ReadFileMode
from py3comtrade.reader.data_reader import DataReader


class Comtrade:
    """
    comtrade文件解析类
    """

    __configure: Configure = None
    __data: DataReader = None

    def __init__(self, _comtrade_file_name: str):
        """
        comtrade文件读取初始化
        :param _comtrade_file_name: cfg文件名带后缀名
        """
        self.__comtrade_file_name = _comtrade_file_name

    def clear(self):
        """清除类内部的私有变量"""
        self.__comtrade_file_name = ''
        self.__configure.clear()
        self.__data.clear()

    def read(self, read_mode: ReadFileMode = ReadFileMode.CFG):
        comtrade_reader = ComtradeReader(self.__comtrade_file_name, read_mode)
        self.__configure = comtrade_reader.configure
        self.__data = comtrade_reader.data

    def get_raw_samples_by_index(self, index: int, start_point: int = 0, end_point: int = None) -> np.ndarray:
        """
        获取指定通道、指定采样点的原始采样值
        :param index: 通道索引值
        :param start_point: 采样点开始位置,
        :param end_point: 采样点结束位置
        :return: 原始采样值numpy数组
        """
        if not isinstance(index, int):
            raise TypeError("模拟量通道索引值类型错误!!!")
        if self.cfg.channel_num.analog_num < index < 0:
            raise ValueError(f"模拟量通道索引值超出范围!!!")
        end_point = self.cfg.sample.count - 1 if end_point is None else end_point
        return self.dat.analog_value.T[index:index + 1, start_point:end_point + 1]

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
        start_point, end_point, _ = self.cfg.get_cursor_sample_range(start_point, end_point, cycle_num, mode)
        # 获取原始值
        values = self.get_raw_samples_by_index(analog.index, start_point, end_point)
        values = values * analog.a + analog.b
        if primary:
            values = values if analog.ps == "P" else values * analog.ratio
        else:
            values = values / analog.ratio if analog.ps == "P" else values
        return np.around(values, 3)

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
        start_point, end_point, _ = self.cfg.get_cursor_sample_range(start_point, end_point, cycle_num, mode)
        instant_samples = []
        for analog in analogs:
            values = self.get_raw_samples_by_index(analog.index, start_point, end_point)
            values = values * analog.a + analog.b
            if primary:
                instant_samples.append(values if analog.ps == "P" else values * analog.ratio)
            else:
                instant_samples.append(values / analog.ratio if analog.ps == "P" else values)
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
        segment = self.cfg.sample.nrates[segment_index]
        if isinstance(analog, Analog):
            return self.get_instant_samples_by_analog(analog, segment.start_point, segment.end_point, primary)
        if isinstance(analog, list):
            return self.get_instant_samples_by_analogs(analog, segment.start_point, segment.end_point, primary)
        if analog is None:
            return self.get_instant_samples_by_analogs(self.cfg.analogs, segment.start_point, segment.end_point,
                                                       primary)

    def calc_channel_data(self, analog: Analog, site_point: int = 0, cycle_num: float = None, mode: int = 1) -> Calcium:
        vs = self.get_instant_samples_by_analog(analog, start_point=site_point, cycle_num=cycle_num, mode=mode)
        calcium = Calcium(vs[0])
        return calcium

    @property
    def cfg(self):
        return self.__configure

    @property
    def dat(self):
        return self.__data


if __name__ == '__main__':
    pass
