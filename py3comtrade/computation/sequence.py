#!/usr/bin/python3
# _*_ coding: utf-8 _*_
#
# Copyright (C) 2024 - 2024 张松贵, Inc. All Rights Reserved
#
# @Time    : 2024/3/23 11:27
# @Author  : 张松贵
# @File    : sequence.py
# @IDE     : PyCharm
import numpy as np


def compute_sequence_component(pa: complex, pb: complex, pc: complex):
    """
    将相分量转化为序分量,使用旋转B、C角度进行计算
    :param pa: A相相量值
    :param pb: B相相量值
    :param pc: C相相量值
    :return: 返回该组通道的序分量值,索引0为零序分量，1为正序分量，2为负序分量
    """
    # 参数校验
    if not all(isinstance(arg, complex) for arg in [pa, pb, pc]):
        raise ValueError("所有参数必须是复数类型")

    positive_sequence = (pa + pb * np.exp(1j * 2 * np.pi / 3) + pc * np.exp(1j * 4 * np.pi / 3)) / 3 / np.sqrt(2.0)
    negative_sequence = (pa + pb * np.exp(-1j * 2 * np.pi / 3) + pc * np.exp(-1j * 4 * np.pi / 3)) / 3 / np.sqrt(2.0)
    zero_sequence = (pa + pb + pc) / 3 / np.sqrt(2.0)
    return np.around([zero_sequence, positive_sequence, negative_sequence], 3)


def phasor_to_sequence(phasor_arr: np.ndarray):
    """
    将相量值转化为序分量，使用numpy矩阵
    :param phasor_arr:
    :return: 返回该组通道的序分量值,索引0为零序分量，1为正序分量，2为负序分量
    """
    if not all(isinstance(p, complex) for p in phasor_arr):
        raise ValueError("参数类型输入错误")
    a = complex(-0.5, np.sqrt(3.0) / 2.0)
    # phasor_arr = np.array([pa, pb, pc])
    # 转换矩阵，零序、正序、负序
    trans_arr = np.array([[1, 1, 1], [1, a, a * a], [1, a * a, a]])
    order_arr = np.dot(trans_arr, phasor_arr) / 3
    order_arr = order_arr / np.sqrt(2.0)
    return np.around(order_arr, 3)
