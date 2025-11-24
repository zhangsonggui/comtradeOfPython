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

from pydantic import BaseModel, Field

from py3comtrade.model.equipment.bus import Bus
from py3comtrade.model.equipment.line import Line
from py3comtrade.model.equipment.transformer import Transformer


def create_finder(element_attr: str, return_tuple: bool = True):
    """
    创建查找器的工厂函数
    :param element_attr: 元素属性名 ('buses', 'lines', 'transformers')
    :param return_tuple: 是否返回(index, element)元组，False则只返回索引
    """

    def finder(self, name: str):
        elements = getattr(self, element_attr)
        for index, element in enumerate(elements):
            if hasattr(element, 'name') and element.name == name:
                return (index, element) if return_tuple else index
        return None if return_tuple else -1

    return finder


class Equipment(BaseModel):
    buses: List[Bus] = Field(default_factory=list, description="母线")
    lines: List[Line] = Field(default_factory=list, description="线路")
    transformers: List[Transformer] = Field(default_factory=list, description="变压器")

    # 查找并返回索引
    get_bus_index = create_finder('buses', return_tuple=False)
    get_line_index = create_finder('lines', return_tuple=False)
    get_transformer_index = create_finder('transformers', return_tuple=False)

    # 查找并返回(index, element)元组
    find_bus_by_name = create_finder('buses', return_tuple=True)
    find_line_by_name = create_finder('lines', return_tuple=True)
    find_transformer_by_name = create_finder('transformers', return_tuple=True)
