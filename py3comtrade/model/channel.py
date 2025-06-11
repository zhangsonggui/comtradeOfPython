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

from pydantic import BaseModel, Field

from .type import PhaseCode


class Channel(BaseModel):
    """
    通道类
    """
    cfg_index: int = Field(..., description="模拟通道索引号，必选，数字，整数")
    name: str = Field(..., description="通道标识符，必选，字符串，最大长度128个字符")
    phase: PhaseCode = Field(default=PhaseCode.NO_PHASE,
                             description="通道相别标识，可选，字母、数字，最小0个字符，最大长度2个字符")
    ccbm: str = Field(default="", description="被监视的电路元件，可选，字母、数字，最小0个字符，最大长度64个字符")
    index: int = Field(default=0, description="通道索引号")
    instants: list[float] = Field(default=list, description="通道数值")

    def clear(self) -> None:
        """清除模型中所有字段"""
        for field in self.model_fields.keys():
            setattr(self, field, None)

    def __str__(self):
        return f"{self.cfg_index},{self.name},{self.phase.code},{self.ccbm}"
