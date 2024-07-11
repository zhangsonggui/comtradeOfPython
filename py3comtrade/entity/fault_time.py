#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (C) 2024 - 2024 张松贵, Inc. All Rights Reserved
# 故障时间类，包含录波开始时间，故障开始时间，故障开始时间与波形开始时间的时间差
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
        self.__start_time = start_time
        self.__trigger_time = trigger_time
        self.__zero_time = zero_time

    def clear(self):
        self.__start_time = None
        self.__trigger_time = None
        self.__zero_time = 0

    @property
    def start_time(self):
        """
        波形开始时间
        """
        return self.__start_time

    @start_time.setter
    def start_time(self, value):
        """
        修改波形开始时间
        """
        self.__start_time = value

    @property
    def trigger_time(self):
        """
        故障开始时间
        """
        return self.__trigger_time

    @trigger_time.setter
    def trigger_time(self, value):
        """
        修改故障开始时间
        """
        self.__trigger_time = value

    @property
    def zero_time(self):
        """
        故障开始时间与波形开始时间的时间差
        """
        return self.__zero_time

    @zero_time.setter
    def zero_time(self, value):
        """
        修改故障开始时间与波形开始时间的时间差
        """
        self.__zero_time = value

    def to_string(self):
        return f"{self.start_time.strftime(time_format)}\n{self.trigger_time.strftime(time_format)}"
