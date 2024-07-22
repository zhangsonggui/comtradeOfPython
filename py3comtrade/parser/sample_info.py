#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (C) 2024 - 2024 张松贵, Inc. All Rights Reserved
# 解析采样频率开始行到结束的字符串，解析为采样信息对象，根据采样信息对象生成字符串
# @FileName  :sample_info.py
# @Author    :张松贵
from py3comtrade.entity.fault_nrate import FaultNrate
from py3comtrade.entity.sample_info import SampleInfo
from py3comtrade.parser.fault_nrate import parse_str_nrate
from py3comtrade.parser.fault_time import parse_str_fault_time


def parse_str_sample_info(sample_info):
    """
    解析采样频率开始行到结束的字符串，解析为采样信息对象
    :param sample_info:采样段数开始行到结束的字符串
    """
    lf = int(sample_info[0].rstrip())
    nrate_num = int(sample_info[1].rstrip())

    nrates = []  # 各采样段的采样率原始信息
    # 循环实例化各采样段的采样率信息
    for i in range(2, nrate_num + 2):
        nrates.append(parse_str_nrate(sample_info[i].rstrip()))

    # 计算各采样段采样率及采样点信息
    for i in range(0, nrate_num):
        nrate: FaultNrate = nrates[i]
        # 每个周波采多少个点数
        nrate.cycle_sample_num = nrate.samp / lf
        # 每段包含多少个采样点数
        nrate.sample_num = nrate.end_point if i == 0 else nrate.end_point - nrates[i - 1].end_point
        # 每段开始的采样点号
        nrate.start_point = 0 if i == 0 else nrates[i - 1].end_point
        # 计算采样段一共用了多少时间
        nrate.waste_time = nrate.sample_num / nrate.cycle_sample_num * 20
        # 计算每个采样段结束是的时间
        nrate.end_time = nrate.waste_time if i == 0 else nrate.waste_time + nrates[i - 1].end_time
    sample_total_num = nrates[-1].end_point
    fault_time = None
    ft = ''
    timemult = 1.0
    # 实例化故障时间和采样格式
    if len(sample_info) >= nrate_num + 4:
        fault_time = parse_str_fault_time(
            sample_info[nrate_num + 2:nrate_num + 4])
        ft = sample_info[nrate_num + 4].strip('\n').upper()
    bit_width = 2
    if ft in ['BINARY32', 'FLOAT32']:
        bit_width = 4
    if len(sample_info) >= nrate_num + 5:
        timemult = parse_str_timemult(sample_info[nrate_num + 4])

    return SampleInfo(lf=lf, nrate_num=nrate_num, sample_total_num=sample_total_num, ft=ft, timemult=timemult,
                      nrates=nrates, fault_time=fault_time, bit_width=bit_width)


def parse_str_timemult(timemult_str):
    """解析倍频因数"""
    try:
        timemult = float(timemult_str.strip('\n'))
    except ValueError:
        timemult = 1.0
    return timemult


def generate_sample_info_str(sample_info_obj):
    """
    直接使用对象的方法生成字符串
    """
    return sample_info_obj.to_string()
