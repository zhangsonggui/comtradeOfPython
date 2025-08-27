#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from typing import List

from py3comtrade.model.type.analog_enum import ElectricalUnit, AnalogFlag

# 预编译名称启用规则正则表达式，提升性能
_NAME_ENABLE_COMPILED_PATTERNS: List[re.Pattern] = [
    # 电压相关模式
    re.compile(r'^电压\d+\s*[Uu][abc]$', re.IGNORECASE),  # 电压+数字+Ua/Ub/Uc
    re.compile(r'^电压\d+\s*[Uu]0$', re.IGNORECASE),  # 电压+数字+U0
    re.compile(r'^电压\d+\s*3[Uu]0$', re.IGNORECASE),  # 电压+数字+3U0
    # 电流相关模式
    re.compile(r'^电流\d+\s*[Ii][abc]$', re.IGNORECASE),  # 电流+数字+Ia/Ib/Ic
    re.compile(r'^电流\d+\s*[Ii]0$', re.IGNORECASE),  # 电流+数字+I0
    re.compile(r'^电流\d+\s*3[Ii]0$', re.IGNORECASE),  # 电流+数字+3I0
    # 带空格的模式
    re.compile(r'^电流\d+\s+[Ii][abc]$', re.IGNORECASE),  # 电流+数字+空格+Ia/Ib/Ic
    re.compile(r'^电流\d+\s+[Ii]0$', re.IGNORECASE),  # 电流+数字+空格+I0
    re.compile(r'^电流\d+\s+3[Ii]0$', re.IGNORECASE),  # 电流+数字+空格+3I0
    re.compile(r'^电压\d+\s+[Uu][abc]$', re.IGNORECASE),  # 电压+数字+空格+Ua/Ub/Uc
    re.compile(r'^电压\d+\s+[Uu]0$', re.IGNORECASE),  # 电压+数字+空格+U0
    re.compile(r'^电压\d+\s+3[Uu]0$', re.IGNORECASE),  # 电压+数字+空格+3U0
    # 更通用的模式
    re.compile(r'^电流\d*\s+[Ii][abc0]$', re.IGNORECASE),  # 电流+可选数字+空格+相别
    re.compile(r'^电流\d*\s+3[Ii]0$', re.IGNORECASE),  # 电流+可选数字+空格+3I0
    re.compile(r'^电压\d*\s+[Uu][abc0]$', re.IGNORECASE),  # 电压+可选数字+空格+相别
    re.compile(r'^电压\d*\s+3[Uu]0$', re.IGNORECASE),
    re.compile(r'^\s*\d+\s*$'),  # 纯数字或数字前后有空格
    re.compile(r'^模拟量$'),  # 仅模拟量三个字
    re.compile(r'^模拟量\s*\d*$'),  # 模拟量加数字或数字前有空格
    re.compile(r'^电压$'),  # 仅电压
    re.compile(r'^电压\s*\d+$'),  # 电压加数字
    re.compile(r'^电流\s*\d+$'),  # 电流加数字
    re.compile(r'^电流'),  # 以电流开头（注意：可能需要进一步限制）
    re.compile(r'^开关量\s*\d+$'),  # 开关量加数字
    re.compile(r'^状态量\s*\d+$'),  # 状态量加数字
]

# 预编译名称判断电压规则正则表达式，提升性能
_NAME_VOLTAGE_COMPILED_PATTERNS: List[re.Pattern] = [
    re.compile(r'.*电压.*_[Uu][abc]$', re.IGNORECASE),  # 包含"电压"和相别如_Ua
    re.compile(r'.*_[Uu][abc]$', re.IGNORECASE),  # 包含"电压"和相别如_Ua
    re.compile(r'.*[Uu][abc]$', re.IGNORECASE),  # 包含"电压"和相别如_Ua
    re.compile(r'.*[Uu]0$', re.IGNORECASE),  # 包含"电压"和相别如_Ua
    re.compile(r'.*电压.* [Uu][abc]$', re.IGNORECASE),  # 包含"电压"和相别如Ua
    re.compile(r'.*电压\d+\s*[Uu]0$', re.IGNORECASE),  # 包含"电压"和相别如Ua
    re.compile(r'.*电压.*[abc]相电压$', re.IGNORECASE),  # 包含"电压"和相别如A相电压
]

