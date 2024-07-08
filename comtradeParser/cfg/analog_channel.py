#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 - 2024 张松贵, Inc. All Rights Reserved
# 解析模拟量通道字符串为对象和根据模拟量对象生成字符串
# @FileName  : analog_channel.py
# @Author    :张松贵
from comtradeParser.cfg.entity.analog_channel import AnalogChannel


def parse_str_analog_channel(channel_str):
    """
    从字符串解析模拟量通道对象,通过采用逗号分割字符串当不足10个元素时设置默认值格式化为b1999版本
    :param channel_str: 模拟量通道字符串
    """
    channel_info = channel_str.split(',')
    ps = channel_info[12].rstrip() if len(channel_info) > 12 else "S"
    uu = channel_info[4].upper()
    if uu == ['KV', 'KA'] and ps != 'P':
        ps = 'P'
    return AnalogChannel(
        an=int(channel_info[0]),
        chid=channel_info[1],
        ph=channel_info[2],
        ccbm=channel_info[3],
        uu=channel_info[4],
        a=float(channel_info[5]),
        b=float(channel_info[6]),
        skew=float(channel_info[7]),
        min_val=int(channel_info[8]),
        max_val=int(channel_info[9]),
        primary=float(channel_info[10]) if len(channel_info) > 10 else 1.0,
        secondary=float(channel_info[11]) if len(channel_info) > 11 else 1.0,
        ps=ps
    )


def generate_analog_channel_str(analog_channel_obj: AnalogChannel):
    """
    将模拟量通道对象格式化为采用逗号分割的字符串
    :param analog_channel_obj: 模拟量通道对象
    :return : 模拟量通道字符串
    """
    return analog_channel_obj.to_string()
