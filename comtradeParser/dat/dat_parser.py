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

from comtradeParser.cfg.analog_channel import AnalogChannel
from comtradeParser.cfg.entity.digital_channel import DigitalChannel
from comtradeParser.cfg.entity.fault_header import FaultHeader
from comtradeParser.cfg.sample_info import SampleInfo


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
        self.__analog_channel_num = fault_header.analog_channel_num
        self.__digital_channel_num = fault_header.digital_channel_num
        self.__analog_first_index = fault_header.analog_first_index
        self.__digital_first_index = fault_header.digital_first_index
        self.__sample_time_lists = np.zeros((self.__sample_total_num, 2), dtype=np.int32)
        self.__analog_values = np.zeros((self.__sample_total_num, self.__analog_channel_num), dtype=np.float32)
        self.__digital_values = np.zeros((self.__sample_total_num, self.__digital_channel_num), dtype=np.int32)
        self.__changed_digital_channels = self.get_changed_digital_channel()
        self.__changed_digital_channels_details = self.get_digital_channel_change_details()
        # 判断DAT文件的格式
        if sample_info.ft == "ASCII":
            self._parse_ascii_data(dat_file_name)
        else:
            self._parse_binary_data(dat_file_name)

    def clear(self):
        self.__sample_time_lists = None
        self.__analog_values = None
        self.__digital_values = None

    @property
    def changed_digital_channels(self) -> list:
        """
        获取开关量改变的通道列表
        :return:变位开关量列表
        """
        return self.__changed_digital_channels

    def _parse_ascii_data(self, file_name) -> None:
        """
        解析ASCII格式的DAT文件
        :param file_name: DAT文件路径
        :return:ASCII文件的结构化的numpy数组
        """
        with open(file_name, 'r') as f:
            dat_file_content = np.loadtxt(f, delimiter=',')
        self.__sample_time_lists[:] = dat_file_content[0:2]
        self.__analog_values[:] = dat_file_content[2:self.__analog_channel_num + 2]
        self.__digital_values[:] = dat_file_content[self.__analog_channel_num + 2:]

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
                self.__analog_values[i:] = sample_struct[2:self.__analog_channel_num + 2]
                digital_ints = sample_struct[self.__analog_channel_num + 2:]
                self.__digital_values[i:] = digital_split(digital_ints)

    def get_sample_relative_time_list(self, start_point: int = 0, end_point: int = None) -> np.ndarray:
        """
        获取采样点和相对时间数组
        :param start_point: 采样起始点，默认为0
        :param end_point: 采样终止点，不含终止点，默认为None 代表全部采样点
        :return: 采样时间数组
        """
        return self.__sample_time_lists.T[:, start_point:end_point]

    def get_analog_ysz_from_channel(self, cfg_an: int, start_point: int = 0, end_point: int = None) -> np.ndarray:
        """
        读取单个模拟量通道所有原始采样值
        :param cfg_an: CFG文件通道标识
        :param start_point: 采样起始点，默认为0
        :param end_point: 采样终止点，不含终止点，默认为None 代表全部采样点
        :return: 单个模拟量原始采样值数组
        """
        # 判断采样通道的合法性,获取通道对应数组的索引值
        if not isinstance(cfg_an, int):
            try:
                cfg_an = int(cfg_an)
            except ValueError:
                raise ValueError(f"指定的模拟量通道{cfg_an}不是数字类型，无法读取该通道数据!")
        if cfg_an > self.__analog_channel_num:
            raise ValueError(
                f"指定的模拟量通道{cfg_an}大于模拟量通道{self.__analog_channel_num}，无法读取该通道数据!")
        idx = cfg_an - self.__analog_first_index
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
        vs = self.get_analog_ysz_from_channel(analog_channel.an, start_point, end_point)
        # 利用numpy的乘法和加法运算获取瞬时值
        ssz = vs * analog_channel.a + analog_channel.b
        # 判断输出值的类型，根据变比进行转换
        if primary:
            result = ssz if analog_channel.ps == "P" else ssz * analog_channel.ratio
        else:
            result = ssz / analog_channel.ratio if analog_channel.ps == "P" else ssz
        return np.around(result, 3)

    def get_digital_ssz_from_channel(self, digital_channel: DigitalChannel, start_point: int = 0,
                                     end_point: int = None) -> np.ndarray:
        """
        返回指定状态量通道的瞬时值数组
        :param digital_channel: CFG文件中通道数组中的索引号
        :param start_point: 采样起始点，默认为0
        :param end_point: 采样终止点，不含终止点，默认为None 代表全部采样点
        :return: 指定通道0和1的数组
        """
        # 判断采样通道的合法性，获取通道对应数组的索引值
        if not isinstance(digital_channel, DigitalChannel):
            raise ValueError("指定的开关量通道不是DigitalChannel类型")
        if dn := digital_channel.dn > self.__digital_channel_num:
            raise ValueError("指定的开关量通道数大于开关量通道数")
        idx = dn - self.__digital_first_index
        values = self.__digital_values.T[idx:idx + 1, start_point:end_point]
        return values[0]

    def get_digital_channels_first_value(self) -> list:
        """
        获取每个开关通道初始值
        @return: 返回所有开关量通道初始值列表
        """
        first_value = self.__digital_values[0, :]
        return list(first_value)

    def get_digital_channel_change_details(self):
        """
        获取所有变化开关量通道变化详情
        @return: 返回所有开关量通道变化详情列表
        """
        change_channels = self.get_changed_digital_channel()
        change_details = []
        for cc in change_channels:
            # 使用np.diff计算连续元素之间的差异
            ch_idx = cc - self.__digital_first_index
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

    def get_changed_digital_channel(self) -> list:
        """
        获取变位开关量的列表
        @return: 返回变位的开关量列表
        """
        if self.__digital_values.size == 0:  # 检查数据是否为空
            return []  # 如果是空的，直接返回空列表
            # 计算所有列的最大值和最小值
        min_values, max_values = np.min(self.__digital_values, axis=0), np.max(self.__digital_values, axis=0)

        result = []
        for i in range(self.__digital_channel_num):
            if min_values[i] != max_values[i]:  # 如果最大值不等于最小值，说明该列有变化
                result.append(i + self.__digital_first_index)
        return result
