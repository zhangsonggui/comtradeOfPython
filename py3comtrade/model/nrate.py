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
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from py3comtrade.model.exceptions import ComtradeDataFormatException


class Nrate(BaseModel):
    """
    每个采样段的采样率,采样序号
    """
    index: int = Field(default=0, description="采样段索引号")
    samp: int = Field(default=0, description="采样率, 单位为Hz")
    end_point: int = Field(default=0, description="该段最末的采样序号")
    start_point: int = Field(default=0, description="该段最开始的采样序号")
    cycle_point: float = Field(default=0, description="该采样段每周波包含的采样点数")
    count: int = Field(default=0, description="该采样段的采样点数")
    duration: float = Field(default=0, description="该采样段时间")
    end_time: float = Field(default=0, description="该段结束时间")

    def calc_count(self):
        self.count = self.end_point - self.start_point

    @field_validator('count')
    def validate_count(cls, v, info):
        values = info.data if hasattr(info, "data") else {}
        if 'end_point' in values and 'start_point' in values:
            return values['end_point'] - values['start_point']
        return v

    def clear(self):
        self.samp = 0
        self.end_point = 0
        self.start_point = 0

    @classmethod
    def from_string(cls, data_str: str) -> 'Nrate':
        if not data_str or not isinstance(data_str, str):
            raise ComtradeDataFormatException(f"输入字符串不能为空或不是字符串类型")
        samp, end_point = data_str.strip().split(",")
        return cls(samp=int(samp), end_point=int(end_point))

    @classmethod
    def from_dict(cls, data_dict: dict) -> Optional['Nrate']:
        index = data_dict.get("index", 0)
        samp = data_dict.get("samp", 0)
        start_point = data_dict.get("start_point", 0)
        end_point = data_dict.get("end_point", 0)
        cycle_point = data_dict.get("cycle_point", 0)
        count = data_dict.get("count", 0)
        duration = data_dict.get("duration", 0)
        end_time = data_dict.get("end_time", 0)

        if samp == 0 or end_point == 0:
            return None
        return cls(
            index=index,
            samp=samp,
            end_point=end_point,
            start_point=start_point,
            cycle_point=cycle_point,
            count=count,
            duration=duration,
            end_time=end_time
        )

    def __str__(self):
        return f"{self.samp},{self.end_point}"
