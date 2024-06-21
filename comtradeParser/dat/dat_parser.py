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
from comtradeParser.cfg.cfg_parser import CfgParser
from comtradeParser.cfg.sample_info import SampleInfo


class DatParser:
    """
    这是用于读取IEEE Comtrade dat文件的python类
    可以解析ASCII、BINARY、BINARY32格式类型
    提供原始采样值、瞬时值的读取
    """

    def __init__(self, cfg: CfgParser, dat_file_name):
        """
        DATParser构造函数：
        :param cfg: 与dat文件匹配的cfg文件对象
        :param dat_file_name: dat文件路径
        """
        self.clear()
        self._cfg: CfgParser = cfg
        # 判断DAT文件的格式
        if self.cfg.sample_info.ft == "ASCII":
            with open(dat_file_name, 'r') as f:
                self._dat_file_content = np.loadtxt(f, delimiter=',').T
        else:
            self._dat_file_content = self._parse_binary_data(dat_file_name)

    def clear(self):
        self._cfg = None  # 清空cfg文件对象
        self._dat_file_content = None  # 清空数据文件内容

    @property
    def cfg(self):
        return self._cfg

    def _parse_binary_data(self, file_name) -> np.ndarray:
        """
        解析二进制格式的DAT文件
        :todo 二进制开关量没有拆分成每个通道
        :param file_name: DAT文件路径
        :return:二进制文件的结构化的numpy数组
        """
        sample: SampleInfo = self.cfg.sample_info
        value = np.zeros((sample.sample_total_num, 2 + self.cfg.analog_channel_num + sample.digital_bytes))
        with open(file_name, "rb") as f:
            for i in range(sample.sample_total_num):
                ana_byte_str = f.read(sample.total_bytes)
                if len(ana_byte_str) != sample.total_bytes:
                    raise ValueError("读取数据长度不符合预期")
                str_struct = f"ii{self.cfg.analog_channel_num}h{sample.digital_bytes}H"
                value[i, :] = struct.unpack(str_struct, ana_byte_str)

        return value.T

    def get_sample_relative_time_list(self, start_point: int = 0, end_point: int = None) -> np.ndarray:
        """
        获取采样点和相对时间数组
        :param start_point: 采样起始点，默认为0
        :param end_point: 采样终止点，不含终止点，默认为None 代表全部采样点
        :return: 采样时间数组
        """
        return self._dat_file_content[0:2, start_point:end_point]

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
        if cfg_an > self.cfg.analog_channel_num:
            raise ValueError(
                f"指定的模拟量通道{cfg_an}大于模拟量通道{self.cfg.analog_channel_num}，无法读取该通道数据!")
        idx = cfg_an - self.cfg.analog_first_index
        values = self._dat_file_content[2 + idx:2 + idx + 1, start_point:end_point]
        return values[0]

    def get_analog_ssz_from_channel(self, cfg_an: int, start_point: int = 0, end_point: int = None,
                                    primary: bool = False) -> np.ndarray:
        """
        读取单个模拟量通道全部采样点瞬时值
        :param cfg_an: CFG文件通道标识
        :param start_point: 采样起始点，默认为0
        :param end_point: 采样终止点，不含终止点，默认为None 代表全部采样点
        :param primary: 输出值类型是一次值还是二次值，默认为False二次值
        :return: 单个模拟量瞬时值数组
        """
        # 获取通道在通道数组中的索引值
        vs = self.get_analog_ysz_from_channel(cfg_an, start_point, end_point)
        # 利用numpy的乘法和加法运算获取瞬时值
        channel: AnalogChannel = self.cfg.analog_channels[cfg_an - self.cfg.analog_first_index]
        ssz = vs * channel.a + channel.b
        # 获取通道是否一次值
        ch_primary = self.cfg.is_primary_analog(cfg_an)
        if primary:
            result = ssz if ch_primary else ssz * channel.ratio
        else:
            result = ssz / channel.ratio if ch_primary else ssz
        return np.around(result, 3)

    def get_digital_ssz_from_channel(self, idx: int, start_point: int = 0, end_point: int = None) -> np.ndarray:
        """
        返回指定状态量通道的瞬时值数组
        :param idx: CFG文件中通道数组中的索引号
        :param start_point: 采样起始点，默认为0
        :param end_point: 采样终止点，不含终止点，默认为None 代表全部采样点
        :return: 指定通道0和1的数组
        """
        # 判断采样通道的合法性，获取通道对应数组的索引值
        if not isinstance(idx, int):
            try:
                idx = int(idx)
            except ValueError:
                raise ValueError(f"指定的模拟量通道{idx}不是数字类型，无法读取该通道数据!")
        if idx > self.cfg.digital_channel_num:
            raise ValueError("指定的开关量通道数大于开关量通道数")
        ch_idx = self._cfg.get_channel_info(idx, 'index', 'dig')
        ch_idx = 2 + self.cfg.analog_channel_num + ch_idx
        values = self._dat_file_content[ch_idx:ch_idx + 1, start_point:end_point]
        return values

    def get_digital_shift_stat_channel(self, idx: int):
        """
        获取单个开关量的变位情况
        :param cfg_an: CFG文件中通道数组中的索引号
        @return: 返回变位的开关量列表
        """
        # 判断采样通道的合法性，获取通道对应数组的索引值
        if not isinstance(idx, int):
            try:
                idx = int(idx)
            except ValueError:
                raise ValueError(f"指定的模拟量通道{idx}不是数字类型，无法读取该通道数据!")
        if idx > self.cfg.digital_channel_num:
            raise ValueError("指定的开关量通道数大于开关量通道数")
        result = []
        ssz = self.get_digital_ssz_from_channel(idx)
        for i, val in enumerate(ssz):
            if i == 0 or ssz[i - 1] != val:
                result.append({"index": i, "value": val})
        return result

    def get_digital_change_channel(self, idx: int):
        ssz = self.get_digital_ssz_from_channel(idx)
        diff = np.diff(ssz)
        change_indices = np.where(diff != 0)[0]
        # 获取变化位置的前后值
        change_values = []
        for idx in change_indices:
            # 因为差分后数组长度比原数组少1，所以变化位置的值需要从原数组获取
            if idx == 0:  # 处理数组开头的变化
                change_values.append((ssz[idx], ssz[idx + 1]))
            elif idx == len(ssz) - 1:  # 处理数组末尾的变化
                change_values.append((ssz[idx - 1], ssz[idx]))
            else:  # 处理数组中间的变化
                change_values.append((ssz[idx - 1], ssz[idx + 1]))
        for i, (before, after) in enumerate(change_values, start=1):
            print(f"Change {i}: Position {change_indices[i - 1]}, from {before} to {after}")
