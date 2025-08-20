#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

from py3comtrade.model.type import ElectricalUnit, AnalogFlag


def match_channel_name(_name_str: str) -> bool:
    """
    判断字符串是否符合指定规则

    参数:
        _name_str (str): 要匹配的字符串

    返回:
        bool: 符合规则返回 True，否则返回 False
    """
    patterns = [
        r'^\s*\d+\s*$',  # 纯数字或数字前后有空格
        r'^模拟量$',  # 仅模拟量三个字
        r'^模拟量\s*\d*$',  # 模拟量加数字或数字前有空格
        r'^电压\s*\d+$',  # 电压加数字或数字前有空格
        r'^电流\s*\d+$',  # 电流加数字或数字前有空格
        r'^开关量\s*\d+$',  # 开关量加数字或数字前有空格
        r'^状态量\s*\d+$'  # 状态量加数字或数字前有空格
    ]

    return any(re.match(pattern, _name_str) for pattern in patterns)


def analog_channel_classification(_name_str: str, unit: ElectricalUnit = None) -> AnalogFlag | None:
    analog_flag = None
    if unit == ElectricalUnit.V or unit == ElectricalUnit.KV:
        analog_flag = AnalogFlag.ACV
    elif unit == ElectricalUnit.A or unit == ElectricalUnit.KA:
        analog_flag = AnalogFlag.ACC

    pattern = r'^(高频$|高频通道$|高频\s*\d+$|高频通道\s*\d+$)'
    if bool(re.match(pattern, _name_str)) and _name_str in ["电压", "U"]:
        analog_flag = AnalogFlag.DCV
    pattern = r'^(直流$|直流电源)'
    if bool(re.match(pattern, _name_str)) and _name_str in ["电流", ]:
        analog_flag = AnalogFlag.DCC

    return analog_flag


# 示例用法
if __name__ == "__main__":
    test__name_strs = [
        "123",  # 纯数字
        " 123 ",  # 数字前后有空格
        "模拟量",  # 仅模拟量
        "模拟量1",  # 模拟量加数字
        "模拟量 1",  # 模拟量加空格和数字
        "电压220",  # 电压加数字
        "电压 220",  # 电压加空格和数字
        "电流5",  # 电流加数字
        "电流 5",  # 电流加空格和数字
        "开关量1",  # 开关量加数字
        "开关量 1",  # 开关量加空格和数字
        "状态量2",  # 状态量加数字
        "状态量 2",  # 状态量加空格和数字
        "频率量",  # 不符合规则
        "模拟量abc",  # 不符合规则
        "abc123",  # 不符合规则
        ""  # 空字符串
    ]

    print("使用match_channel__name函数:")
    for name_str in test__name_strs:
        result = match_channel_name(name_str)
        print(f"'{name_str}': {result}")
