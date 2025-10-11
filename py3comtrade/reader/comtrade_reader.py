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

import numpy as np

from py3comtrade.model.comtrade import Comtrade
from py3comtrade.model.exceptions import (
    ComtradeFileEncodingException,
    ComtradeFileNotFoundException,
)
from py3comtrade.model.precision_time import PrecisionTime
from py3comtrade.model.timemult import TimeMult
from py3comtrade.model.type.types import ValueType
from py3comtrade.reader.analog_parser import analog_from_dict
from py3comtrade.reader.channel_num_parser import channel_num_from_dict
from py3comtrade.reader.config_reader import config_reader
from py3comtrade.reader.data_reader import data_reader
from py3comtrade.reader.digital_parser import digital_from_dict
from py3comtrade.reader.dmf_reader import dmf_parser
from py3comtrade.reader.header_parser import header_from_dict
from py3comtrade.reader.nrates_parser import sample_from_dict
from py3comtrade.utils.comtrade_file_path import (
    generate_comtrade_path,
    get_comtrade_path,
)


def comtrade_reader(_file_path: str, read_mode: str = "full") -> Comtrade:
    """
    读取Comtrade数据

    参数:
        _file_path(str): 文件路径
        read_mode: 读取模式,可选择full、cfg、dat、dmf,默认为full
    返回:
        Comtrade对象
    """
    files = get_comtrade_path(_file_path)
    if not files:
        raise ComtradeFileNotFoundException(_file_path, "文件不存在")
    try:
        cfg = config_reader(files.cfg_path)
    except ComtradeFileEncodingException:
        raise ComtradeFileEncodingException(f"文件格式错误:{_file_path}")
    _comtrade: Comtrade = Comtrade(
        file_path=files,
        header=cfg.header,
        channel_num=cfg.channel_num,
        analogs=cfg.analogs,
        digitals=cfg.digitals,
        sample=cfg.sample,
        file_start_time=cfg.file_start_time,
        fault_time=cfg.fault_time,
        timemult=cfg.timemult,
    )
    if read_mode.lower() in ["dat", "full"]:
        try:
            dat = data_reader(str(files.dat_path), cfg.sample)
            _comtrade.sample_point = dat.sample_time[:, 0].tolist()
            _comtrade.sample_time = dat.sample_time[:, 1].tolist()
            for analog in _comtrade.analogs:
                vs = dat.analog_value.T[analog.index, :]
                analog.values_type = ValueType.INSTANT
                analog.values = np.round(vs * analog.a + analog.b, 3).tolist()
            for digital in _comtrade.digitals:
                digital.values = dat.digital_value.T[digital.index, :].tolist()
        except ComtradeFileEncodingException as e:
            raise ComtradeFileEncodingException(_file_path, "文件解析失败")
        _comtrade.analyze_digital_change_status()
    if read_mode.lower() in ["dmf", "full"]:
        try:
            _dmf = dmf_parser(str(files.dmf_path))
            _comtrade.buses = _dmf.buses
            _comtrade.lines = _dmf.lines
            _comtrade.transformers = _dmf.transformers
        except ComtradeFileEncodingException as e:
            pass

    return _comtrade


def comtrade_from_dict(comtrade_dict: dict) -> Comtrade:
    _file_path = generate_comtrade_path(
        comtrade_dict.get("file_path", {}).get("cfg_path")
    )
    header = header_from_dict(comtrade_dict.get("header"))
    channel_num = channel_num_from_dict(comtrade_dict.get("channel_num"))
    analogs_dict = comtrade_dict.get("analogs")
    analogs = []
    for analog_dict in analogs_dict:
        analogs.append(analog_from_dict(analog_dict))
    digitals_dict = comtrade_dict.get("digitals")
    digitals = []
    for digital_dict in digitals_dict:
        digitals.append(digital_from_dict(digital_dict))
    sample = sample_from_dict(comtrade_dict.get("sample"))
    fault_point = comtrade_dict.get("fault_point", 0)
    # 安全获取嵌套字典的值
    file_start_time_dict = comtrade_dict.get("file_start_time", {})
    fault_time_dict = comtrade_dict.get("fault_time", {})
    timemult_dict = comtrade_dict.get("timemult", {})

    _comtrade = Comtrade(
        file_path=_file_path,
        header=header,
        channel_num=channel_num,
        analogs=analogs,
        digitals=digitals,
        sample=sample,
        fault_point=fault_point,
        sample_point=comtrade_dict.get("sample_point", []),
        sample_time=comtrade_dict.get("sample_time", []),
        file_start_time=PrecisionTime(file_start_time_dict.get("time")),
        fault_time=PrecisionTime(fault_time_dict.get("time")),
        timemult=TimeMult(timemult=float(timemult_dict.get("timemult", 1.0))),
    )
    _comtrade.analyze_digital_change_status()
    return _comtrade


if __name__ == "__main__":
    file_path = r"D:\codeArea\gitee\comtradeOfPython\tests\data\xtz"
    wave = comtrade_reader(file_path)
    print(wave)
