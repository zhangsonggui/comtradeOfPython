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


from py3comtrade.model.config_header import ConfigHeader


def header_parser(line) -> ConfigHeader:
    """解析配置头信息"""
    line = line.strip()
    if not line:
        raise ValueError("配置头信息为空")
    parts = line.split(",")
    if len(parts) < 2:
        raise ValueError("配置头信息格式错误")
    if len(parts) == 3:
        return ConfigHeader(station_name=parts[0], recorder_name=parts[1], version=parts[2])
    return ConfigHeader(station_name=parts[0], recorder_name=parts[1])
