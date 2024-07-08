#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (C) 2024 - 2024 张松贵, Inc. All Rights Reserved
# 解析采样段字符串为对象，根据采样段对象生成采样段字符串
# @FileName  :fault_nrate.py
# @Author    :张松贵
from comtradeParser.cfg.entity.fault_nrate import FaultNrate


def parse_str_nrate(nrate_str):
    """
    解析采样段字符串，使用逗号分割，获取该段采样频率采样点截止点
    :param nrate_str: 采样段字符串
    """
    nrate_info = nrate_str.split(',')
    return FaultNrate(samp=int(nrate_info[0]),
                      end_point=int(nrate_info[1].rstrip()))


def generate_nrate_str(nrate_obj: FaultNrate):
    """
    根据采样段对象生成使用逗号分割字符串
    :return :采样段字符串
    """
    return nrate_obj.to_string()
