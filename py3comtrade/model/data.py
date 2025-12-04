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
import numpy as np
from pydantic import BaseModel, Field, ConfigDict


class Data(BaseModel):
    size: int = Field(default=0, description="文件大小")
    sample_time: np.ndarray = Field(default=None, description="采样时间")
    analog_value: np.ndarray = Field(default=None, description="模拟量值")
    digital_value: np.ndarray = Field(default=None, description="开关量值")

    model_config = ConfigDict(arbitrary_types_allowed=True)

class DataFile(BaseModel):
    sample_points:list[int] = Field(description="采样点")
    sample_times:list[int] = Field(description="采样时间")
    analog_values:list[list[float]] = Field(description="模拟量值")
    digital_values:list[list[int]] = Field(description="开关量值")
