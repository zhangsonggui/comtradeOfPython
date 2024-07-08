#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (C) 2024 - 2024 张松贵, Inc. All Rights Reserved
# 解析开关量通道字符串为对象和根据开关量对象生成字符串
# @FileName  :digital_channel.py
# @Author    :张松贵
from comtradeParser.cfg.entity.digital_channel import DigitalChannel


def parse_str_digital_channel(channel_str):
    """
    从字符串解析开关量通道对象,通过采用逗号分割字符串
    :param channel_str: 开关量量通道字符串
    """
    channel_info = channel_str.split(',')
    return DigitalChannel(
        dn=int(channel_info[0]),
        chid=channel_info[1],
        ph=channel_info[2],
        ccbm=channel_info[3],
        y=channel_info[4].rstrip(),
    )


def generate_digital_channel_str(digital_channel_obj: DigitalChannel):
    """
    将开关量通道对象格式化为采用逗号分割的字符串
    :param digital_channel_obj: 开关量通道对象
    :return : 开关量通道字符串
    """
    return digital_channel_obj.to_string()
