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
from pydantic import Field
from typing import Optional, Union

from .channel import ChannelIdx
from .type import BreakerFlag, ChannelFlag, Contact, RelayFlag, SignalType, WarningFlag


class StatusChannel(ChannelIdx):
    idx_org: Optional[int] = Field(description="装置端子号")
    type: SignalType = Field(default=SignalType.RELAY, description="通道类型")
    flag: Union[ChannelFlag,RelayFlag,BreakerFlag,WarningFlag] = Field(default=ChannelFlag.GENERAL, description="通道标志")
    contact: Contact = Field(default=Contact.NORMALLY_OPEN, description="通道接点类型")
    reference: Optional[str] = Field(default=None, description="IEC61850参引")
