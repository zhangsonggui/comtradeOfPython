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

from pydantic import Field

from .channel import Channel
from .digital_change_status import DigitalChangeStatus
from .type import Contact


class Digital(Channel):
    """
    开关量通道类
    """
    contact: Contact = Field(default=Contact.NORMALLY_OPEN, description="状态通道正常状态")
    change_status: DigitalChangeStatus = Field(default_factory=list, description="变位记录")

    def clear(self) -> None:
        """清除模型中所有字段"""
        super().clear()
        for field in self.model_fields.keys():
            setattr(self, field, None)

    def __str__(self):
        contact_code = 0
        if self.contact == Contact.NORMALLY_CLOSED:
            contact_code = 1
        return super().__str__() + f",{contact_code}"
