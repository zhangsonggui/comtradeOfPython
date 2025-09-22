#!/usr/bin/env python
# -*- coding: utf- 8 -*-
from typing import Any, Dict

import numpy as np
from pydantic import Field, BaseModel

from py3comtrade.computation.fourier import compute_dft_component, fft_component
from py3comtrade.computation.math_polar_rect import complex_to_polar, complex_to_magnitude
from py3comtrade.model.harmonic import Harmonic


class Calcium(BaseModel):
    instant: list[float] = Field(description="瞬时值数组")
    effective: float = Field(default=None, description="有效值")
    vector: complex = Field(default=None, description="相量值")
    angle: float = Field(default=None, description="相角值")
    dc_component: float = Field(default=None, description="直流分量")
    harmonics: Dict[int, Harmonic] = Field(default={}, description="各次谐波")

    def model_post_init(self, context: Any) -> None:
        """
        在模型初始化完成后自动执行
        """
        # 在这里执行初始化后的逻辑
        self.calc_vector()
        self.calc_angle()
        self.calc_effective()
        self.calc_dc_component()
        self.calc_harmonics()

    def calc_vector(self, k: int = 1):
        """计算向量"""
        dft = compute_dft_component(self.instant, k)
        self.vector = complex(round(dft.real, 3), round(dft.imag, 3))
        return self.vector

    def calc_angle(self):
        """计算角度"""
        self.angle = complex_to_polar(self.vector)[1]

    def calc_effective(self):
        """计算有效值"""
        self.effective = complex_to_magnitude(self.vector)

    def calc_dc_component(self):
        """计算直流分量"""
        signal_samples = np.array(self.instant)  # 例如，这是一个周期性的电流信号样本
        # 计算直流分量
        self.dc_component = float(np.round(np.mean(signal_samples), 3))
        return self.dc_component

    def calc_harmonics(self, hs: list = None):
        """计算谐波,使用numpy中的fft
        也可使用compute_dft_component函数实现相关计算
        参数:
            hs(int) 计算谐波数组,默认计算2、3、5、9次谐波
        """
        hs = [2, 3, 5, 7, 9] if hs is None else hs
        self.harmonics = fft_component(self.instant, hs)
        return self.harmonics


if __name__ == '__main__':
    ssz = [-84.691, -85.198, -84.824, -83.715, -81.708, -78.662, -75.062, -70.744, -65.683, -60.217, -54.29,
           -47.527, -40.1, -32.525, -24.521, -16.524, -8.403, 0.141, 8.59, 16.805, 24.615, 32.291, 39.928,
           47.253, 54.063, 60.256, 65.621, 70.564, 74.836, 78.631, 81.466, 83.426, 84.73, 85.128, 84.816, 83.613,
           81.661, 78.709, 75.007, 70.744, 65.73, 60.186, 54.352, 47.48, 40.163, 32.564, 24.537, 16.657, 8.395,
           -0.031, -8.504, -16.798, -24.622, -32.33, -39.866, -47.207, -54.063, -60.186, -65.621, -70.564, -74.812,
           -78.646, -81.497, -83.394]
    cal = Calcium(instant=ssz)
    cal.calc_harmonics([0, 1, 2, 3, 5, 7, 9])
    print(f"向量值:{cal.vector}")
    print(f"有效值:{cal.effective}")
    print(f"角度:{cal.angle}")
    print(f"直流分量:{cal.dc_component}")
    # print(f"谐波:{cal.harmonics}")
    for k, h in cal.harmonics.items():
        print(f"{k}次谐波:{h.amplitude}")
