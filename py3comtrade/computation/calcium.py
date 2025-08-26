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
    dc_component: float = Field(default=None, description="直流分量")
    harmonics: dict = Field(default={}, description="各次谐波")

    def model_post_init(self, context: Any) -> None:
        """
        在模型初始化完成后自动执行
        """
        # 在这里执行初始化后的逻辑
        # 可以进行一些计算或设置
        self.calc_value()

    def calc_vector(self, k: int):
        """计算向量"""
        v = self.dft_rx(self.instant, k)
        self.vector = complex(round(v.real, 3), round(v.imag, 3))
        return self.vector

    def calc_angle(self):
        """计算角度"""
        self.angle = math_polar_rect.complex_to_polar(self.vector)[1]

    def calc_effective(self):
        """计算有效值"""
        self.effective = round(abs(self.vector), 3)

    def calc_dc_component(self):
        """计算直流分量"""
        signal_samples = np.array(self.instant)  # 例如，这是一个周期性的电流信号样本
        # 计算直流分量
        self.dc_component = float(np.round(np.mean(signal_samples), 3))

    def calc_harmonics(self, samp: int, hs=None):
        """计算谐波
        参数:
            samp(int) 采样频率,单位Hz
            hs(int) 计算谐波数组,默认计算2、3、5、9次谐波
        """
        if hs is None:
            hs = [2, 3, 5, 7, 9]
        n = len(self.instant)  # 数据点数
        f0 = samp / n  # 频率分辨率
        # fft计算
        fft_values = np.fft.fft(self.instant)
        fft_magnitude = np.abs(fft_values) / n  # 幅值归一化

        # 计算频率轴
        freqs = np.fft.fftfreq(n, 1 / samp)

        # 提取K次谐波
        for h in hs:  # 2~9 次谐波
            freq = h * f0  # 谐波频率
            idx = np.argmin(np.abs(freqs - freq))  # 找到最接近的频率点
            amplitude = fft_magnitude[idx] / np.sqrt(2) * 2  # 幅值
            self.harmonics[h] = {"frequency": freq, "amplitude": np.around(amplitude, 3)}

    def calc_value(self):
        self.calc_vector(k=1)
        self.calc_angle()
        self.calc_effective()
        self.calc_dc_component()

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
    cal.calc_harmonics(3200)
    print(cal.vector)
    print(cal.effective)
    print(cal.angle)
    print(cal.dc_component)
