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
from typing import List

from pydantic import Field

from py3comtrade.model.channel.channel import ChannelIdx
from py3comtrade.model.equipment.base_param import BaseParam
from py3comtrade.model.equipment.branch import ACVBranch
from py3comtrade.model.type.analog_enum import TvInstallation


class Bus(BaseParam):
    """
    Bus class
    """
    v_rtg: float = Field(default=0.0, description="一次额定电压")
    v_rtg_snd: float = Field(default=100.0, description="二次额定电压")
    v_rtg_snd_pos: TvInstallation = Field(default=TvInstallation.BUS, description="TV安装位置")
    bus_uuid: str = Field(default="", description="母线标识")
    acv_chn: ACVBranch = Field(default=ACVBranch(), description="交流电压通道")
    analog_chn: List[ChannelIdx] = Field(default_factory=list, description="模拟量通道")
    digital_chn: List[ChannelIdx] = Field(default_factory=list, description="开关量通道")

    def __str__(self):
        xml = f"<scl:Bus idx={self.idx} bus_name={self.name} srcRef={self.reference} VRtg={self.v_rtg} VRtgSnd={self.v_rtg_snd} VRtgSnd_Pos={self.v_rtg_snd_pos.get_code()} bus_uuid="">"
        xml += str(self.acv_chn)
        for chn in self.analog_chn:
            xml += str(chn)
        for chn in self.digital_chn:
            xml += str(chn)
        return xml
