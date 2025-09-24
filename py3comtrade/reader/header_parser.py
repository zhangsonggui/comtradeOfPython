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


def identify_text_type(text):
    """
    判断文本类型,是全数字、数字加A、数字加D的组合，返回类型

    Args:
        text (str): 需要识别的文本

    Returns:
        dict: 包含不同类型匹配结果的字典
    """
    # 匹配纯数字（大于1991）
    all_numbers = re.findall(r'\b\d+\b', text)
    pure_numbers = [num for num in all_numbers if int(num) > 1991]

    # 匹配数字+A（如 1992A, 2000A等）
    numbers_with_a = re.findall(r'\b(\d+[Aa])\b', text)

    # 匹配数字+D（如 1992D, 2000D等）
    numbers_with_d = re.findall(r'\b(\d+[Dd])\b', text)

    return {
        'year'  : pure_numbers,
        'an_num': numbers_with_a,
        'dn_num': numbers_with_d
    }


YEAR_RE = r'\b([2-9]\d{3,}|199[1-9]|19[0-9]{3,}|[2-9][0-9]{4,})\b'


def header_parser(line) -> ConfigHeader:
    """解析配置头信息"""
    line = line.strip()
    if not line:
        raise ValueError("配置头信息为空")
    parts = line.split(",")
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


if __name__ == '__main__':
    # text = identify_text_type("浚河站,浚河站220kV河泉线PSL602G保护,11A,8D")
    pattern = r'\b([2-9]\d{3,}|199[1-9]|19[0-9]{3,}|[2-9][0-9]{4,})\b'
    p1 = re.search(pattern, "")
    print(p1.string)
