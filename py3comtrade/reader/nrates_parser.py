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
from py3comtrade.model.config_sample import ConfigSample
from py3comtrade.model.nrate import Nrate
from py3comtrade.model.type.data_file_type import DataFileType
from py3comtrade.model.type.types import ValueType
from py3comtrade.reader.channel_num_parser import channel_num_from_dict


def create_nrates(freg, nrate_num):
    """
    创建采样段对象
    """
    freg = float(freg.strip())
    freg = 50.0 if freg == 0.0 else freg
    nrate_num = int(nrate_num.strip())
    return ConfigSample(freg=freg, nrate_num=nrate_num)


def create_nrate(line):
    """
    解析采样段信息
    """
    samp, end_point = line.strip().split(",")
    return Nrate(samp=samp, end_point=end_point)


def nrate_from_dict(_nrate_dict: dict) -> Nrate | None:
    index = _nrate_dict.get("index", 0)
    samp = _nrate_dict.get("samp", 0)
    start_point = _nrate_dict.get("start_point", 0)
    end_point = _nrate_dict.get("end_point", 0)
    cycle_point = _nrate_dict.get("cycle_point", 0)
    count = _nrate_dict.get("count", 0)
    duration = _nrate_dict.get("duration", 0)
    end_time = _nrate_dict.get("end_time", 0)

    if samp == 0 or end_point == 0:
        return None
    return Nrate(
        index=index,
        samp=samp,
        end_point=end_point,
        start_point=start_point,
        cycle_point=cycle_point,
        count=count,
        duration=duration,
        end_time=end_time
    )


def sample_from_dict(_sample_dict: dict) -> ConfigSample:
    sample = ConfigSample(
        freg=_sample_dict.get("freg", 50.0),
        nrate_num=_sample_dict.get("nrate_num", 0),
        count=_sample_dict.get("count", 0),
        data_file_type=DataFileType.from_string(_sample_dict.get("data_file_type", "BINARY"),
                                                default=DataFileType.BINARY),
        value_type=ValueType.from_string(_sample_dict.get("value_type", "INSTANT"), default=ValueType.INSTANT),
        analog_word=_sample_dict.get("analog_word", 2),
        digital_word=_sample_dict.get("digital_word", 2),
        analog_sampe_word=_sample_dict.get("analog_sampe_word", 2),
        digital_sampe_word=_sample_dict.get("digital_sampe_word", 2),
        total_sampe_word=_sample_dict.get("total_sampe_word", 2),
    )
    for nrate in _sample_dict.get("nrates", []):
        nrate = nrate_from_dict(nrate)
        if nrate is None:
            continue
        sample.nrates.append(nrate)

    sample.channel_num = channel_num_from_dict(_sample_dict.get("channel_num"))
    return sample
