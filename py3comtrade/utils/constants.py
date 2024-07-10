#!/usr/bin/python3
# _*_ coding: utf-8 _*_
#
# Copyright (C) 2024 - 2024 张松贵, Inc. All Rights Reserved
#
# @Time    : 2024/3/23 11:27
# @Author  : 张松贵
# @File    : constants.py
# @IDE     : PyCharm
# 定义通道关键字，用于屏蔽不需要解析的通道
NAME_MASKEY = ["高频", "模拟量", "高抗", "电抗", "单量", "母联", "分段", "开关量", "电压", "电流"]
# 定义监视元件关键字，用于检测元件是否有效
CCBM_MASKEY = ["", "kV", "KV", "kA", "KA"]
# 电压单位
VOLTAGE_UNIT = ["kV", "KV", "v", "V"]
# 电流单位
CURRENT_UNIT = ["kA", "KA", "a", "A"]
# 一次值标志
PAIMARY_SIGN = ['P', 'p']
