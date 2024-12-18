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

from typing import Union

from py3comtrade.model.base_channel import BaseChannel
from py3comtrade.model.type.digital_enum import Contact
from py3comtrade.model.type.phase_code import PhaseCode


class Digital(BaseChannel):
    """
    开关量通道类
    """

    __contact: Contact

    def __init__(
            self,
            cfg_index: Union[int, str],
            name: str,
            phase: PhaseCode = PhaseCode.NO_PHASE,
            ccbm: str = "",
            contact: Contact = Contact.NORMALLYOPEN,
    ):
        """
        初始化
        :param cfg_index: 通道索引
        :param name: 通道名称
        :param phase: 通道相位
        :param ccbm: 通道CCBM
        :param contact: 开关量初始值
        """
        super().__init__(cfg_index, name, phase, ccbm)
        self.__contact = contact

    def clear(self) -> None:
        super().clear()
        self.__contact = 0

    def __str__(self):
        return super().__str__() + f",{self.contact}"

    @property
    def contact(self) -> Contact:
        return self.__contact
