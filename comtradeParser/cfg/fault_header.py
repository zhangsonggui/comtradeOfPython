#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (C) 2024 - 2024 张松贵, Inc. All Rights Reserved
# 解析故障头字符串为对象和根据故障头对象生成故障头两行字符串
# @FileName  :fault_header.py
# @Author    :张松贵
from comtradeParser.cfg.entity.fault_header import FaultHeader


def parse_str_fault_header(header_str):
    """
    解析故障头两行数据，获取变电站、设备ID、录波版本、通道数量
    :param header_str: cfg文件头两行字符串
    """
    fs = header_str[0].rstrip()
    fs = fs.split(',')
    nums = header_str[1].rstrip()
    nums = nums.split(',')
    station_name = fs[0]
    rec_dev_id = fs[1]
    rev_year = 1991
    if len(fs) > 2:
        rev_year = int(fs[2])
    channel_total_num = int(nums[0])
    analog_channel_num = int(nums[1].strip('A'))
    digital_channel_num = int(nums[2].strip('D'))
    return FaultHeader(station_name=station_name, rec_dev_id=rec_dev_id, channel_total_num=channel_total_num,
                       analog_channel_num=analog_channel_num, digital_channel_num=digital_channel_num,
                       rev_year=rev_year)


def generate_fault_header_str(fault_header: FaultHeader):
    """
    根据故障头对象生成故障头两行字符串
    :param fault_header:故障头对象
    :return fault_header_str:故障头两行字符串
    """
    return fault_header.to_string()
