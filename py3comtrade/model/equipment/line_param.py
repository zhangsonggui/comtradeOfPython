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

from pydantic import BaseModel, Field


class RX(BaseModel):
    r1: float = Field(default=0.0, description="正序电阻")
    x1: float = Field(default=0.0, description="正序电抗")
    r0: float = Field(default=0.0, description="零序电阻")
    x0: float = Field(default=0.0, description="零序电抗")

    def __str__(self):
        return f"<scl:RX r1={self.r1} x1={self.x1} r0={self.r0} x0={self.x0}/>"


class CG(BaseModel):
    c1: float = Field(default=0.0, description="正序电容")
    c0: float = Field(default=0.0, description="零序电容")
    g1: float = Field(default=0.0, description="正序电导")
    g0: float = Field(default=0.0, description="零序电导")

    def __str__(self):
        return f"<scl:CG c1={self.c1} c0={self.c0} g1={self.g1} g0={self.g0}/>"


class MR(BaseModel):
    idx: int = Field(default=0, description="母线索引号")
    mr0: float = Field(default=0.0, description="零序互感电阻")
    mx0: float = Field(default=0.0, description="零序互感电抗")

    def __str__(self):
        return f"<scl:MR idx={self.idx} mr0={self.mr0} mx0={self.mx0}/>"
