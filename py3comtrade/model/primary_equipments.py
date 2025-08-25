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

from pydantic import BaseModel, Field

from py3comtrade.model.type.analog_enum import CtDirection


class PrimaryEquipments(BaseModel):
    idx: int = Field(default=None, description="内部索引号")
    name: str = Field(default=None, description="名称，站内唯一")
    reference: Optional[str] = Field(default=None, description="IEC61850参引")


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


class ACVBranch(BaseModel):
    """交流电压通道"""
    ua_idx: int = Field(default=None, description="A相电压通道索引号")
    ub_idx: int = Field(default=None, description="B相电压通道索引号")
    uc_idx: int = Field(default=None, description="C相电压通道索引号")
    un_idx: int = Field(default=None, description="N相电压通道索引号")
    ul_idx: int = Field(default=None, description="L相电压通道索引号")

    def __str__(self):
        return f"<scl:ACVBranch ua_idx={self.ua_idx} ub_idx={self.ub_idx} uc_idx={self.uc_idx} un_idx={self.un_idx} ul_idx={self.ul_idx}/>"


class ACCBranch(BaseModel):
    idx: int = Field(default=None, description="分支序号")
    ia_idx: int = Field(default=None, description="A相电流通道索引号")
    ib_idx: int = Field(default=None, description="B相电流通道索引号")
    ic_idx: int = Field(default=None, description="C相电流通道索引号")
    in_idx: int = Field(default=None, description="N相电流通道索引号")
    dir: CtDirection = Field(default=CtDirection.POS, description="电流方向")

    def __str__(self):
        return f"<scl:ACC_Bran idx={self.idx} ia_idx={self.ia_idx} ib_idx={self.ib_idx} ic_idx={self.ic_idx} in_idx={self.in_idx} dir={self.dir.get_code()}/>"
