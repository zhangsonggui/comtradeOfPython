#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 - 2024 张松贵, Inc. All Rights Reserved
# comtrade实体类
from __future__ import annotations

from typing import List, Union

import numpy as np

from py3comtrade.computation.fourier import dft_rx_channels, eliminate_exp_decay_channels
from py3comtrade.computation.sequence import phasor_to_sequence
from py3comtrade.entity.analog_channel import AnalogChannel
from py3comtrade.entity.cfg import Cfg
from py3comtrade.entity.dat import Dat
from py3comtrade.utils import math_polar_rect


class Comtrade:

    def __init__(self, cfg: Cfg, dat: Dat, dmf=None):
        self.__cfg = cfg
        self.__dmf = dmf
        self.__analog_values = dat.analog_values
        self.__digital_values = dat.digital_values
        self.__sample_time_lists = dat.sample_time_lists
        self.__changed_digital_channels = dat.changed_digital_channels
        self.__digital_channels_state = dat.digital_channels_state

    def clear(self):
        self.__cfg = None
        self.__dmf = None
        self.__analog_values = None
        self.__digital_values = None
        self.__sample_time_lists = None
        self.__changed_digital_channels = None
        self.__digital_channels_state = None

    def get_sample_time_lists(self, start_point: int = 0, end_point: int = None):
        """
        获取采样点和相对时间数组
        :param start_point:采样点开始位置,默认为0
        :param end_point:采样点结束位置,默认为None,代表全部采样点
        """
        return self.__sample_time_lists.T[:, start_point:end_point]

    def get_analog_ysz(self, analog_channels: Union[AnalogChannel, List[AnalogChannel]],
                       start_point: int = 0, end_point: int = None,
                       cycle_num: int = None, mode: int = 1) -> np.ndarray:
        """
        获取指定通道的原始值
        :param analog_channels:通道列表
        :param start_point:采样点开始位置,默认为0
        :param end_point:采样点结束位置,默认为None,代表全部采样点
        :param cycle_num:采样周期数,默认为None,代表全部采样周期
        :param mode:模式,默认为1,代表向后取值,0为前后取值,-1为向前取值
        """
        # 处理analog_channels的类型
        if not isinstance(analog_channels, list):
            analog_channels = [analog_channels]
        # 根据传入的开始和结束采样点,判断是否跨越不同采样频率的采样段避免有效值计算错误
        start_point, end_point, samp_point = self.__cfg.get_cursor_sample_range(start_point, end_point, cycle_num, mode)
        values = np.zeros((len(analog_channels), samp_point), dtype=np.float64)
        for i, analog_channel in enumerate(analog_channels):
            idx = analog_channel.an - self.fault_header.analog_first_index
            # 循环传入的采样通道,将dat中的数组转置后切片
            try:
                values[i] = self.analog_values.T[idx, start_point:end_point + 1]
            except IndexError as e:
                raise ValueError(f'处理通道{analog_channel.an}时发生错误') from e
        return values

    def get_analog_ssz(self, analog_channels: Union[AnalogChannel, List[AnalogChannel]],
                       start_point: int = 0, end_point: int = None,
                       cycle_num: int = None, mode=1, primary: bool = False) -> np.ndarray:
        """
        获取指定通道的采样值
        :param analog_channels:通道对象列表
        :param start_point:采样点开始位置,默认为0
        :param end_point:采样点结束位置,默认为None,代表全部采样点
        :param cycle_num:采样周期数,默认为None,代表全部采样周期
        :param mode:模式,默认为1,代表向后取值,0为前后取值,1为向前取值
        :param primary:是否输出主变比值,默认为False,代表输出变比值
        """
        # 处理analog_channels的类型
        if not isinstance(analog_channels, list):
            analog_channels = [analog_channels]
        # 获取原始值
        values = self.get_analog_ysz(analog_channels, start_point, end_point, cycle_num, mode)
        for i, analog_channel in enumerate(analog_channels):
            # 利用numpy的乘法和加法获取瞬时值
            values[i] = values[i, :] * analog_channel.a + analog_channel.b
            # 判断输出值的类型,根据变比进行转换
            if primary:
                values[i] = values[i, :] if analog_channel.ps == "P" else values[i, :] * analog_channel.ratio
            else:
                values[i] = values[i, :] / analog_channel.ratio if analog_channel.ps == "P" else values[i, :]
        return np.around(values, 3)

    def get_analog_yxz(self, value: np.ndarray = None, sample_rate: int = None, k: int = 1, **kwargs) -> np.ndarray:
        """
        获取模拟量通道当前游标位置整周波的有效值
        :param value: 一个周波的瞬时值数组
        :param sample_rate: 采样率，默认为None,取数组长度
        :param k: 频谱变换的次数，默认为1
        :return 返回有效值列表，索引序号和ch_number对应
        """
        if value is None:
            value = self.get_analog_phasor(**kwargs)
        else:
            if not isinstance(value, np.ndarray):
                raise ValueError(f"输入的瞬时值数组vs必须是numpy数组")
            value = self.get_analog_phasor(value, sample_rate, k)
        return np.around(abs(value), 3)

    def get_analog_phasor(self, value: np.ndarray = None, sample_rate: int = None, k: int = 1, **kwargs) -> np.ndarray:
        """
        获取模拟量通道当前游标位置的相量值
        :param value: 一个周波的瞬时值数组
        :param sample_rate: 采样率，默认为None,取数组长度
        :param k: 频谱变换的次数，默认为1
        :return 返回相量值列表，索引序号和ch_number对应
        """
        if value is None:
            value = self.get_analog_ssz(**kwargs)
        else:
            if not isinstance(value, np.ndarray):
                raise ValueError(f"输入的瞬时值数组vs必须是numpy数组")
        _dft_rx = dft_rx_channels(value, sample_rate, k)
        phasor: np.ndarray = _dft_rx / np.sqrt(2.0)
        return np.around(phasor, 3)

    def get_analog_angle(self, value: np.ndarray = None, sample_rate: int = None, k: int = 1, **kwargs):
        """
        获取模拟量通道当前游标位置角度值
        :param value: 一个周波的瞬时值数组
        :param sample_rate: 采样率，默认为None,取数组长度
        :param k: 频谱变换的次数，默认为1
        :return 返回有效值列表，索引序号和ch_number对应
        """
        angle = []
        if value is None:
            value = self.get_analog_phasor(**kwargs)
        else:
            if not isinstance(value, np.ndarray):
                raise ValueError(f"输入的瞬时值数组vs必须是numpy数组")
            value = self.get_analog_phasor(value, sample_rate, k)
        for item in value:
            angle.append(math_polar_rect.complex_to_polar(item)[1])
        return angle

    def get_analog_xfl_phasor(self, value: np.ndarray = None, decay_dc: bool = False, **kwargs):
        """
        计算序分量

        :param value: 瞬时值数组
        :param decay_dc: 是否过滤直流分量
        :return: 返回一个数组，正序、负序、零序分量值
        """
        if value is None:
            value = self.get_analog_ssz(**kwargs)
        xfl = []
        if decay_dc:
            _dft_rx = eliminate_exp_decay_channels(value)
        else:
            _dft_rx = dft_rx_channels(value)
        # TODO: 目前只实现了一组通道（3组数据）的序分量相量获取，待后续解析DMF或自动生成分组后实现全部
        if value.shape[0] % 3 == 0:
            for i in range(0, value.shape[0], 3):
                xfl.append(phasor_to_sequence(_dft_rx[i:i + 3]))
        else:
            raise ValueError('通道数量必须是3的倍数')
        return np.around(xfl, 3)

    def get_analog_xfl_magnitude(self, vs: np.ndarray = None, **kwargs):
        """
        计算序分量模值
        :param vs:
        :return: 返回一个数组，正序、负序、零序分量值
        """
        magnitude = []
        if vs is None:
            vs = self.get_analog_xfl_phasor(**kwargs)
        for item in vs:
            magnitude.append(abs(item))
        return np.around(magnitude, 3)

    @property
    def cfg(self):
        return self.__cfg

    @property
    def fault_header(self):
        return self.__cfg.fault_header

    @property
    def sample_info(self):
        return self.__cfg.sample_info

    @property
    def analog_channels(self):
        return self.__cfg.analog_channels

    @property
    def digital_channels(self):
        return self.__cfg.digital_channels

    @property
    def analog_values(self):
        return self.__analog_values

    @property
    def digital_values(self):
        return self.__digital_values

    @property
    def sample_time_lists(self):
        return self.__sample_time_lists

    @property
    def changed_digital_channels(self):
        return self.__changed_digital_channels

    @property
    def digital_channels_state(self):
        return self.__digital_channels_state
