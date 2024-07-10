#!/usr/bin/env python
# -*- coding: utf-8 -*-
from py3comtrade.parser.analog_channel import generate_analog_channel_str
from py3comtrade.parser.cfg_parser import CfgParser
from py3comtrade.parser.digital_channel import generate_digital_channel_str
from py3comtrade.parser.fault_header import generate_fault_header_str
from py3comtrade.parser.sample_info import generate_sample_info_str


def generate_cfg_str(cfg_obj):
    """
    生成cfg文件字符串
    @param cfg_obj: cfg对象
    @return: cfg文件字符串
    """
    fault_headers_str = generate_fault_header_str(cfg_obj.fault_header) + '\n'
    analog_channels_str = ''
    for ac in cfg_obj.analog_channels:
        analog_channels_str += generate_analog_channel_str(ac) + '\n'
    digital_channels_str = ''
    for dc in cfg_obj.digital_channels:
        digital_channels_str += generate_digital_channel_str(dc) + '\n'
    sample_info_str = generate_sample_info_str(cfg_obj.sample_info) + '\n'
    return fault_headers_str + analog_channels_str + digital_channels_str + sample_info_str


def cfg_to_file(cfg: CfgParser, filename: str):
    """
    将cfg文件写入文件
    :param cfg: cfg文件对象
    :param filename: 文件名
    """
    with open(filename, 'w', encoding='gbk') as f:
        f.write(generate_cfg_str(cfg.cfg))
    return f'{filename}文件生成成功！'
