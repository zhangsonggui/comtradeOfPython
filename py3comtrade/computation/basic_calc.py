#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import List, Union

import numpy as np


def convert_primary_secondary(vs: Union[float, List[float]],
                              primary: float,
                              secondary: float,
                              input_primary: bool,
                              output_primary: bool) -> Union[float, List[float]]:
    """
    一次值与二次值之间的相互转换

    参数:
        vs(Union[float, List[float]]): 输入的瞬时值（单个值或数组）
        primary(float): 通道互感器变比一次系数
        secondary(float): 通道互感器变比二次系数
        input_primary(bool): 输入数值类型是一次值(True)或二次值(False)
        output_primary(bool): 输出数值类型是一次值(True)或二次值(False)

    返回值:
        Union[float, List[float]]: 转换后的值或数组
    """
    # 输入输出类型一致时，直接返回
    if input_primary == output_primary:
        return vs
    # 修正变比系数合法性检查
    if primary <= 0 or secondary <= 0:
        raise ValueError(f"变比系数不合法，输入的一次值为{primary}，输入的二次值为{secondary}")

    ratio = primary / secondary
    if output_primary:
        vs = vs if input_primary else [v * ratio for v in vs]
    else:
        vs = [v / ratio for v in vs] if input_primary else vs

    return vs


def convert_instant_raw(vs: List[Union[float, int]], a: float, b: float, input_type: str, output_type: str) -> list[
    Union[float, int]]:
    """
    原始采样值和有效值互转
    参数:
        vs: 输入值数组（原始采样值或瞬时值）
        a(float): 通道增益系数
        b(float): 通道偏移系数
    返回值:
        vs数组
    """
    if (it := input_type.upper()) == (ot := output_type.upper()):
        return vs
    if it == "RAW":
        # 原始采样值转换为瞬时值
        instants = np.asarray(vs) * a + b
        return instants.tolist()
    if it == "INSTANT":
        return np.round(vs).astype(int).tolist()


def convert_raw_instant(values: Union[List[int], List[Union[float, int]]],
                        a: float, b: float,
                        primary: float, secondary: float,
                        input_primary: bool = False,
                        output_primary: bool = False,
                        to_instant: bool = True) -> Union[List[float], List[int]]:
    """
    原始采样值与瞬时值双向转换函数

    参数:
        values: 输入值数组（原始采样值或瞬时值）
        a(float): 通道增益系数
        b(float): 通道偏移系数
        primary(float): 通道互感器变比一次系数
        secondary(float): 通道互感器变比二次系数
        input_primary(bool): 输入数值类型是一次值或二次值
        output_primary(bool): 输出数值类型是一次值或二次值
        to_instant(bool): 转换方向，True表示转换为瞬时值，False表示转换为原始采样值

    返回值:
        转换后的值数组
    """

    if to_instant:
        # 原始采样值转换为瞬时值
        instants = np.asarray(values) * a + b
        return convert_primary_secondary(instants, primary, secondary, input_primary, output_primary)
    else:
        instants = convert_primary_secondary(values, primary, secondary, input_primary, output_primary)
        raw_values = [(instant - b) / a for instant in instants]
        return np.round(raw_values).astype(int).tolist()
