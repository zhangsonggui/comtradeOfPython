#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from typing import List

import pandas as pd

from py3comtrade.model.type.analog_enum import AnalogFlag, ElectricalUnit
from py3comtrade.model.type.phase_code import Phase

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
# 预编译相别规则正则表达式
_PHASE_A_COMPILED_PATTERNS: List[re.Pattern] = [
    re.compile(r'.*[UuIi][Aa]$', re.IGNORECASE),  # Ua, Ia结尾
    re.compile(r'.*[UuIi]0$', re.IGNORECASE),  # U0, I0结尾（作为A相处理）
    re.compile(r'.*[Aa]相[电电压流]+$', re.IGNORECASE),  # A相电压, A相电流
]

_PHASE_B_COMPILED_PATTERNS: List[re.Pattern] = [
    re.compile(r'.*[UuIi][Bb]$', re.IGNORECASE),  # Ub, Ib结尾
    re.compile(r'.*[Bb]相[电电压流]+$', re.IGNORECASE),  # B相电压, B相电流
]

_PHASE_C_COMPILED_PATTERNS: List[re.Pattern] = [
    re.compile(r'.*[UuIi][Cc]$', re.IGNORECASE),  # Uc, Ic结尾
    re.compile(r'.*[Cc]相[电电压流]+$', re.IGNORECASE),  # C相电压, C相电流
]

_PHASE_N_COMPILED_PATTERNS: List[re.Pattern] = [
    re.compile(r'.*3[UuIi]0$', re.IGNORECASE),  # 3U0, 3I0
    re.compile(r'.*[UuIi]0$', re.IGNORECASE),  # U0, I0
    re.compile(r'.*[Nn]相[电电压流]+$', re.IGNORECASE),  # N相电压, N相电流
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


def parser_phase(_name_str: str):
    _phase = Phase.NO_PHASE
    if any(re.match(pattern, _name_str) for pattern in _PHASE_A_COMPILED_PATTERNS):
        _phase = Phase.A_PHASE
    if any(re.match(pattern, _name_str) for pattern in _PHASE_B_COMPILED_PATTERNS):
        _phase = Phase.B_PHASE
    if any(re.match(pattern, _name_str) for pattern in _PHASE_C_COMPILED_PATTERNS):
        _phase = Phase.C_PHASE
    if any(re.match(pattern, _name_str) for pattern in _PHASE_N_COMPILED_PATTERNS):
        _phase = Phase.N_PHASE
    return _phase


# 示例用法
if __name__ == "__main__":
    df = pd.read_csv(r"D:\codeArea\gitee\comtradeOfPython\通道名称汇总.csv", encoding='gbk')
    print(f"开始解析故障相别")
    ok = 0
    fail = 0
    for index, row in df.iterrows():
        name_str = row.iloc[0]  # 使用 iloc[0] 获取第一列的值
        phase = parser_phase(name_str)
        phase_ori = row.iloc[1]
        if phase_ori != phase.value:
            fail += 1
            print(f"行 {index}: 第一列的值 = {name_str},识别相别:{phase.value},原始相别{phase_ori}")
        else:
            ok += 1
    print(f"故障相别解析完毕")
    # print("使用match_channel__name函数:")
    # for name_str in test__name_strs:
    #     result = match_channel_name(name_str)
    #     print(f"'{name_str}': {result}")
