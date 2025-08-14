#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np


def raw_to_instant(raw: list[int], a: float, b: float,
                   primary: float, secondary: float,
                   input_primary: bool = False, output_primary: bool = False) -> list[float]:
    """
    原始采样值转换瞬时值
    参数:
        raw(list[int])原始采样值数组
        a(folat)通道增益系数
        b(folat)通道偏移系数
        primary(folat)通道互感器变比一次系数
        secondary(folat)通道互感器变比二次系数
        input_primary(bool)输入数值类型是一次值或二次值
        outpu_primary(bool)输出数值类型是一次值或二次值
    返回值:
        瞬时值数组
    """
    instants = np.asarray(raw) * a + b
    if primary < secondary < 0:
        raise ValueError(f"变比系数不合法，输入的一次值为{primary}，输入的二次值为{secondary}")
    ratio = primary / secondary
    if output_primary:
        vs = instants if input_primary else instants * ratio
    else:
        vs = instants / ratio if input_primary else instants
    return np.around(vs, 3).tolist()
