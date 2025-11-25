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
from pydantic import BaseModel, Field

from py3comtrade.model.channel.analog import Analog
from py3comtrade.model.channel.digital import Digital
from py3comtrade.model.channel_num import ChannelNum
from py3comtrade.model.comtrade import Comtrade
from py3comtrade.model.config_sample import ConfigSample
from py3comtrade.model.configure import Configure
from py3comtrade.model.exceptions import (
    ComtradeFileEncodingException,
    ComtradeFileNotFoundException, ComtradeFileNumException, ComtradeFileSizeException, ComtradeFileSuffixException,
    ComtradeParamException,
)
from py3comtrade.model.header import Header
from py3comtrade.model.precision_time import PrecisionTime
from py3comtrade.model.timemult import TimeMult
from py3comtrade.model.type.types import ValueType
from py3comtrade.reader.data_reader import data_reader
from py3comtrade.reader.dmf_reader import dmf_parser
from py3comtrade.utils.comtrade_file import ComtradeFile
from py3comtrade.utils.file_tools import try_decode
from py3comtrade.utils.log import logger


def comtrade_reader(_file_path: str, read_mode: str = "full") -> Comtrade:
    """
    读取Comtrade数据

    参数:
        _file_path(str): 文件路径
        read_mode: 读取模式,可选择full、cfg、dat、dmf,默认为full
    返回:
        Comtrade对象
    """
    cfr = ComtradeFileReader(_file_path=_file_path)
    cfg = cfr.read_cfg_file()

    _comtrade: Comtrade = Comtrade(
        file_path=cfr.comtrade_file,
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
            dat = data_reader(str(cfr.comtrade_file.dat_path), cfg.sample)
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
            _dmf = dmf_parser(str(cfr.comtrade_file.dmf_path))
            _comtrade.buses = _dmf.buses
            _comtrade.lines = _dmf.lines
            _comtrade.transformers = _dmf.transformers
        except ComtradeFileEncodingException as e:
            pass

    return _comtrade


def comtrade_from_dict(comtrade_dict: dict) -> Comtrade:
    _file_path = ComtradeFile(
        file_path=comtrade_dict.get("_file_path", {}).get("cfg_path")
    )
    header = Header.from_dict(comtrade_dict.get("header"))
    channel_num = ChannelNum.from_dict(comtrade_dict.get("channel_num"))
    analogs_dict = comtrade_dict.get("analogs")
    analogs = []
    for analog_dict in analogs_dict:
        analogs.append(Analog.from_dict(analog_dict))
    digitals_dict = comtrade_dict.get("digitals")
    digitals = []
    for digital_dict in digitals_dict:
        digitals.append(Digital.from_dict(digital_dict))
    sample = ConfigSample.from_dict(comtrade_dict.get("sample"))
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


class ComtradeFileReader(BaseModel):
    comtrade_file: ComtradeFile = Field(default=None, description="comtrade文件组")

    def __init__(self, _file_path: str, **data):
        super().__init__(**data)
        self.get_comtrade_file(_file_path)

    def get_comtrade_file(self, _file_path: str):
        if not _file_path:
            message = f"{_file_path}不能为空"
            logger.error(message)
            return ComtradeParamException(param_name="_file_path", message=message)
        try:
            # 将Path对象转换为字符串传递给ComtradeFile
            self.comtrade_file = ComtradeFile(file_path=str(_file_path))
        except ComtradeFileNotFoundException as e:
            return e.message
        except ComtradeFileNumException as e:
            return e.message
        except ComtradeFileSizeException as e:
            return e.message
        except ComtradeFileSuffixException as e:
            return e.message
        except Exception as e:
            raise e

    def read_cfg_file(self) -> Configure | None:
        if not self.comtrade_file or not self.comtrade_file.cfg_path:
            return None
        cfg_path = self.comtrade_file.cfg_path
        enc = try_decode(cfg_path)
        if not enc:
            return None
        with open(cfg_path, encoding=enc) as cfg:
            return Configure.from_string(cfg.read())

    def read_data_file(self) -> Comtrade | None:
        pass


if __name__ == "__main__":
    file_path = r"D:\codeArea\gitee\comtradeOfPython\tests\data\xtz"
    wave = comtrade_reader(file_path)
    print(wave)
