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
import json
from datetime import datetime
from enum import Enum
from pathlib import WindowsPath


class BaseEnum(Enum):
    def __new__(cls, *args, **kargs):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    def __init__(self, code, description):
        self.code = code
        self.description = description

    def get_code(self) -> str:
        return self.code

    def get_description(self) -> str:
        return self.description

    @classmethod
    def from_string(cls, string: str, fuzzy: bool = True, default=None):
        """
        尝试将给定的字符串转换为对应的枚举成员。

        :param string: 要解析的字符串
        :param fuzzy: 是否启用模糊匹配（如结尾匹配），默认开启
        :param default: 默认枚举值
        :return: 对应的枚举成员
        :raises ValueError: 如果找不到匹配项且未启用 fuzzy 或 fuzzy 也失败
        """
        # 处理空字符串或空白字符串
        if not string or string.strip() in ["", "null"]:
            if default is not None:
                return default
            raise ValueError(f"{cls.__name__} 未提供字符串且未设置默认值")

        string = string.strip().upper()

        # 精确匹配
        for member in cls:
            code = str(member.get_code()).upper()
            if code == string:
                return member

        # 模糊匹配（结尾匹配）
        if fuzzy:
            for member in cls:
                code = str(member.get_code()).upper()
                if string.endswith(code):
                    return member
        return default
        # raise ValueError(f"无法将 '{string}' 映射到 {cls.__name__} 枚举类型中")


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()

        if isinstance(obj, WindowsPath):
            return str(obj)
        # 处理所有枚举类型
        if isinstance(obj, Enum):
            return obj.value

        return super().default(obj)
