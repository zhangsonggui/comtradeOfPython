#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (C) 2024 - 2024 张松贵, Inc. All Rights Reserved
# 故障采样信息类，包含采样频率、采样段信息、故障时间信息、采样格式、采样时间因子、各采样段采样信息、故障时间信息、每采样点字节使用情况
# 将采样信息对象转字符串
# @FileName  :sample_info.py
# @Time      :2024/07/05 13:57:47
# @Author    :张松贵
from py3comtrade.entity.fault_nrate import FaultNrate
from py3comtrade.entity.fault_time import FaultTime
from py3comtrade.parser.fault_nrate import generate_nrate_str
from py3comtrade.parser.fault_time import generate_fault_time_str


class SampleInfo:
    """
    故障采样信息类
    """

    def __init__(self, lf: int, nrate_num: int, sample_total_num: int, ft: str, timemult: float,
                 nrates: list[FaultNrate], fault_time: FaultTime, bit_width: int, analog_bytes: int = 0,
                 digital_bytes: int = 0, total_bytes: int = 0):
        """
        初始化
        :param lf: 系统频率
        :param nrate_num: 采样段数量
        :param sample_total_num: 采样点总数
        :param ft: 采样格式
        :param timemult: 采样时间因子
        :param nrates: 各采样段采样信息
        :param fault_time: 故障时间信息
        :param bit_width: 模拟量每通道每采样点所占用字节
        :param analog_bytes: 每采样点模拟采样字节数
        :param digital_bytes: 每采样点数字采样字节数
        :param total_bytes: 每采样点总采样字节数
       """
        self.__lf = lf
        self.__nrate_num = nrate_num
        self.__sample_total_num = sample_total_num
        self.__ft = ft
        self.__timemult = timemult
        self.__nrates = nrates
        self.__fault_time = fault_time
        self.__bit_width = bit_width
        self.__analog_bytes = analog_bytes
        self.__digital_bytes = digital_bytes
        self.__total_bytes = total_bytes

    def clear(self) -> None:
        self.__lf = 0
        self.__nrate_num = 0
        self.__sample_total_num = 0
        self.__ft = ''
        self.__timemult = 1.0
        self.__nrates = []
        self.__fault_time = None
        self.__bit_width = 2
        self.__analog_bytes = 0
        self.__digital_bytes = 0
        self.__total_bytes = 0

    @property
    def lf(self):
        """
        获取系统频率
        """
        return self.__lf

    @lf.setter
    def lf(self, value):
        """
        修改系统频率
        """
        self.__lf = value

    @property
    def nrate_num(self):
        """
        获取采样段数量
        """
        return self.__nrate_num

    @nrate_num.setter
    def nrate_num(self, value):
        """
        修改采样段数量
        """
        self.__nrate_num = value

    @property
    def sample_total_num(self):
        """
        获取采样点总数
        """
        return self.__sample_total_num

    @sample_total_num.setter
    def sample_total_num(self, value):
        """
        修改采样点总数
        """
        self.__sample_total_num = value

    @property
    def ft(self):
        """
        获取采样格式
        """
        return self.__ft

    @ft.setter
    def ft(self, value):
        """
        修改采样格式
        """
        self.__ft = value

    @property
    def timemult(self):
        """
        获取采样时间因子
        """
        return self.__timemult

    @timemult.setter
    def timemult(self, value):
        """
        修改采样时间因子
        """
        self.__timemult = value

    @property
    def nrates(self):
        """
        获取各采样段采样信息
        """
        return self.__nrates

    @nrates.setter
    def nrates(self, value):
        """
        修改各采样段采样信息
        """
        self.__nrates = value

    @property
    def fault_time(self):
        """
        获取故障时间信息
        """
        return self.__fault_time

    @fault_time.setter
    def fault_time(self, value):
        """
        修改故障时间信息
        """
        self.__fault_time = value

    @property
    def bit_width(self):
        """
        获取采样格式
        """
        return self.__bit_width

    @bit_width.setter
    def bit_width(self, value):
        """
        修改采样格式
        """
        self.__bit_width = value

    @property
    def analog_bytes(self):
        """
        获取采样格式
        """
        return self.__analog_bytes

    @analog_bytes.setter
    def analog_bytes(self, value):
        """
        修改采样格式
        """
        self.__analog_bytes = value

    @property
    def digital_bytes(self):
        """
        获取采样格式
        """
        return self.__digital_bytes

    @digital_bytes.setter
    def digital_bytes(self, value):
        """
        修改采样格式
        """
        self.__digital_bytes = value

    @property
    def total_bytes(self):
        """
        获取采样格式
        """
        ad = self.analog_bytes + self.digital_bytes * 2
        if self.__total_bytes != ad:
            return ad + 8
        return self.__total_bytes

    @total_bytes.setter
    def total_bytes(self, value):
        """
        修改采样格式
        """
        self.__total_bytes = value

    def nrates_to_string(self):
        """
        修改各采样段采样信息
        """
        nrate_str = ''
        for nrate in self.__nrates:
            nrate_str = generate_nrate_str(nrate) + '\n'
        return nrate_str

    def fault_time_to_string(self):
        """故障时间信息转字符串"""
        return generate_fault_time_str(self.__fault_time)

    def to_string(self) -> str:
        """对象转字符串"""
        nrates_str = self.nrates_to_string()
        fault_time_str = self.fault_time_to_string()
        return f'{self.lf}\n{self.nrate_num}\n{nrates_str}{fault_time_str}\n{self.ft}\n{str(self.timemult)}'
