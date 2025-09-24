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
import os
import re

import chardet

from py3comtrade.model.configure import Configure
from py3comtrade.model.exceptions import ComtradeDataNullException
from py3comtrade.model.precision_time import PrecisionTime
from py3comtrade.model.timemult import TimeMult
from py3comtrade.model.type.data_file_type import DataFileType
from py3comtrade.reader.analog_parser import analog_parser
from py3comtrade.reader.channel_num_parser import channel_num_parser, str_to_int
from py3comtrade.reader.digital_parser import digital_parser
from py3comtrade.reader.header_parser import header_parser
from py3comtrade.reader.nrates_parser import create_nrate, create_nrates


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
        # 如果chardet无法检测到编码或置信度太低，则尝试常见编码
        # if encoding is None or result["confidence"] < 0.7:
        #     # 尝试常见的编码格式，按优先级排序
        #     # 优先尝试中文编码，再尝试国际编码
        #     common_encodings = ["gbk", "gb2312", "utf-8", "utf-16", "ascii", "cp936", "ansi"]
        #     for enc in common_encodings:
        #         try:
        #             raw_data.decode(enc)
        #             return enc
        #         except UnicodeDecodeError:
        #             continue
        #     # 如果所有常见编码都失败，回退到gbk（中文Windows常用编码）
        #     return "gbk"
        if encoding is None:
            encoding = "gbk"
        # 对于检测到的编码，再次验证其有效性
        try:
            raw_data.decode(encoding)
            return encoding
        except UnicodeDecodeError:
            # 如果检测到的编码无效，尝试其他常见编码
            fallback_encodings = ["gbk", "utf-8", "gb2312", "utf-16", "ascii"]
            for enc in fallback_encodings:
                try:
                    raw_data.decode(enc)
                    return enc
                except UnicodeDecodeError:
                    continue
            # 最后的回退方案
            return "gbk"


def read_file(file_path):
    # 检查文件是否存在
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")

    """判断文件格式后，读取cfg文件"""
    encoding = detect_file_encoding(file_path)
    if encoding is None:
        raise ValueError("无法确定文件编码格式")
    with open(file_path, "r", encoding=encoding, errors="ignore") as f:
        content = [line.strip() for line in f.readlines() if line.strip()]
        # 增加文件是否为空的判断
        if len(content) < 10:
            raise ComtradeDataNullException(f"数据内容为空: {file_path}")
        return content


def config_reader(cfg_file_name) -> Configure:
    cfg_content = read_file(cfg_file_name)
    _configure = Configure()
    try:
        _header = cfg_content.pop(0)
        _header_arr = _header.strip().split(",")
        if len(_header_arr) > 3:
            for i in range(2, len(_header_arr)):
                part = _header_arr[i]
                if re.search(r'\b\d+[Aa]\b', part):
                    _configure.channel_num.analog_num = str_to_int(part)
                if re.search(r'\b\d+[Dd]\b', part):
                    _configure.channel_num.digital_num = str_to_int(part)
        else:
            _configure.header = header_parser(_header)  # 解析cfg文件头
            _configure.channel_num = channel_num_parser(cfg_content.pop(0))  # 解析通道数量
        # TODO 增加cfg文件对于通道数的校验工作
        for i in range(_configure.channel_num.analog_num):
            _configure.add_analog(analog_parser(cfg_content.pop(0)))
        for i in range(_configure.channel_num.digital_num):
            _configure.add_digital(digital_parser(cfg_content.pop(0)))
        _configure.sample = create_nrates(cfg_content.pop(0),
                                          cfg_content.pop(0))
        for i in range(_configure.sample.nrate_num):
            _configure.sample.add_nrate(create_nrate(cfg_content.pop(0)))
        _configure.sample.channel_num = _configure.channel_num
        _configure.sample.calc_sampling()
        _configure.file_start_time = PrecisionTime(cfg_content.pop(0))
        _configure.fault_time = PrecisionTime(cfg_content.pop(0))
        _configure.sample.data_file_type = DataFileType.from_string(cfg_content.pop(0))
        _configure.sample.calc_sampling()
        if cfg_content:
            try:
                timemult = float(cfg_content.pop(0))
            except ValueError:
                timemult = 1.0
            _configure.timemult = TimeMult(timemult=timemult)
    except IndexError:
        raise ValueError("cfg文件格式错误")
    return _configure


if __name__ == "__main__":
    configure = config_reader(r"D:\codeArea\gitee\comtradeOfPython\tests\data\hjz.cfg")
    print(configure.header.version)
