#!/usr/bin/env python
# -*- coding:utf-8 -*-
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
        self._samp = samp
        self._end_point = end_point
        self._cycle_sample_num = cycle_sample_num
        self._sample_num = sample_num
        self._start_point = start_point
        self._waste_time = waste_time
        self._end_time = end_time
        self._valuses = values

    def clear(self):
        self._samp = 0
        self._end_point = 0
        self._cycle_sample_num = 0
        self._sample_num = 0
        self._start_point = 0
        self._waste_time = 0
        self._end_time = 0
        self._valuses = []

    def to_string(self):
        return f'{str(self._samp)},{str(self._end_point)}'

    @property
    def samp(self):
        return self._samp

    @samp.setter
    def samp(self, value):
        """
        该段采样频率
        """
        self._samp = value

    @property
    def end_point(self):
        """
        该采样段结束位置
        """
        return self._end_point

    @end_point.setter
    def end_point(self, value):
        self._end_point = value

    @property
    def cycle_sample_num(self):
        """
        该采样段每周波采样点数
        """
        return self._cycle_sample_num

    @cycle_sample_num.setter
    def cycle_sample_num(self, value):
        self._cycle_sample_num = value

    @property
    def sample_num(self):
        """
        该采样段采样点数
        """
        return self._sample_num

    @sample_num.setter
    def sample_num(self, value):
        self._sample_num = value

    @property
    def start_point(self):
        """
        该采样段开始位置
        """
        return self._start_point

    @start_point.setter
    def start_point(self, value):
        self._start_point = value

    @property
    def waste_time(self):
        """
        该采样段用时
        """
        return self._waste_time

    @waste_time.setter
    def waste_time(self, value):
        self._waste_time = value

    @property
    def end_time(self):
        """
        该采样段结束时间
        """
        return self._end_time

    @end_time.setter
    def end_time(self, value):
        self._end_time = value

    @property
    def valuses(self):
        """
        该采样段原始采样值
        """
        return self._valuses

    @valuses.setter
    def valuses(self, value):
        self._valuses = value
