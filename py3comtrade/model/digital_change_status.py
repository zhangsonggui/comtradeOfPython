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

from pydantic import BaseModel, Field


class StatusRecord(BaseModel):
    """表示一个变为记录的模型类，包含时间戳和状态"""
    timestamp: int = Field(description="时间戳")
    status: int = Field(description="状态")


class DigitalChangeStatus(BaseModel):
    records: List[StatusRecord] = Field(default_factory=list, description="变位记录列表")

    def __len__(self):
        return len(self.records)
