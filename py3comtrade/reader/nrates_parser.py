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
from py3comtrade.model.config_sample import ConfigSample
from py3comtrade.model.nrate import Nrate


def create_nrates(freg, nrate_num):
    """
    创建采样段对象
    """
    freg = float(freg.strip())
    nrate_num = int(nrate_num.strip())
    return ConfigSample(freg=freg, nrate_num=nrate_num)


def create_nrate(line):
    """
    解析采样段信息
    """
    samp, end_point = line.strip().split(",")
    return Nrate(samp=samp, end_point=end_point)
