#!/usr/bin/python3
# _*_ coding: utf-8 _*_
#
# Copyright (C) 2024 - 2024 张松贵, Inc. All Rights Reserved
# @description  "将dat文件解析成numpy数组"
#
# @Time    : 2024/6/14 10:27
# @Author  : 张松贵
# @File    : dat_parser.py
# @IDE     : PyCharm
import struct

import numpy as np

from py3comtrade.entity.dat import Dat
from py3comtrade.entity.fault_header import FaultHeader
from py3comtrade.entity.sample_info import SampleInfo


def digital_split(datas: tuple) -> list:
    """
    将开关量整数数组拆分成数组
    :return: data
    """
    digitals = []
    for data in datas:
        binary_array = [(data >> i) & 1 for i in range(15, -1, -1)]
        binary_array.reverse()
        digitals.extend(binary_array)
    return digitals


class DatParser:
    """
    这是用于读取IEEE Comtrade dat文件的python类
    可以解析ASCII、BINARY、BINARY32格式类型
    提供原始采样值、瞬时值的读取
    """

    def __init__(self, dat_file_name: str, fault_header: FaultHeader, sample_info: SampleInfo):
        """
        DATParser构造函数：
        :param dat_file_name: dat文件路径
        :param fault_header:FaultHeader类,包含模拟量、开关量通道数量及对应的起始索引号
        :param sample_info:
        """
        self.clear()
        self.__sample_total_num = sample_info.sample_total_num
        self.__bit_width = sample_info.bit_width
        self.__analog_bytes = sample_info.analog_bytes
        self.__digital_bytes = sample_info.digital_bytes
        self.__total_bytes = sample_info.total_bytes
        self.__fault_header = fault_header
        self.__sample_time_lists = np.zeros((self.__sample_total_num, 2), dtype=np.int32)
        self.__analog_values = np.zeros((self.__sample_total_num, self.__fault_header.analog_channel_num),
                                        dtype=np.float32)
        self.__digital_values = np.zeros((self.__sample_total_num, self.__fault_header.digital_channel_num),
                                         dtype=np.int32)
        # 判断DAT文件的格式
        if sample_info.ft == "ASCII":
            self._parse_ascii_data(dat_file_name)
        else:
            self._parse_binary_data(dat_file_name)
        self.__changed_digital_channels = self._get_changed_digital_channel()
        self.__digital_channels_state = self._get_digital_channels_state()

    def clear(self):
        self.__sample_time_lists = None
        self.__analog_values = None
        self.__digital_values = None

    @property
    def dat(self) -> Dat:
        return Dat(self.__analog_values, self.__digital_values, self.__sample_time_lists,
                   self.__changed_digital_channels, self.__digital_channels_state, self.__fault_header)

    def _parse_ascii_data(self, file_name) -> None:
        """
        解析ASCII格式的DAT文件
        :param file_name: DAT文件路径
        :return:ASCII文件的结构化的numpy数组
        """
        with open(file_name, 'r') as f:
            dat_file_content = np.loadtxt(f, delimiter=',')
        self.__sample_time_lists = dat_file_content[:, 0:2]
        self.__analog_values = dat_file_content[:, 2:self.__fault_header.analog_channel_num + 2]
        self.__digital_values = dat_file_content[:, self.__fault_header.analog_channel_num + 2:]

    def _parse_binary_data(self, file_name) -> None:
        """
        解析二进制格式的DAT文件
        :param file_name: DAT文件路径
        :return:二进制文件的结构化的numpy数组
        """
        an_bit = int(self.__analog_bytes / self.__bit_width)
        dn_bit = self.__digital_bytes
        str_struct = f"ii{an_bit}h{dn_bit}H"
        with open(file_name, "rb") as f:
            for i in range(self.__sample_total_num):  # 循环每一个采样点
                ana_byte_str = f.read(self.__total_bytes)  # 读取一个采样点所占用的字节
                if len(ana_byte_str) != self.__total_bytes:  # 读取字节长度不够一个采样点的数据
                    raise ValueError("读取数据长度不符合预期")
                sample_struct = struct.unpack(str_struct, ana_byte_str)  # 将二进制格式进行解包
                self.__sample_time_lists[i:] = sample_struct[0:2]
                self.__analog_values[i:] = sample_struct[2:self.__fault_header.analog_channel_num + 2]
                digital_ints = sample_struct[self.__fault_header.analog_channel_num + 2:]
                self.__digital_values[i:] = digital_split(digital_ints)

    def _get_digital_channels_state(self) -> list:
        """
        获取每个开关通道初始值及变位情况
        @return: 返回所有开关量通道初始值列表
        """
        result = []
        for i in range(self.__fault_header.digital_channel_num):
            # 使用np.diff计算连续元素之间的差异
            channel = self.__digital_values[:, i]
            diffs = np.diff(channel)
            # 找到变化的位置，即差异不为0的位置
            change_positions = np.where(diffs != 0)[0] + 1  # 加1是因为np.diff减少了数组的长度
            result.append(
                {
                    "channel": i + self.__fault_header.digital_first_index,
                    "first_state": channel[0],  # 确定初始值
                    "change_positions": change_positions.tolist(),
                    "changes": channel[change_positions].tolist()  # 确定变化的值，即变化位置的元素值
                }
            )
        return result

    def _get_digital_channel_change_details(self):
        """
        获取所有变化开关量通道变化详情
        @return: 返回所有开关量通道变化详情列表
        """
        change_channels = self._get_changed_digital_channel()
        change_details = []
        for cc in change_channels:
            # 使用np.diff计算连续元素之间的差异
            ch_idx = cc - self.__fault_header.digital_first_index
            channel = self.__digital_values[:, ch_idx]
            diffs = np.diff(channel)
            # 找到变化的位置，即差异不为0的位置
            change_positions = np.where(diffs != 0)[0] + 1  # 加1是因为np.diff减少了数组的长度
            change_details.append(
                {
                    "channel": cc,
                    "first_state": channel[0],  # 确定初始值
                    "change_positions": list(change_positions),
                    "changes": list(channel[change_positions])  # 确定变化的值，即变化位置的元素值
                }
            )
        return change_details

    def _get_changed_digital_channel(self) -> list:
        """
        获取变位开关量的列表
        @return: 返回变位的开关量列表
        """
        if self.__digital_values.size == 0:  # 检查数据是否为空
            return []  # 如果是空的，直接返回空列表
            # 计算所有列的最大值和最小值
        min_values, max_values = np.min(self.__digital_values, axis=0), np.max(self.__digital_values, axis=0)

        result = []
        for i in range(self.__fault_header.digital_channel_num):
            if min_values[i] != max_values[i]:  # 如果最大值不等于最小值，说明该列有变化
                result.append(i + self.__fault_header.digital_first_index)
        return result