# 预编译名称判断电流规则正则表达式，提升性能
_NAME_CURRENT_COMPILED_PATTERNS: List[re.Pattern] = [
    re.compile(r'.*电流.*_[Ii][abc]$', re.IGNORECASE),  # 包含"电流"和相别如_Ia
    re.compile(r'.*电流.* [Ii][abc]$', re.IGNORECASE),  # 包含"电流"和相别如_Ia
    re.compile(r'.*_[Ii][abc]$', re.IGNORECASE),  # 包含"电流"和相别如_Ia
    re.compile(r'.*[Ii][abc]$', re.IGNORECASE),  # 包含"电流"和相别如_Ia
    re.compile(r'.*[Ii]0$', re.IGNORECASE),  # 包含"电流"和相别如_Ia
    re.compile(r'.*电流\d+\s.* [Ii][0]$', re.IGNORECASE),  # 包含"电流"和相别如_Ia
    re.compile(r'.*电流.*[Ii]相电流$', re.IGNORECASE),  # 包含"电流"和相别如A相电流
]

# 预编译高频规则正则表达式
_HF_COMPILED_PATTERN = [
    re.compile(r'.*高频$'),
    re.compile(r'.*高频通道'),
    re.compile(r'.*高频\s*\d'),
    re.compile(r'.*高频通道\s*\d')
]

# 预编译直流规则正则表达式
_DC_COMPILED_PATTERN = [
    re.compile(r'.*直流$'),
    re.compile(r'.*直流通道'),
    re.compile(r'.*直流电源')
]


def match_channel_name(_name_str: str) -> bool:
    """
    判断字符串是否符合指定规则

    参数:
        _name_str (str): 要匹配的字符串

    返回:
        bool: 符合规则返回 True，否则返回 False
    """
    if not isinstance(_name_str, str):
        return False

    return any(re.match(pattern, _name_str) for pattern in _NAME_ENABLE_COMPILED_PATTERNS)


def analog_channel_classification(_name_str: str, unit: ElectricalUnit = None) -> AnalogFlag | None:
    analog_flag = None
    is_voaltage = any(re.match(pattern, _name_str) for pattern in _NAME_VOLTAGE_COMPILED_PATTERNS)
    is_current = any(re.match(pattern, _name_str) for pattern in _NAME_CURRENT_COMPILED_PATTERNS)
    if unit == ElectricalUnit.V or unit == ElectricalUnit.KV or is_voaltage:
        analog_flag = AnalogFlag.ACV
    elif unit == ElectricalUnit.A or unit == ElectricalUnit.KA or is_current:
        analog_flag = AnalogFlag.ACC

    if any(re.match(pattern, _name_str) for pattern in _HF_COMPILED_PATTERN) and is_voaltage:
        analog_flag = AnalogFlag.DCV
    elif any(re.match(pattern, _name_str) for pattern in _DC_COMPILED_PATTERN) and is_current:
        analog_flag = AnalogFlag.DCC
    elif analog_flag is None:
        analog_flag = AnalogFlag.DCV

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
        "",  # 空字符串
        "电流10 Ia",
        "电流14 I0",
        "电压5 Ua",
        "电压3 3U0",
        "电流1 Ib",
        "电流2 Ic",
        "电压1 Ub",
        "电压2 Uc"
    ]

    print("使用match_channel__name函数:")
    for name_str in test__name_strs:
        result = match_channel_name(name_str)
        print(f"'{name_str}': {result}")
