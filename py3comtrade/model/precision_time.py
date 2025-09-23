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
    "%d/%m/%Y,%H:%M:%S.%f",  # 四位年，欧洲格式（日/月/年）
    "%m/%d/%Y,%H:%M:%S.%f",  # 四位年，美国格式（月/日/年）
    "%m/%d/%y,%H:%M:%S.%f",  # 两位年，美国格式（月/日/年）
    "%d/%m/%Y, %H:%M:%S.%f",  # 四位年，欧洲格式，带空格（你提供的例子）
    "%Y-%m-%d %H:%M:%S",  # ISO日期格式，无微秒
    "%Y-%m-%d %H:%M:%S.%f",  # ISO日期格式，带微秒
    "%Y-%m-%d,%H:%M:%S.%f",  # ISO日期格式，逗号分隔，带微秒
    "%Y/%m/%d %H:%M:%S",  # 斜杠分隔的年月日格式
    "%Y/%m/%d %H:%M:%S.%f",  # 带微秒的斜杠分隔格式
    "%d/%m/%Y %H:%M:%S",  # 欧洲常用格式，空格分隔
    "%d/%m/%Y %H:%M:%S.%f",  # 带微秒的欧洲常用格式
    "%m/%d/%Y %H:%M:%S",  # 美国常用格式，空格分隔
    "%m/%d/%Y %H:%M:%S.%f",  # 带微秒的美国常用格式
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
            # 处理闰年日期错误的情况
            if "29" in str_time and ("02/" in str_time or "/02/" in str_time):
                # 尝试将2月29日替换为2月28日
                try:
                    modified_time = str_time.replace("/29/", "/28/")
                    return datetime.strptime(modified_time, fmt)
                except ValueError:
                    continue
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
