#!/usr/bin/env python
# -*- coding: utf- 8 -*-
from typing import Any

import numpy as np
from pydantic import Field, BaseModel

from py3comtrade.computation import math_polar_rect


class Calcium(BaseModel):
    instant: list[float] = Field(description="瞬时值数组")
    effective: float = Field(default=None, description="有效值")
    vector: complex = Field(default=None, description="相量值")
    angle: float = Field(default=None, description="相角值")

    def model_post_init(self, context: Any) -> None:
        """
        在模型初始化完成后自动执行
        """
        # 在这里执行初始化后的逻辑
        # 可以进行一些计算或设置
        self.calc_value()

    def calc_vector(self, k: int):
        v = self.dft_rx(self.instant, k)
        self.vector = complex(round(v.real, 3), round(v.imag, 3))
        return self.vector

    def calc_angle(self):
        self.angle = math_polar_rect.complex_to_polar(self.vector)[1]

    def calc_effective(self):
        self.effective = round(abs(self.vector), 3)

    def calc_value(self):
        self.calc_vector(k=1)
        self.calc_angle()
        self.calc_effective()

    @staticmethod
    def dft_rx(vs: list[float], k: int) -> complex:
        """
        离散傅里叶变换实部和虚部
        @param vs: 瞬时值数组
        @param k: 获取的频率
        @return: 相量值，虚部和虚部元组
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


if __name__ == '__main__':
    ssz = [-84.691, -85.198, -84.824, -83.715, -81.708, -78.662, -75.062, -70.744, -65.683, -60.217, -54.29,
           -47.527, -40.1, -32.525, -24.521, -16.524, -8.403, 0.141, 8.59, 16.805, 24.615, 32.291, 39.928,
           47.253, 54.063, 60.256, 65.621, 70.564, 74.836, 78.631, 81.466, 83.426, 84.73, 85.128, 84.816, 83.613,
           81.661, 78.709, 75.007, 70.744, 65.73, 60.186, 54.352, 47.48, 40.163, 32.564, 24.537, 16.657, 8.395,
           -0.031, -8.504, -16.798, -24.622, -32.33, -39.866, -47.207, -54.063, -60.186, -65.621, -70.564, -74.812,
           -78.646, -81.497, -83.394]
    cal = Calcium(instant=ssz)
    print(cal.vector)
    print(cal.effective)
    print(cal.angle)
