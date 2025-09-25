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

from py3comtrade.model.config_header import ConfigHeader

YEAR_RE = r'\b([2-9]\d{3,}|199[1-9]|19[0-9]{3,}|[2-9][0-9]{4,})\b'


def header_from_str(_header_str: str) -> ConfigHeader:
    """解析配置头信息"""
    if not _header_str:
        raise ValueError("配置头信息为空")
    parts = _header_str.strip().split(",")
    station_name = ''
    recorder_name = ''
    version = 1991
    if (l := len(parts)) >= 1:
        station_name = parts[0]
    if l >= 2:
        recorder_name = parts[1]
    if l >= 3:
        p3 = re.search(YEAR_RE, parts[2])
        version = 1991 if p3 is None else p3.string

    return ConfigHeader(station_name=station_name, recorder_name=recorder_name, version=version)


def header_from_dict(_header_dict: dict):
    """从字典解析配置头信息"""
    station_name = _header_dict.get("station_name", "变电站")
    recorder_name = _header_dict.get("recorder_name", "录波设备")
    version = _header_dict.get("version", 1991)
    return ConfigHeader(station_name=station_name, recorder_name=recorder_name, version=version)
