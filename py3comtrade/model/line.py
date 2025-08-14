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
from typing import List

from pydantic import Field

from .channel import ChannelIdx
from .primary_equipments import ACCBranch, CG, MR, PrimaryEquipments, RX
from .type import BranNum


class Line(PrimaryEquipments):
    bus_idx: int = Field(..., description="母线索引号")
    v_rtg: float = Field(default=0.0, description="一次额定电压")
    a_rtg: float = Field(default=0.0, description="一次额定电流")
    a_rtg_snd: float = Field(default=1.0, description="二次额定电流")
    lin_len: float = Field(default=0.0, description="线路长度")
    bran_num: BranNum = Field(default=BranNum.B1, description="线路分段数")
    line_uuid: str = Field(default="", description="线路标识")
    rx: RX = Field(default=RX(), description="线路阻抗")
    cg: CG = Field(default=CG(), description="线路电容")
    mr: MR = Field(default=MR(), description="线路互感")
    acc_bran: List[ACCBranch] = Field(default_factory=list, description="交流电流通道")
    ana_chn: List[ChannelIdx] = Field(default_factory=list, description="模拟通道索引号")
    sta_chn: List[ChannelIdx] = Field(default_factory=list, description="开关量通道索引号")

    def __str__(self):
        xml = f"<scl:Line idx={self.idx} line_name={self.name} bus_ID={self.bus_idx} srcRef={self.reference} " \
              + f"VRtg={self.v_rtg} ARtg={self.a_rtg} ARtgSnd={self.a_rtg_snd} LinLen={self.lin_len} " \
              + f"bran_num={self.bran_num.get_code()} line_uuid="">"
        for acc_branch in self.acc_bran:
            xml += "\n" + str(acc_branch)
        for ana_chn in self.ana_chn:
            xml += "\n" + str(ana_chn)
        for sta_chn in self.sta_chn:
            xml += "\n" + str(sta_chn)
        return xml
