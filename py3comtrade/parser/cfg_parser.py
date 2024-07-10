#!/usr/bin/python3
# _*_ coding: utf-8 _*_
#
# Copyright (C) 2024 - 2024 张松贵, Inc. All Rights Reserved
# 解析comtrade配置文件
# @Author  : 张松贵
# @File    : cfg_parser.py

import numpy as np

from py3comtrade.entity.cfg import Cfg
from py3comtrade.parser.analog_channel import parse_str_analog_channel
from py3comtrade.parser.digital_channel import parse_str_digital_channel
from py3comtrade.parser.fault_header import parse_str_fault_header
from py3comtrade.parser.sample_info import parse_str_sample_info
from py3comtrade.utils.file_tools import read_file_adaptive_encoding


class CfgParser:
    """
    这是用于读取IEEE Comtrade cfg文件的python类
    提供通道信息，开关量信息获取，采样段信息，游标位置和周波采样信息
    """

    # 1.基本信息
    _file_handler = ''  # 文件处理

    def __init__(self, cfg_name, cfg_content=None):
        """
        构造函数：初始化解析CFG文件的实例
        @param cfg_name:CFG文件的路径字符串。
        """
        self.clear()
        if cfg_content is None:
            self._file_handler = read_file_adaptive_encoding(cfg_name)
        else:
            self._file_handler = cfg_content.split('\n')
        self._cfg = self._parse_cfg()

    def clear(self):
        """
        清除类内部的私有变量
        @return:
        """
        # 1.基本信息
        self._file_handler = ''  # 文件处理
        self._cfg = Cfg()

    def _parse_cfg(self):
        """
        解析CFG文件
        """
        fault_header_str = self._file_handler[0:2]
        fault_header = parse_str_fault_header(fault_header_str)
        analog_channels = []
        # 解析模拟量通道信息，从第三行开始到模拟量通道总数+3
        for i in range(2, fault_header.analog_channel_num + 2):
            analog_channel_str = self._file_handler[i]
            analog_channel = parse_str_analog_channel(analog_channel_str)
            # 当第一个模拟量通道的an不为1，则更新第一个模拟量通道的an
            if i == 2 and analog_channel.an != 1:
                fault_header.analog_first_index = analog_channel.an
            analog_channels.append(analog_channel)

        digital_channels = []
        # 解析开关量通道信息,从模拟量通道总数+2开始
        for i in range(fault_header.analog_channel_num + 2, fault_header.channel_total_num + 2):
            digital_channel_str = self._file_handler[i]
            digital_channel = parse_str_digital_channel(digital_channel_str)
            # 当第一个开关量通道的dn不为1，则更新第一个开关量通道的dn
            if i == fault_header.analog_channel_num + 2 and digital_channel.dn != 1:
                fault_header.digital_first_index = digital_channel.dn
            digital_channels.append(digital_channel)
        # 解析采样段信息
        sample_info_str = self._file_handler[fault_header.channel_total_num + 2:]
        sample_info = parse_str_sample_info(sample_info_str)
        # 每个采样点模拟量和开关量的字节数
        sample_info.analog_bytes = fault_header.analog_channel_num * sample_info.bit_width
        sample_info.digital_bytes = int(np.ceil(fault_header.digital_channel_num) / float(16))
        sample_info.total_bytes = 8 + sample_info.analog_bytes + sample_info.digital_bytes * 2
        return Cfg(fault_header, analog_channels, digital_channels, sample_info)

    @property
    def cfg(self):
        """
        获取解析后的CFG对象
        @return:
        """
        return self._cfg
