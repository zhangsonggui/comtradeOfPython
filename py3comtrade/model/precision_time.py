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
from datetime import datetime

from pydantic import BaseModel, Field

from py3comtrade.model.exceptions import ComtradeDataFormatException

time_formats = [
    "%d/%m/%Y,%H:%M:%S.%f",  # 四位年
    "%m/%d/%Y,%H:%M:%S.%f",  # 四位年
    "%m/%d/%y,%H:%M:%S.%f",  # 两位年
    "%Y-%m-%d %H:%M:%S",  # 另一种常见格式
]


def format_time(str_time: str):
    if isinstance(str_time, datetime):
        return str_time

    str_time = str_time.strip()
    if "." in str_time:
        parts = str_time.split(".")
        base = parts[0]
        microsecond = parts[1].ljust(6, "0")[:6]
        str_time = base + "." + microsecond
    for fmt in time_formats:
        try:
            return datetime.strptime(str_time, fmt)
        except ValueError:
            continue
    raise ComtradeDataFormatException(f"时间格式错误")


class PrecisionTime(BaseModel):
    time: datetime = Field(default=datetime.now(), description="时间")

    def __init__(self, time: str):
        super().__init__()
        self.time = format_time(time)

    def clear(self):
        self.time = datetime.now()

    def __str__(self):
        return f"{self.time.strftime(time_formats[0])}"
