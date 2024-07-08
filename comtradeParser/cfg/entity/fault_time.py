#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :fault_time.py
# @Time      :2024/07/05 13:55:21
# @Author    :张松贵
from datetime import datetime

time_format = '%d/%m/%Y,%H:%M:%S.%f'  # 时间格式字符串


class FaultTime:
    """
    故障时间类
    """

    def __init__(self, start_time: datetime, trigger_time: datetime, zero_time: int):
        self.clear()
        self._start_time = start_time
        self._trigger_time = trigger_time
        self._zero_time = zero_time

    def clear(self):
        self._start_time = None
        self._trigger_time = None
        self._zero_time = 0

    @property
    def start_time(self):
        """
        波形开始时间
        """
        return self._start_time

    @start_time.setter
    def start_time(self, value):
        """
        修改波形开始时间
        """
        self._start_time = value

    @property
    def trigger_time(self):
        """
        故障开始时间
        """
        return self._trigger_time

    @trigger_time.setter
    def trigger_time(self, value):
        """
        修改故障开始时间
        """
        self._trigger_time = value

    @property
    def zero_time(self):
        """
        故障开始时间与波形开始时间的时间差
        """
        return self._zero_time

    @zero_time.setter
    def zero_time(self, value):
        """
        修改故障开始时间与波形开始时间的时间差
        """
        self._zero_time = value

    def to_string(self):
        return f"{self.start_time.strftime(time_format)}\n{self.trigger_time.strftime(time_format)}"
