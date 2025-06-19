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

from pydantic import BaseModel,Field

from .analog_channel import AnalogChannel
from .bus import Bus
from .line import Line
from .transformer import Transformer
from .status_channel import StatusChannel


class DMF(BaseModel):
    station_name:str = Field(default="变电站", description="站点名称")
    version:float = Field(default=1.0, description="版本号")
    reference:str = Field(default=0,description="参引类型")
    rec_dev_name:str = Field(default="录波装置", description="装置名称")
    rec_ref:Optional[str] = Field(default="",description="装置RDRE参引")
    analog_channels:List[AnalogChannel] = Field(default_factory=list, description="模拟通道")
    status_channels:List[StatusChannel] = Field(default_factory=list, description="开关量通道")
    buses:List[Bus] = Field(default_factory=list, description="母线")
    lines:List[Line] = Field(default_factory=list, description="线路")
    transformers:List[Transformer] = Field(default_factory=list, description="变压器")
