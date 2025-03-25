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

from py3comtrade.model.channel import Channel
from py3comtrade.model.type.digital_enum import Contact


class Digital(Channel):
    """
    开关量通道类
    """
    contact: Contact = Field(default=Contact.NORMALLYOPEN, description="状态通道正常状态")

    def __init__(self,
                 cfg_index: int,
                 name: str,
                 phase: str = None,
                 ccbm: str = None,
                 contact: Contact = Contact.NORMALLYOPEN):
        super().__init__(cfg_index=cfg_index, name=name, phase=phase, ccbm=ccbm)
        self.contact = contact

    def clear(self) -> None:
        """清除模型中所有字段"""
        super().clear()
        for field in self.__fields__.keys():
            setattr(self, field, None)

    def __str__(self):
        return super().__str__() + f",{self.contact.code}"
