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
from datetime import datetime

from pydantic import BaseModel, Field

time_format = "%d/%m/%Y,%H:%M:%S.%f"  # 时间格式字符串


def format_time(time):
    if isinstance(time, datetime):
        return time

    try:
        str_time = time.strip()
        return datetime.strptime(str_time, time_format)
    except ValueError as e:
        raise ValueError(f"时间格式错误:{e}")


class PrecisionTime(BaseModel):
    time: datetime = Field(default=datetime.now(), description="时间")

    def __init__(self, time: str):
        super().__init__()
        self.time = format_time(time)

    def clear(self):
        self.time = datetime.now()

    def __str__(self):
        return f"{self.time.strftime(time_format)}"
