#!/usr/bin/python3
# _*_ coding: utf-8 _*_
#
# Copyright (C) 2024 - 2024 张松贵, Inc. All Rights Reserved
# dat文件类
# @Time    : 2024/7/9 11:27
# @Author  : 张松贵
# @File    : dat.py
# @IDE     : PyCharm


import numpy as np

from py3comtrade.entity.analog_channel import AnalogChannel
from py3comtrade.entity.digital_channel import DigitalChannel
from py3comtrade.entity.fault_header import FaultHeader


class Dat:

    def __init__(self, analog_values: np.ndarray, digital_values: np.ndarray,
                 sample_time_lists: np.ndarray, changed_digital_channels: list,
                 digital_channels_state: list, fault_header: FaultHeader):
        """
        dat实体类
        :param analog_values: 模拟量值数组
        :param digital_values: 开关量值数组
        :param sample_time_lists: 采样点相对时间数组
        :param changed_digital_channels: 开关量通道发生列表
        :param digital_channels_state: 开关量通道发生变位详情
        :param fault_header: 故障头信息
        """
        self.__analog_values = analog_values
        self.__digital_values = digital_values
        self.__sample_time_lists = sample_time_lists
        self.__changed_digital_channels = changed_digital_channels
        self.__digital_channels_state = digital_channels_state
        self.__fault_header = fault_header

    def clear(self):
        self.__analog_values = None
        self.__digital_values = None
        self.__sample_time_lists = None
        self.__changed_digital_channels = None
        self.__digital_channels_state = None
        self.__fault_header = None

    @property
    def analog_values(self):
        return self.__analog_values

    @property
    def digital_values(self):
        return self.__digital_values

    @property
    def sample_time_lists(self) -> np.ndarray:
        """
        获取采样点和相对时间数组
        :return: 采样时间数组
        """
        return self.__sample_time_lists

    @property
    def changed_digital_channels(self) -> list:
        """
        获取改变的开关量通道列表
        :return: 改变的开关量通道列表
        """
        return self.__changed_digital_channels

    @property
    def digital_channels_state(self) -> list:
        """
        获取改变的开关量通道改变详情列表
        :return: 改变的开关量通道改变详情列表
        """
        return self.__digital_channels_state

    def get_sample_relative_time_list(self, start_point: int = 0, end_point: int = None) -> np.ndarray:
        """
        获取采样点和相对时间数组
        :param start_point: 采样起始点，默认为0
        :param end_point: 采样终止点，不含终止点，默认为None 代表全部采样点
        :return: 采样时间数组
        """
        return self.__sample_time_lists.T[:, start_point:end_point]

    def get_analog_ysz_from_channel(self, analog_channel: AnalogChannel, start_point: int = 0,
                                    end_point: int = None) -> np.ndarray:
        """
        读取单个模拟量通道所有原始采样值
        :param analog_channel: 模拟量通道对象
        :param start_point: 采样起始点，默认为0
        :param end_point: 采样终止点，不含终止点，默认为None 代表全部采样点
        :return: 单个模拟量原始采样值数组
        """
        # 判断采样通道的合法性,获取通道对应数组的索引值
        if not isinstance(analog_channel, AnalogChannel):
            raise ValueError(f"指定的开关量通道不是DigitalChannel类型!")
        if (an := analog_channel.an) > self.__fault_header.analog_channel_num:
            raise ValueError(f"指定的开关量通道大于开关量通道数!")
        idx = an - self.__fault_header.analog_first_index
        values = self.__analog_values.T[idx:idx + 1, start_point:end_point]
        return values[0]

    def get_analog_ssz_from_channel(self, analog_channel: AnalogChannel, start_point: int = 0,
                                    end_point: int = None, primary: bool = False) -> np.ndarray:
        """
        读取单个模拟量通道全部采样点瞬时值
        :param analog_channel: 模拟量通道对象
        :param start_point: 采样起始点，默认为0
        :param end_point: 采样终止点，不含终止点，默认为None 代表全部采样点
        :param primary: 是否要换算一次值
        :return: 单个模拟量瞬时值数组
        """
        # 获取通道在通道数组中的索引值
        vs = self.get_analog_ysz_from_channel(analog_channel, start_point, end_point)
        # 利用numpy的乘法和加法运算获取瞬时值
        ssz = vs * analog_channel.a + analog_channel.b
        # 判断输出值的类型，根据变比进行转换
        if primary:
            result: np.ndarray = ssz if analog_channel.ps == "P" else ssz * analog_channel.ratio
        else:
            result: np.ndarray = ssz / analog_channel.ratio if analog_channel.ps == "P" else ssz
        return np.around(result, 3)

    def get_digital_ssz_from_channel(self, digital_channel: DigitalChannel, start_point: int = 0,
                                     end_point: int = None) -> np.ndarray:
        """
        返回指定状态量通道的瞬时值数组
        :param digital_channel: 开关量通道对象
        :param start_point: 采样起始点，默认为0
        :param end_point: 采样终止点，不含终止点，默认为None 代表全部采样点
        :return: 指定通道0和1的数组
        """
        # 判断采样通道的合法性，获取通道对应数组的索引值
        if not isinstance(digital_channel, DigitalChannel):
            raise ValueError("指定的开关量通道不是DigitalChannel类型")
        if (dn := digital_channel.dn) > self.__fault_header.digital_channel_num:
            raise ValueError("指定的开关量通道数大于开关量通道数")
        idx = dn - self.__fault_header.digital_first_index
        values = self.__digital_values.T[idx:idx + 1, start_point:end_point]
        return values[0]
