#!/usr/bin/python3
# _*_ coding: utf-8 _*_
"""
@File    :   math_polar_rect.py
@Time    :   2024/06/17
@Version :   1.0
@Desc    :   实现角度弧度转换和复数向量转换功能
"""
import cmath
import math


def degrees_to_radians(degrees: float) -> float:
    """
    将角度转换为弧度
    :param degrees: 角度值
    :return: 弧度值
    """
    return math.radians(degrees)


def radians_to_degrees(radians: float) -> float:
    """
    将弧度转换为角度
    :param radians: 弧度值
    :return: 角度值
    """
    return math.degrees(radians)


def complex_to_polar(complex_num: complex, use_degrees: bool = True) -> tuple[float, float]:
    """
    将复数转换为其极坐标形式，即返回幅值和角度（或弧度）
    :param complex_num: 输入的复数
    :param use_degrees: True返回角度，False返回弧度
    :return: 返回模和角度（或弧度）
    """
    magnitude, radians = cmath.polar(complex_num)
    if use_degrees:
        angle = round(radians_to_degrees(radians), 3)
    else:
        angle = radians
    return magnitude, angle


def polar_to_complex(magnitude: float, angle: float, use_degrees: bool = True) -> complex:
    """
    将模和角度（或弧度）转换为复数形式
    :param magnitude: 模
    :param angle: 角度或弧度值
    :param use_degrees: True表示angle为角度，False表示angle为弧度
    :return: 返回复数
    """
    if use_degrees:
        angle_rad = degrees_to_radians(angle)
    else:
        angle_rad = angle
    return cmath.rect(magnitude, angle_rad)


def complex_to_angle(complex_num: complex, use_degrees: bool = True) -> float:
    """
    将复数转换为角度或弧度
    :param complex_num: 输入的复数
    :param use_degrees: True返回角度，False返回弧度
    :return: 角度或弧度值
    """
    _, radians = cmath.polar(complex_num)
    if use_degrees:
        return round(radians_to_degrees(radians), 3)
    else:
        return radians


def complex_to_magnitude(complex_num: complex) -> float:
    """
    获取复数的模值（幅值）
    :param complex_num: 输入的复数
    :return: 模值
    """
    return round(abs(complex_num), 3)


if __name__ == '__main__':
    # 示例：角度和弧度互转
    angle = -95.654
    rad = degrees_to_radians(angle)
    print(f"{angle}度 = {rad}弧度")
    print(f"{rad}弧度 = {round(radians_to_degrees(rad), 3)}度")

    # 示例：将模为5、角度为45度的复数转换为直角坐标形式
    magnitude = 60.19
    angle_deg = -95.654
    ptc = polar_to_complex(magnitude, angle_deg)
    print(f"实部{ptc.real:.3f}，虚部{ptc.imag:.3f}")

    # (-5.93-59.897j)
    ctp = complex_to_polar(ptc)
    print(f"模{ctp[0]:.3f},角度{ctp[1]:.3f}")

    # 使用弧度
    angle_rad = degrees_to_radians(-95.654)
    ptc_rad = polar_to_complex(60.19, angle_rad, use_degrees=False)
    print(f"模60.19，角度{angle_rad}度的复数: 实部{ptc_rad.real:.3f}，虚部{ptc_rad.imag:.3f}")

    # 获取复数的角度和模值
    print(f"复数的角度(角度制): {complex_to_angle(ptc_rad, use_degrees=True)}")
    print(f"复数的角度(弧度制): {complex_to_angle(ptc_rad, use_degrees=False)}")
    print(f"复数的模值: {complex_to_magnitude(ptc_rad)}")
