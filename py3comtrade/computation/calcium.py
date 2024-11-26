#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np

from py3comtrade.computation.fourier import dft_rx
from py3comtrade.utils import math_polar_rect


class Calcium:
    __instants: np.ndarray  # 瞬时值数组
    __instant: float  # 当前采样位置的瞬时值
    __phasor: complex  # 相量值
    __angle: float  # 角度
    __effective: float  # 有效值

    def __init__(self, value: np.ndarray):
        self.clear()
        if isinstance(value, np.ndarray) and value.ndim == 1:
            self.__instants = value
            self.instant = value[0]
            self.phasor = dft_rx(value, value.shape[0], 1)
            self.angle = self.calc_angle(self.phasor)
            self.effective = self.calc_effective(self.phasor)
        else:
            raise ValueError("输入的瞬时值数组必须是一维非空的numpy数组")

    def clear(self):
        self.__instants = None
        self.__phasor = complex(0.0, 0.0)
        self.__angle = 0.0

    def calc_angle(self, phasor: complex):
        self.angle = math_polar_rect.complex_to_polar(phasor)[1]
        return self.angle

    def calc_effective(self, phasor: complex):
        self.effective = abs(phasor)
        return self.effective

    @property
    def instants(self) -> np.ndarray:
        return self.__instants

    @property
    def instant(self) -> float:
        return self.__instant

    @instant.setter
    def instant(self, value: float) -> None:
        self.__instant = value

    @property
    def phasor(self) -> complex:
        return np.around(self.__phasor, 3)

    @phasor.setter
    def phasor(self, value: complex) -> None:
        self.__phasor = value

    @property
    def angle(self) -> float:
        return np.around(self.__angle, 3)

    @angle.setter
    def angle(self, value: float) -> None:
        self.__angle = value

    @property
    def effective(self) -> float:
        return np.around(self.__effective, 3)

    @effective.setter
    def effective(self, value: float) -> None:
        self.__effective = value
