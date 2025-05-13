#!/usr/bin/python3
# _*_ coding: utf-8 _*_
"""
@File    :   math_polar_rect.py
@Time    :   2024/06/17
@Version :   1.0
@Desc    :   阻抗值和灵敏角转换直角坐标
"""
import cmath
import math


def complex_to_polar(complex_num: complex) -> tuple[float, float]:
    """
    将复数转换为其极坐标形式，即返回幅值（阻抗）和角度（相位角）
    :param complex_num: 输入的复数
    :return: 返回模和角度
    """
    _magnitude, _radians = cmath.polar(complex_num)
    _degrees = round(math.degrees(_radians), 3)
    return _magnitude, _degrees


def polar_to_complex(_magnitude, _angle) -> complex:
    """
    将模和角度转换为实部和虚部形式
    :param _magnitude: 模
    :param _angle: 角度
    :return: 返回实部和虚部
    """
    angle_rad = math.radians(_angle)
    complex_num = cmath.rect(_magnitude, angle_rad)
    return complex_num


if __name__ == '__main__':
    # 示例：将模为5、角度为45度的复数转换为直角坐标形式
    magnitude = 3.7
    angle_deg = 69.5
    ptc = polar_to_complex(magnitude, angle_deg)
    print(f"实部{ptc.real}，虚部{ptc.imag}:")
    ctp = complex_to_polar(ptc)
    print(f"模{ctp[0]},角度{ctp[1]}")
