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

from pydantic import Field, BaseModel

from py3comtrade.model.channel import Channel
from py3comtrade.model.type.digital_enum import Contact
from py3comtrade.model.type.types import IdxType


class StatusRecord(BaseModel):
    """表示一个变为记录的模型类，包含时间戳和状态"""
    sample_point: int = Field(description="采样点")
    timestamp: int = Field(description="时间戳")
    status: int = Field(description="状态")


class Digital(Channel):
    """
    开关量通道类
    """
    contact: Contact = Field(default=Contact.NORMALLY_OPEN, description="状态通道正常状态")
    change_status: List[StatusRecord] = Field(default_factory=list, description="变位记录")

    def clear(self) -> None:
        """清除模型中所有字段"""
        super().clear()
        for field in self.model_fields.keys():
            setattr(self, field, None)

    def is_change(self):
        return len(self.change_status) > 1

    def is_enable(self):
        return super().is_enable() or self.is_change()

    def is_selected(self, target:list=None, target_type:IdxType= IdxType.INDEX):
        """判断通道是否被选中"""
        if target is None:
            self.selected = self.is_change()
            return self.selected
        return super().is_selected(target, target_type)

    def __str__(self):
        contact_code = 1 if self.contact == Contact.NORMALLY_CLOSED else 0
        return super().__str__() + f",{contact_code}"
