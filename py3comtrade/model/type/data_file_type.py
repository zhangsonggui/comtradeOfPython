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
from py3comtrade.model.type.base_enum import BaseEnum


class DataFileType(BaseEnum):
    ASCII = ("ASCII", "ASCII格式")
    BINARY = ("BINARY", "二进制格式")
    BINARY32 = ("BINARY32", "32位二进制文件")
    FLOAT32 = ("FLOAT32", "32位浮点数")

    @classmethod
    def from_string(cls, string: str):
        """
        尝试将给定的字符串转换为对应的枚举成员。

        :param string: 需要被解析的字符串
        :return: 对应的枚举成员或 None 如果没有匹配
        """
        string = string.strip().upper()
        for ft in cls:
            if string == ft.get_code:
                return ft
        return cls.BINARY
