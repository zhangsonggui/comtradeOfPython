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
from typing import List, Optional

from pydantic import BaseModel, Field

from . import ChannelIdx
from .primary_equipments import ACCBranch, ACVBranch, PrimaryEquipments
from .type import TransWindLocation, WGFlag


class WG(BaseModel):
    wgroup: WGFlag = Field(default=WGFlag.Y, description="绕组标识符")
    angle: int = Field(default=0, description="绕组角度")


class Igap(BaseModel):
    zgap_idx: int = Field(default=0, description="中性点直接接地电流的通道号")
    zsgap_idx: int = Field(default=0, description="中性点经间隙接地电流的通道号")

    def __str__(self):
        xml = f"<scl:Igap zGap_idx={self.zgap_idx} zSGap_idx={self.zsgap_idx} />"
        return xml


class TransformerWinding(BaseModel):
    bus_id: int = Field(default=0, description="母线索引号")
    location: TransWindLocation = Field(default=TransWindLocation.HIGH, description="绕组位置")
    reference: Optional[str] = Field(default=None, description="IEC61850参引")
    v_rtg: float = Field(default=0.0, description="额定电压")
    a_rtg: float = Field(default=0.0, description="一次额定电流")
    bran_num: int = Field(default=0, description="分路数")
    wg: WG = Field(default=WG(), description="绕组标识符")
    acv_chn: ACVBranch = Field(default=ACVBranch(), description="交流电压通道")
    acc_bran: List[ACCBranch] = Field(default_factory=list, description="交流电流通道")
    igap: Igap = Field(default=Igap(), description="中性点电流通道号")

    def __str__(self):
        xml = f"<scl:TransformerWinding location={self.location.get_code()} srcRef={self.reference} VRtg={self.v_rtg} ARtg={self.a_rtg} bran_num={self.bran_num} bus_ID={self.bus_id} wG="">"
        xml += str(self.acv_chn)
        for acc_bran in self.acc_bran:
            xml += str(acc_bran)
        xml += str(self.igap)
        return xml


class Transformer(PrimaryEquipments):
    pwr_rtg: float = Field(default=0.0, description="变压器额定功率")
    transWinds: List[TransformerWinding] = Field(default_factory=list, description="变压器绕组")
    ana_chn: List[ChannelIdx] = Field(default_factory=list, description="模拟通道索引号")
    sta_chn: List[ChannelIdx] = Field(default_factory=list, description="开关量通道索引号")
    transformer_uuid: str = Field(default="", description="变压器标识")

    def __str__(self):
        xml = f"<scl:Transformer idx={self.idx} trm_name={self.name} srcRef={self.reference} pwrRtg={self.pwr_rtg} transformer_uuid={self.transformer_uuid}>"
        for trans_wind in self.transWinds:
            xml += str(trans_wind)
        for ana_chn in self.ana_chn:
            xml += str(ana_chn)
        for sta_chn in self.sta_chn:
            xml += str(sta_chn)
        return xml
