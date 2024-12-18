#!/usr/bin/env python
# -*- coding: utf-8 -*-

from py3comtrade.model.digital import Digital
from py3comtrade.model.type.digital_enum import Contact
from py3comtrade.model.type.phase_code import PhaseCode


def digital_parser(_line_str):
    """
    从一行文本字符串中生成数字通道对象
    :param _line_str: 配置文件中一行数字通道字符串
    :return: 数字通道对象
    """
    _line_str = _line_str.strip().split(",")
    index = _line_str[0]
    name = _line_str[1]
    phase = PhaseCode.from_string(_line_str[2])
    ccbm = _line_str[3]
    status = Contact.from_string(_line_str[4])
    return Digital(index, name, phase, ccbm, status)
