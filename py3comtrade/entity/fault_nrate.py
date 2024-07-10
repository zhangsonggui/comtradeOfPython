#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (C) 2024 - 2024 张松贵, Inc. All Rights Reserved
# 故障采样段信息类，包含该段采样频率、采样点数、采样点开始位置、采样点结束位置、采样点用时、采样点结束位置、采样点原始采样值
# @FileName  :fault_nrate.py
# @Time      :2024/07/05 13:56:30
# @Author    :张松贵

class FaultNrate:
    def __init__(self, samp: int, end_point: int, cycle_sample_num: int = None, sample_num: int = None,
                 start_point: int = None, waste_time: int = None, end_time: int = None, values: list = None):
        """
        :param samp: 该段采样频率
        :param end_point: 该采样段结束位置
        :param cycle_sample_num: 该采样段每周波采样点数
        :param sample_num: 该采样段采样点数
        :param start_point: 该采样段开始位置
        :param waste_time: 该采样段用时
        :param end_time: 该采样段结束时间
        :param values: 该采样段原始采样值
        """
        self.clear()
        self.__samp = samp
        self.__end_point = end_point
        self.__cycle_sample_num = cycle_sample_num
        self.__sample_num = sample_num
        self.__start_point = start_point
        self.__waste_time = waste_time
        self.__end_time = end_time
        self.__values = values

    def clear(self):
        self.__samp = 0
        self.__end_point = 0
        self.__cycle_sample_num = 0
        self.__sample_num = 0
        self.__start_point = 0
        self.__waste_time = 0
        self.__end_time = 0
        self.__values = []

    def to_string(self):
        return f'{str(self.__samp)},{str(self.__end_point)}'

    @property
    def samp(self):
        return self.__samp

    @samp.setter
    def samp(self, value):
        """
        该段采样频率
        """
        self.__samp = value

    @property
    def end_point(self):
        """
        该采样段结束位置
        """
        return self.__end_point

    @end_point.setter
    def end_point(self, value):
        self.__end_point = value

    @property
    def cycle_sample_num(self):
        """
        该采样段每周波采样点数
        """
        return self.__cycle_sample_num

    @cycle_sample_num.setter
    def cycle_sample_num(self, value):
        self.__cycle_sample_num = value

    @property
    def sample_num(self):
        """
        该采样段采样点数
        """
        return self.__sample_num

    @sample_num.setter
    def sample_num(self, value):
        self.__sample_num = value

    @property
    def start_point(self):
        """
        该采样段开始位置
        """
        return self.__start_point

    @start_point.setter
    def start_point(self, value):
        self.__start_point = value

    @property
    def waste_time(self):
        """
        该采样段用时
        """
        return self.__waste_time

    @waste_time.setter
    def waste_time(self, value):
        self.__waste_time = value

    @property
    def end_time(self):
        """
        该采样段结束时间
        """
        return self.__end_time

    @end_time.setter
    def end_time(self, value):
        self.__end_time = value

    @property
    def values(self):
        """
        该采样段原始采样值
        """
        return self.__values

    @values.setter
    def values(self, value):
        self.__values = value
