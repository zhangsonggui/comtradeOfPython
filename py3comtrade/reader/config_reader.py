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
import chardet

from py3comtrade.model.configure import Configure
from py3comtrade.model.precision_time import PrecisionTime
from py3comtrade.model.timemult import TimeMult
from py3comtrade.model.type.data_file_type import DataFileType
from py3comtrade.reader.analog_parser import analog_parser
from py3comtrade.reader.channel_num_parser import channel_num_parser
from py3comtrade.reader.digital_parser import digital_parser
from py3comtrade.reader.header_parser import header_parser
from py3comtrade.reader.nrates_parser import create_nrates, create_nrate


def detect_file_encoding(file_path):
    """
    检测文件的编码格式
    :param file_path: 文件路径
    :return: 文件的编码格式
    """
    with open(file_path, "rb") as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        encoding = result["encoding"]
        return encoding


def read_file(file_path):
    """判断文件格式后，读取cfg文件"""
    encoding = detect_file_encoding(file_path)
    if encoding is None:
        raise ValueError("无法确定文件编码格式")
    with open(file_path, "r", encoding=encoding) as f:
        content = f.readlines()
        return content


def config_reader(cfg_file_name):
    cfg_content = read_file(cfg_file_name)
    _configure = Configure(cfg_file_name)
    _configure.header = header_parser(cfg_content[0])  # 解析cfg文件头
    _configure.channel_num = channel_num_parser(cfg_content[1])  # 解析通道数量
    analog_num = _configure.channel_num.analog_num
    for i in range(2, _cl := analog_num + 2):
        _configure.add_analog(analog_parser(cfg_content[i]))
    for i in range(_cl, _configure.channel_num.total_num + 2):
        _configure.add_digital(digital_parser(cfg_content[i]))
    _configure.sample = create_nrates(cfg_content[_configure.channel_num.total_num + 2],
                                      cfg_content[_configure.channel_num.total_num + 3])
    for i in range(_cl := _configure.channel_num.total_num + 4, _configure.sample.nrate_num + _cl):
        _configure.sample.add_nrate(create_nrate(cfg_content[i]))
    _configure.sample.channel_num = _configure.channel_num
    _configure.sample.calc_sampling()
    _cl = _configure.sample.nrate_num + _cl
    _configure.file_start_time = PrecisionTime(cfg_content[_cl])
    _configure.fault_time = PrecisionTime(cfg_content[_cl + 1])
    _configure.sample.data_file_type = DataFileType.from_string(cfg_content[_cl + 2])
    _configure.sample.calc_sampling()
    if len(cfg_content) >= _cl + 3:
        _configure.timemult = TimeMult(timemult=float(cfg_content[_cl + 3]))
    return _configure


if __name__ == "__main__":
    configure = config_reader(r"D:\codeArea\gitee\comtradeOfPython\tests\data\hjz.cfg")
    print(configure.header.version)
