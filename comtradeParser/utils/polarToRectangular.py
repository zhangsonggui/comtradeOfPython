#!/usr/bin/python3
# _*_ coding: utf-8 _*_
#
# Copyright (C) 2024 - 2024 张松贵, Inc. All Rights Reserved
#
# @Time    : 2024/3/23 11:27
# @Author  : 张松贵
# @File    : ReadFaultFile.py
# @IDE     : PyCharm
import math


def polar_to_rectangular(_magnitude, _angle_deg):
    """
    将阻抗值和灵敏角转换为直角坐标形式
    :param _magnitude: 模
    :param _angle_deg: 角度
    :return: 返回实部和虚部
    """
    # 将角度转换为弧度
    angle_rad = math.radians(_angle_deg)

    # 计算实部和虚部
    _real = _magnitude * math.cos(angle_rad)
    _imag = _magnitude * math.sin(angle_rad)

    return _real, _imag


if __name__ == '__main__':
    # 示例：将模为5、角度为45度的复数转换为直角坐标形式
    magnitude = 3.7
    angle_deg = 69.5
    real, imag = polar_to_rectangular(magnitude, angle_deg)
    print("实部:", real)
    print("虚部:", imag)
