#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
from pydantic import Field, BaseModel

from py3comtrade.computation import math_polar_rect


class Calcium(BaseModel):
    instant: list[float] = Field(description="瞬时值数组")
    effective: float = Field(default=None, description="有效值")
    vector: complex = Field(default=None, description="相量值")
    angle: float = Field(default=None, description="相角值")

    def calc_vector(self, k: int):
        v = self.dft_rx(self.instant, k)
        self.vector = complex(round(v.real, 3), round(v.imag, 3))

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
