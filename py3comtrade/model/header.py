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
import re

from pydantic import BaseModel, Field

from py3comtrade.model.exceptions import ComtradeDataFormatException

YEAR_RE = r'\b([2-9]\d{3,}|199[1-9]|19[0-9]{3,}|[2-9][0-9]{4,})\b'


class Header(BaseModel):
    """
    cfg文件头部信息，变电站名称，录波设备名称和录波格式版本号
    """

    station_name: str = Field(default="变电站", description="变电站名称")
    recorder_name: str = Field(default="录波设备", description="录波设备名称")
    version: int = Field(default=1991, description="录波格式版本号")

    def clear(self):
        """清除模型中所有字段"""
        for field in self.model_fields.keys():
            setattr(self, field, None)

    @classmethod
    def from_string(cls, data_str: str) -> 'Header':
        """
        从字符串创建Header对象
        :param data_str: 包含Header对象属性的字符串
        :return: Header对象实例
        """
        if not data_str or not isinstance(data_str, str):
            raise ComtradeDataFormatException(f"输入字符串不能为空或不是字符串类型")
        station_name = ""
        recorder_name = ""
        version = 1991
        try:
            parts = data_str.strip().split(",")
            if (l := len(parts)) >= 1:
                station_name = parts[0]
            if l >= 2:
                recorder_name = parts[1]
            if l >= 3:
                p3 = re.search(YEAR_RE, parts[2])
                version = 1991 if p3 is None else int(p3.string)

            header = cls(
                station_name=station_name,
                recorder_name=recorder_name,
                version=version
            )
            return header
        except ValueError as e:
            raise ValueError(f"创建Header对象时发生错误: {str(e)}") from e

    @classmethod
    def from_dict(cls, data_dict: dict) -> 'Header':
        """从字典解析配置头信息"""
        if not data_dict or not isinstance(data_dict, dict):
            raise TypeError(f"期望字典类型输入，实际得到: {type(data_dict).__name__}")
        station_name = data_dict.get("station_name", "变电站")
        recorder_name = data_dict.get("recorder_name", "录波设备")
        version = data_dict.get("version", 1991)
        return cls(station_name=station_name, recorder_name=recorder_name, version=version)

    def __str__(self):
        return f"{self.station_name},{self.recorder_name},{self.version}"
