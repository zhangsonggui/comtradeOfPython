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

from py3comtrade.model.harmonic import Harmonic


def compute_dft_component(vs: list[float], k: int = 1) -> complex:
    """
    实现离散傅里叶变换（DFT）的核心计算逻辑
    参数:
        vs(list[float]): 瞬时值数组
        k(int): 待计算的频率
    返回值:
        相量值，虚部和虚部元组
    """
    # 参数校验
    size = len(vs)
    if not isinstance(vs, list) and size > 2:
        raise ValueError(f"输入的瞬时值数组长度要大于2，现在长度为{size}")
    if not isinstance(k, int) or k < 0 or k >= size:
        raise ValueError(f"频率k必须是非负整数且小于采样点数")
    # 计算中点值，明确使用二进制除法
    m = size // 2
    real = 0.0
    imag = 0.0
    for i in range(size):
        real += vs[i] * np.sin(i * k * np.pi / m)
        imag += vs[i] * np.cos(i * k * np.pi / m)

    real /= m
    imag /= m
    return complex(real, imag) / np.sqrt(2)


def fft_component(vs: list[float], k: int = None) -> dict[int, Harmonic]:
    """
    使用numpy中fft实现离散傅里叶变换的核心计算逻辑
    参数:
        vs(list[float]): 瞬时值数组
        k(int): 待计算的频率
    返回值:
        字典,key为谐波次数,value为谐波结果Harmonic
    """
    # 参数校验
    F0 = 50
    size = len(vs)
    samp = F0 * size
    if not isinstance(vs, list) and size > 2:
        raise ValueError(f"输入的瞬时值数组长度要大于2，现在长度为{size}")
    if k is None:
        k = [2, 3, 5, 7, 9]
    # fft计算
    fft_values = np.fft.fft(vs)
    fft_magnitude = np.abs(fft_values) / size  # 幅值归一化

    # 计算频率轴
    freqs = np.fft.fftfreq(size, 1 / samp)

    # 提取K次谐波
    harmonics = {}
    for h in k:  # 2~9 次谐波
        freq = h * F0  # 谐波频率
        idx = np.argmin(np.abs(freqs - freq))  # 找到最接近的频率点
        amplitude = fft_magnitude[idx] / np.sqrt(2) * 2  # 幅值
        harmonics[h] = Harmonic(frequency=freq, amplitude=float(np.around(amplitude, 3)))

    return harmonics


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
    arr1_dft = compute_dft_component(arr1.tolist())
    arr2_dft = compute_dft_component(arr2.tolist())
    arr3_dft = compute_dft_component(arr3.tolist())

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
