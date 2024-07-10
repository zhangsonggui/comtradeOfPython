#!/usr/bin/python3
# _*_ coding: utf-8 _*_
"""
@File    :   polar_to_rectangular.py
@Time    :   2024/06/17
@Version :   1.0
@Desc    :   阻抗值和灵敏角转换直角坐标
"""
import math


class polarToRectangular:
    """
    将阻抗值和灵敏角转换为直角坐标形式
    """
    magnitude = 0
    angle_deg = 0

    def __init__(self, _magnitude, _angle_deg):
        self.clear()
        self.magnitude = _magnitude
        self.angle_deg = _angle_deg

    def clear(self):
        self.magnitude = 0
        self.angle_deg = 0

    def polar_to_rectangular(self):
        """
        将阻抗值和灵敏角转换为直角坐标形式
        :param _magnitude: 模
        :param _angle_deg: 角度
        :return: 返回实部和虚部
        """
        # 将角度转换为弧度
        angle_rad = math.radians(self.angle_deg)

        # 计算实部和虚部
        real = self.magnitude * math.cos(angle_rad)
        imag = self.angle_deg * math.sin(angle_rad)

        return real, imag


if __name__ == '__main__':
    # 示例：将模为5、角度为45度的复数转换为直角坐标形式
    magnitude = 3.7
    angle_deg = 69.5
    ptr = polarToRectangular(magnitude, angle_deg)
    real, imag = ptr.polar_to_rectangular()
    print("实部:", real)
    print("虚部:", imag)
