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

from py3comtrade.model.equipment.bus import Bus
from py3comtrade.model.equipment.line import Line
from py3comtrade.model.equipment.transformer import Transformer


class Equipment(BaseModel):
    buses: List[Bus] = Field(default_factory=list, description="母线")
    lines: List[Line] = Field(default_factory=list, description="线路")
    transformers: List[Transformer] = Field(default_factory=list, description="变压器")

    def is_bus_exist(self, bus_name: str) -> bool:
        """
        判断母线是否存在
        :param bus_name:母线标识
        :return: 存在返回True，不存在返回False
        """
        return any(bus.name == bus_name for bus in self.buses)

    def is_line_exist(self, line_name: str) -> bool:
        """
        判断线路是否存在
        :param line_name:线路标识
        :return: 存在返回True，不存在返回False
        """
        return any(line.name == line_name for line in self.lines)

    def is_transformer_exist(self, transformer_name: str) -> bool:
        """
        判断变压器是否存在
        :param transformer_name:变压器标识
        :return: 存在返回True，不存在返回False
        """
        return any(transformer.name == transformer_name for transformer in self.transformers)

    def find_bus_by_name(self, bus_name: str) -> Optional[tuple[int, Bus]]:
        """
        根据母线名称查找母线
        :param bus_name:母线标识
        :return: 存在返回母线，不存在返回None
        """
        for index, bus in enumerate(self.buses):
            if bus.name == bus_name:
                return index, bus
        return None

    def find_line_by_name(self, line_name: str) -> Optional[tuple[int, Line]]:
        """
        根据线路名称查找线路
        :param line_name:线路标识
        :return: 存在返回线路，不存在返回None
        """
        for index, line in enumerate(self.lines):
            if line.name == line_name:
                return index, line
        return None

    def find_transformer_by_name(self, transformer_name: str) -> Optional[tuple[int, Transformer]]:
        """
        根据变压器名称查找变压器
        :param transformer_name:变压器标识
        :return: 存在返回变压器，不存在返回None
        """
        for index, transformer in enumerate(self.transformers):
            if transformer.name == transformer_name:
                return index, transformer
        return None

    def bus_edit(self, bus_name: str, **kwargs) -> None:
        idx = kwargs.get('idx', 1)
