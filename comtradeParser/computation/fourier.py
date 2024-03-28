#!/usr/bin/python3
# _*_ coding: utf-8 _*_
#
# Copyright (C) 2024 - 2024 张松贵, Inc. All Rights Reserved
#
# @Time    : 2024/3/23 11:27
# @Author  : 张松贵
# @File    : fourier.py
# @IDE     : PyCharm

import numpy as np


def dft_rx(vs: np.ndarray, num_samples: int, k: int) -> complex:
    """
    离散傅里叶变换实部和虚部
    @param vs: 瞬时值数组
    @param num_samples: 采样点数
    @param k: 获取的频率
    @return: 相量值，虚部和虚部元组
    """
    # 参数校验
    if not isinstance(vs, np.ndarray) or vs.ndim != 1:
        raise ValueError("输入的瞬时值数组vs必须是一维非空的numpy数组")
    if not isinstance(num_samples, int) or num_samples <= 0:
        raise ValueError("采样点数num_samples必须是正整数")
    if not isinstance(k, int) or k < 0 or k >= num_samples:
        raise ValueError("频率k必须是非负整数且小于采样点数")
    # 计算中点值，明确使用二进制除法
    m = num_samples // 2
    real = 0.0
    imag = 0.0
    for i in range(num_samples):
        real += vs[i] * np.sin(i * k * np.pi / m)
        imag += vs[i] * np.cos(i * k * np.pi / m)

    real /= m
    imag /= m
    return complex(real, imag)


def dft_exp_decay(vs: np.ndarray, sample_rate: int = None):
    """
    消除直流分量后返回对应通道的实部和虚部，需要1.5个周波的数据。
    1.[ (第三组点的实部+第二组点的虚部)/(第一组点的虚部+第二组点的实部) ] 的平方，把这个数记为a;
    2.通过第一步的运算结果a，求K1和K2，k1是 (第一组点的实部+第三组点的实部)/ (1+a):k2是(第一组点的虚部+第三组点的虚部) / (1+0).
    3.求修改后的基波分量实部和虚部，实部=第一组点的实部-k1: 虚部= 第二组点的虚部-k2
    :param vs: 瞬时值数组
    :param sample_rate: 采样频率
    :return: 返回一个二维数组，一维是通道列表，二维是实部虚部元祖
    """
    # 参数校验
    if not isinstance(vs, np.ndarray) or (vs.ndim != 1):
        raise ValueError("输入的瞬时值数组vs必须是一维非空的numpy数组。")
    if sample_rate is None:
        sample_rate = int(vs.shape[0] / 1.5)
    elif sample_rate <= 0:
        raise ValueError("采样频率sample_rate必须是正整数。")

    # 分割数组
    arr1 = vs[0:sample_rate]
    arr2 = vs[int(sample_rate / 4):int(sample_rate / 4 + sample_rate)]
    arr3 = vs[int(sample_rate / 2):]

    # 进行傅里叶计算，获取实部和虚部
    arr1_dft = dft_rx(arr1, sample_rate, 1)
    arr2_dft = dft_rx(arr2, sample_rate, 1)
    arr3_dft = dft_rx(arr3, sample_rate, 1)

    # 计算常数
    fz = arr3_dft.real + arr2_dft.imag
    fm = arr1_dft.imag + arr2_dft.real
    # 避免除以零
    if fm == 0:
        raise ValueError("计算中遇到除以零的情况。")

    # 计算系数
    a = np.square(fz / fm)
    k1 = (arr1_dft.real + arr3_dft.real) / (1 + a)
    k2 = (arr1_dft.imag + arr3_dft.imag) / (1 + a)
    # 计算过滤后的实部和虚部
    real = arr1_dft.real - k1
    imag = arr1_dft.imag - k2
    return complex(real, imag)


