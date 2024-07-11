#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (C) 2024 - 2024 张松贵, Inc. All Rights Reserved
# 解析时间字符串为对象，根据时间对象生成字符串
# @FileName  :fault_time.py
# @Author    :张松贵
from datetime import datetime

from py3comtrade.entity.fault_time import FaultTime

time_format = '%d/%m/%Y,%H:%M:%S.%f'  # 时间格式字符串


def parse_str_fault_time(fault_time_strs):
    """
    解析时间字符串为对象，包含采样开始时间和故障时间
    :param fault_time_strs: 时间格式为天/月/年，时:分:秒.微秒
    """
    try:
        str_time = fault_time_strs[0].strip()
        start_time = datetime.strptime(str_time, time_format)
        str_time = fault_time_strs[1].strip()
        trigger_time = datetime.strptime(str_time, time_format)
    except ValueError as e:
        raise ValueError(f"时间格式错误:{e}")
    zero_time = (trigger_time - start_time).microseconds
    return FaultTime(start_time=start_time,
                     trigger_time=trigger_time,
                     zero_time=zero_time)


def generate_fault_time_str(fault_time_obj: FaultTime):
    """
    根据时间对象生成字符串
    :return 时间字符串时间格式为天/月/年，时:分:秒.微秒
    """
    return fault_time_obj.to_string()
