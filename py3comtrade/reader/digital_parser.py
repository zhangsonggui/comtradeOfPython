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
    line = _line_str.strip()
    if not line:
        raise ValueError("开关量信息为空")
    parts = line.split(",")

    if len(parts) ==3:
        index = parts[0]
        name = parts[1]
        status = Contact.from_string(parts[2])
        return Digital(cfg_index=index, name=name, contact=status)
    if len(parts) == 5:
        index = parts[0]
        name = parts[1]
        phase = PhaseCode.from_string(parts[2])
        ccbm = parts[3]
        status = Contact.from_string(parts[4])
        return Digital(cfg_index=index, name=name, phase=phase, ccbm=ccbm, contact=status)
    raise ValueError("数字通道信息格式错误")
