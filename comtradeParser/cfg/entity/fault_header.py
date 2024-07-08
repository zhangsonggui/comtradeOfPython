#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (C) 2024 - 2024 张松贵, Inc. All Rights Reserved
# 故障头信息，包含变电站名称、采集设备ID、版本信息、通道总数、模拟通道数、数字通道数、模拟通道起始索引、数字通道起始索引
# @FileName  :fault_header.py
# @Time      :2024/07/05 13:54:46
# @Author    :张松贵

class FaultHeader:

    def __init__(self, station_name: str = '变电站', rec_dev_id: str = '录波设备', rev_year: int = 1999,
                 channel_total_num: int = 0, analog_channel_num: int = 0, digital_channel_num: int = 0,
                 analog_first_index: int = 1, digital_first_index: int = 1):
        """
        初始化
        :param station_name: 变电站名称
        :param rec_dev_id: 采集设备ID
        :param rev_year: 版本信息
        :param channel_total_num: 通道总数
        :param analog_channel_num: 模拟通道数
        :param digital_channel_num: 数字通道数
        :param analog_first_index: 模拟通道起始索引
        :param digital_first_index: 数字通道起始索引
        """
        self.__station_name = station_name
        self.__rec_dev_id = rec_dev_id
        self.__rev_year = rev_year
        self.__analog_channel_num = analog_channel_num
        self.__digital_channel_num = digital_channel_num
        if channel_total_num != (tt := analog_channel_num + digital_channel_num):
            self.__channel_total_num = tt
        else:
            self.__channel_total_num = channel_total_num
        self.__analog_first_index = analog_first_index
        self.__digital_first_index = digital_first_index

    def clear(self):
        self.__station_name = ''
        self.__rec_dev_id = ''
        self.__rev_year = 1991
        self.__channel_total_num = 0
        self.__analog_channel_num = 0
        self.__digital_channel_num = 0
        self.__analog_first_index = 1
        self.__digital_first_index = 1

    @property
    def station_name(self):
        """
        变电站名称
        """
        return self.__station_name

    @station_name.setter
    def station_name(self, value):
        """
        修改变电站名称
        """
        self.__station_name = value

    @property
    def rec_dev_id(self):
        """
        采集设备ID
        """
        return self.__rec_dev_id

    @rec_dev_id.setter
    def rec_dev_id(self, value):
        """
        修改采集设备ID
        """
        self.__rec_dev_id = value

    @property
    def rev_year(self):
        """
        版本信息
        """
        return self.__rev_year

    @rev_year.setter
    def rev_year(self, value):
        """
        修改版本信息
        """
        self.__rev_year = value

    @property
    def channel_total_num(self):
        """
        通道总数
        """
        return self.__channel_total_num

    @channel_total_num.setter
    def channel_total_num(self, value):
        """
        修改通道总数
        """
        self.__channel_total_num = value

    @property
    def analog_channel_num(self):
        """
        模拟通道数
        """
        return self.__analog_channel_num

    @analog_channel_num.setter
    def analog_channel_num(self, value):
        """
        修改模拟通道数
        """
        self.__analog_channel_num = value

    @property
    def digital_channel_num(self):
        """
        数字通道数
        """
        return self.__digital_channel_num

    @digital_channel_num.setter
    def digital_channel_num(self, value):
        """
        修改数字通道数
        """
        self.__digital_channel_num = value

    @property
    def analog_first_index(self):
        """
        模拟通道起始索引
        """
        return self.__analog_first_index

    @analog_first_index.setter
    def analog_first_index(self, value):
        """
        修改模拟通道起始索引
        """
        self.__analog_first_index = value

    @property
    def digital_first_index(self):
        """
        数字通道起始索引
        """
        return self.__digital_first_index

    @digital_first_index.setter
    def digital_first_index(self, value):
        """
        修改数字通道起始索引
        """
        self.__digital_first_index = value

    def to_string(self):
        """从对象生成字符串"""
        return (f'{self.station_name},{self.rec_dev_id},{str(self.rev_year)}\n' +
                f'{str(self.channel_total_num)},{str(self.analog_channel_num)}A,{str(self.digital_channel_num)}D')
