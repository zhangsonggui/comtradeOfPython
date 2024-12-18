#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  Copyright (c) [2019] [name of copyright holder]
#  [py3comtrade] is licensed under Mulan PSL v2.
#  You can use this software according to the terms and conditions of the Mulan
#  PSL v2.
#  You may obtain a copy of Mulan PSL v2 at:
#           http://license.coscl.org.cn/MulanPSL2
#  THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY
#  KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
#  NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
#  See the Mulan PSL v2 for more details.

from typing import Union

from py3comtrade.model.base_channel import BaseChannel
from py3comtrade.model.type.analog_enum import ElectricalUnit, PsType
from py3comtrade.model.type.phase_code import PhaseCode


class Analog(BaseChannel):
    __unit: ElectricalUnit
    __a: float
    __b: float
    __skew: float
    __min_val: float
    __max_val: float
    __primary: float
    __secondary: float
    __ps: PsType
    __ratio: float

    def __init__(
            self,
            cfg_index: Union[int, str],
            name: str,
            phase: PhaseCode = PhaseCode.NO_PHASE,
            ccbm: str = "",
            unit: ElectricalUnit = ElectricalUnit.NO_UNIT,
            a: Union[float, str] = 0.0,
            b: Union[float, str] = 0.0,
            skew: Union[float, str] = 0.0,
            min_val: Union[float, str] = 0.0,
            max_val: Union[float, str] = 0.0,
            primary: Union[float, str] = 0.0,
            secondary: Union[float, str] = 0.0,
            ps: PsType = PsType.S,
    ):
        """
        模拟量通道类
        :param cfg_index: 模拟通道索引号，必选，数字，整数
        :param name: 通道标识符，必选，字符串，最大长度128个字符
        :param phase: 通道相别标识，可选，字母、数字，最小0个字符，最大长度2个字符
        :param ccbm: 被监视的电路元件，可选，字母、数字，最小0个字符，最大长度64个字符
        :param unit: 通道单位，如kV、V、kA、A RMS、 A Peak,必选，字母，最小长度1个
        :param a: 通道增益系数，必选，实数，数字，最小长度1个字符，最大长度32个字符，可以使用标准浮点标记法
        :param b: 通道偏移系数，必选，实数，数字，最小长度1个字符，最大长度32个字符，可以使用标准浮点标记法
        :param skew: 通道时滞（us），必选，实数，数字，最小长度1个字符，最大长度32个字符，可以使用标准浮点标记法
        :param min_val: 通道最小值，必选，实数，数字，最小长度1个字符，最大长度32个字符，可以使用标准浮点标记法
        :param max_val: 通道最大值，必选，实数，数字，最小长度1个字符，最大长度32个字符，可以使用标准浮点标记法
        :param primary: 通道互感器变比一次系数，必选，实数，数字，最小长度1个字符，最大长度32个字符
        :param secondary: 通道互感器变比二次系数，必选，实数，数字，最小长度1个字符，最大长度32个字符
        :param ps: 一次还是二次值标识,表明通道转换因子方程ax+b得到的值
        """
        super().__init__(cfg_index, name, phase, ccbm)
        self.__unit = unit
        self.__a = a if isinstance(a, float) else float(a)
        self.__b = b if isinstance(b, float) else float(b)
        self.__skew = skew if isinstance(skew, float) else float(skew)
        self.__min_val = min_val if isinstance(min_val, float) else float(min_val)
        self.__max_val = max_val if isinstance(max_val, float) else float(max_val)
        self.__primary = primary if isinstance(primary, float) else float(primary)
        self.__secondary = (
            secondary if isinstance(secondary, float) else float(secondary)
        )
        self.__ps = ps

    def clear(self) -> None:
        super().clear()

    def __str__(self):
        return (
                super().__str__()
                + f",{self.unit.get_code},{self.a},{self.b},{self.skew},{self.min_val},{self.max_val}"
                + f",{self.primary},{self.secondary},{self.ps.get_code}"
        )

    def __format_str_to_float(self, _str):
        if isinstance(self, float):
            return str
        if isinstance(_str, str):
            return float(str)
        return 0.0

    @property
    def unit(self) -> ElectricalUnit:
        return self.__unit

    @unit.setter
    def unit(self, value: str) -> None:
        self.__unit = ElectricalUnit.from_string(value)

    @property
    def a(self) -> float:
        return self.__a

    @a.setter
    def a(self, value) -> None:
        self.__a = value

    @property
    def b(self) -> float:
        return self.__b

    @b.setter
    def b(self, value) -> None:
        self.__b = value

    @property
    def skew(self) -> float:
        return self.__skew

    @skew.setter
    def skew(self, value) -> None:
        self.__skew = value

    @property
    def min_val(self) -> float:
        return self.__min_val

    @min_val.setter
    def min_val(self, value) -> None:
        self.__min_val = value

    @property
    def max_val(self) -> float:
        return self.__max_val

    @max_val.setter
    def max_val(self, value) -> None:
        self.__max_val = value

    @property
    def primary(self) -> float:
        return self.__primary

    @primary.setter
    def primary(self, value) -> None:
        self.__primary = value

    @property
    def secondary(self) -> float:
        return self.__secondary

    @secondary.setter
    def secondary(self, value) -> None:
        self.__secondary = value

    @property
    def ps(self) -> PsType:
        return self.__ps

    @ps.setter
    def ps(self, value: PsType) -> None:
        self.__ps = value

    @property
    def ratio(self) -> float:
        return self.__ratio

    @ratio.setter
    def ratio(self, value) -> None:
        self.__ratio = value
