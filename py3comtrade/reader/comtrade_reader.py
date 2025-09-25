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
from py3comtrade.model.exceptions import ComtradeFileEncodingException, ComtradeFileNotFoundException
from py3comtrade.model.precision_time import PrecisionTime
from py3comtrade.model.type.mode_enum import ReadMode
from py3comtrade.model.type.types import ValueType
from py3comtrade.reader.analog_parser import analog_from_dict
from py3comtrade.reader.channel_num_parser import channel_num_from_dict
from py3comtrade.reader.config_reader import config_reader
from py3comtrade.reader.data_reader import data_reader
from py3comtrade.reader.digital_parser import digital_from_dict
from py3comtrade.reader.dmf_reader import dmf_parser
from py3comtrade.reader.header_parser import header_from_dict
from py3comtrade.reader.nrates_parser import sample_from_dict
from py3comtrade.utils.comtrade_file_path import get_comtrade_path


def comtrade_reader(_file_path: str, read_mode: ReadMode = ReadMode.FULL, value_type: str = "INSTANT") -> Comtrade:
    """
    读取Comtrade数据

    参数:
        _file_path(str): 文件路径
        read_mode: 读取模式
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
    _comtrade: Comtrade = Comtrade(file_path=files,
                                   header=cfg.header,
                                   channel_num=cfg.channel_num,
                                   analogs=cfg.analogs,
                                   digitals=cfg.digitals,
                                   sample=cfg.sample,
                                   file_start_time=cfg.file_start_time,
                                   fault_time=cfg.fault_time,
                                   timemult=cfg.timemult)
    if read_mode in [ReadMode.DAT, ReadMode.FULL]:
        try:
            dat = data_reader(str(files.dat_path), cfg.sample)
            _comtrade.sample_point = dat.sample_time[:, 0].tolist()
            _comtrade.sample_time = dat.sample_time[:, 1].tolist()
            if value_type.upper() == "INSTANT":
                _comtrade.sample.value_type = ValueType.INSTANT
                for analog in _comtrade.analogs:
                    if value_type == ValueType.INSTANT.name:
                        vs = dat.analog_value.T[analog.index, :]
                        analog.values = np.round(vs * analog.a + analog.b, 3).tolist()
            elif value_type.upper() == "RAW":
                _comtrade.sample.value_type = ValueType.RAW
                for analog in _comtrade.analogs:
                    analog.values = dat.analog_value.T[analog.index, :].tolist()
            for digital in _comtrade.digitals:
                digital.values = dat.digital_value.T[digital.index, :].tolist()

        except ComtradeFileEncodingException as e:
            raise ComtradeFileEncodingException(_file_path, "文件解析失败")
        _comtrade.analyze_digital_change_status()
    if read_mode in [ReadMode.DMF, ReadMode.FULL]:
        try:
            _dmf = dmf_parser(str(files.dmf_path))
            _comtrade.buses = _dmf.buses
            _comtrade.lines = _dmf.lines
            _comtrade.transformers = _dmf.transformers
            _comtrade.analog_channels = _dmf.analog_channels
            _comtrade.status_channels = _dmf.status_channels
        except ComtradeFileEncodingException as e:
            pass

    return _comtrade


def comtrade_from_dict(comtrade_dict: dict) -> Comtrade:
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

    return Comtrade(
        header=header,
        channel_num=channel_num,
        analogs=analogs,
        digitals=digitals,
        sample=sample,
        file_start_time=PrecisionTime(comtrade_dict.get("file_start_time").get("time")),
        fault_time=PrecisionTime(comtrade_dict.get("fault_time").get("time")),
        timemult=comtrade_dict.get("timemult").get("timemult")

    )


if __name__ == '__main__':
    file_path = r'D:\codeArea\gitee\comtradeOfPython\tests\data\xtz'
    wave = comtrade_reader(file_path)
    print(wave)
