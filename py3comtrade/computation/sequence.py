#!/usr/bin/env python
# -*- coding: utf-8 -*-


import numpy as np
from pydantic import BaseModel,Field

class Sequence(BaseModel):
    positive:  float = Field(default=0.000, description="正序分量")
    negative: float = Field(default=0.000, description="负序分量")
    zero: float = Field(default=0.000, description="零序分量")

def phasor_to_sequence_by_rotate(pa: complex, pb: complex, pc: complex):
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

    positive = (pa + pb * np.exp(1j * 2 * np.pi / 3) + pc * np.exp(1j * 4 * np.pi / 3)) / 3 / np.sqrt(2.0)
    negative = (pa + pb * np.exp(-1j * 2 * np.pi / 3) + pc * np.exp(-1j * 4 * np.pi / 3)) / 3 / np.sqrt(2.0)
    zero = (pa + pb + pc) / 3 / np.sqrt(2.0)
    return Sequence(positive=positive, negative=negative, zero=zero)

def phasor_to_sequence_by_matrix(phasor_arr: np.ndarray):
    """
    将相量值转化为序分量，使用numpy矩阵
    :param phasor_arr:
    :return: 返回该组通道的序分量值,索引0为零序分量，1为正序分量，2为负序分量
    """
    if not all(isinstance(p, complex) for p in phasor_arr):
        raise ValueError("参数类型输入错误")
    a = complex(-0.5, np.sqrt(3.0) / 2.0)
    # 转换矩阵，零序、正序、负序
    trans_arr = np.array([[1, 1, 1], [1, a, a * a], [1, a * a, a]])
    order_arr = np.dot(trans_arr, phasor_arr) / 3
    order_arr = order_arr / np.sqrt(2.0)
    return Sequence(positive=order_arr[0], negative=order_arr[1], zero=order_arr[2])
