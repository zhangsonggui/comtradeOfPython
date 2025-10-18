#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  Copyright (c) [2019] [name of copyright holder]
#  [py3comtrade] is licensed under Mulan PSL v2.
#  You can use this software according to the terms and conditions of the Mulan
#  PSL v2.
#  You may obtain a copy of Mulan PSL v2 at:
#           http://license.coscl.org.cn/MulanPSL2
#  THIS SOFTWARE IS PROVIDED ON CFGAN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY
#  KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
#  NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
#  See the Mulan PSL v2 for more details.

from py3comtrade.model.channel.analog import Analog
from py3comtrade.model.exceptions import ComtradeDataFormatException
from py3comtrade.model.type.analog_enum import ElectricalUnit, PsType
from py3comtrade.model.type.phase_code import Phase


def analog_from_str(_an_str: str) -> Analog | None:
    """从字符串生成模拟量Analog对象"""
    # 去除字符串两端的空格，并按照逗号分割字符串
    _an_str = _an_str.strip().split(",")
    if len(_an_str) < 10:
        raise ComtradeDataFormatException(f"数据格式不正确")
    idx_cfg = int(_an_str[0])
    name = _an_str[1]
    if idx_cfg == 0 or name == "":
        return None
    # 创建Analog对象，传入参数
    analog = Analog(idx_cfg=idx_cfg,
                    name=name,
                    phase=Phase.from_string(_an_str[2], default=Phase.NO_PHASE),
                    ccbm="" if _an_str[3] == "null" else _an_str[3],
                    unit=ElectricalUnit.from_string(_an_str[4], default=ElectricalUnit.NONE),
                    a=float(_an_str[5]),
                    b=float(_an_str[6]),
                    skew=float(_an_str[7]) if _an_str[7] else 0.0,
                    min_val=float(_an_str[8]),
                    max_val=float(_an_str[9]))
    # 如果分割后的字符串长度大于11，则传入更多参数
    if len(_an_str) > 11:
        analog.primary = 1.0 if _an_str[10] in ["null", ""] else float(_an_str[10])
        analog.secondary = 1.0 if _an_str[11] in ["null", ""] else float(_an_str[11])
        analog.ps = PsType.from_string(_an_str[12], default=PsType.S)
        analog.ratio = analog.primary / analog.secondary if analog.secondary != 0 else 1.0
    # 返回Analog对象
    return analog


def analog_from_dict(_an_dict: dict) -> Analog | None:
    """从字典生成模拟量Analog对象"""
    idx_cfg = _an_dict.get("idx_cfg", 0)
    name = _an_dict.get("name", '')
    if idx_cfg == 0 or name == "":
        return None
    primary = float(_an_dict.get("primary", 1.0))
    secondary = float(_an_dict.get("secondary", 1.0))
    analog = Analog(
        index=_an_dict.get("index", 0),
        idx_cfg=idx_cfg,
        name=name,
        phase=Phase.from_string(_an_dict.get("phase", ''), default=Phase.NO_PHASE),
        ccbm=_an_dict.get("ccbm", ''),
        unit=ElectricalUnit.from_string(_an_dict.get("unit", ''), default=ElectricalUnit.NONE),
        a=float(_an_dict.get("a", 1.0)),
        b=float(_an_dict.get("b", 0.0)),
        min_val=float(_an_dict.get("min_val", 0.0)),
        max_val=float(_an_dict.get("max_val", 0.0)),
        primary=primary,
        secondary=secondary,
        ps=PsType.from_string(_an_dict.get("ps", "S"), default=PsType.S),
        ratio=primary / secondary if secondary != 0 else 1.0
    )
    analog.values = _an_dict.get("values", [])
    return analog
