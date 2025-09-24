#!/usr/bin/env python
# -*- coding: utf-8 -*-

from py3comtrade.model.digital import Digital
from py3comtrade.model.type.digital_enum import Contact
from py3comtrade.model.type.phase_code import Phase


def digital_parser(_line_str):
    """
    从一行文本字符串中生成数字通道对象
    :param _line_str: 配置文件中一行数字通道字符串
    :return: 数字通道对象
    """
    line = _line_str.strip()
    # 去除字符串两端的空格
    if not line:
        # 如果字符串为空，抛出异常
        raise ValueError("开关量信息为空")
    parts = line.split(",")
    parts_num = len(parts)

    # 初始化字段值
    index = None
    name = None
    phase = Phase.NO_PHASE
    ccbm = ""
    status = Contact.NORMALLY_OPEN
    # 按照顺序填充字段
    if parts_num >= 1:
        index = parts[0]
    if parts_num >= 2:
        name = parts[1]
    if parts_num >= 3:
        if parts_num == 3 and parts[2] == '1':
            status = Contact.NORMALLY_CLOSED
        if parts_num >= 3:
            phase = Phase.from_string(parts[2], default=Phase.NO_PHASE)
        if parts_num >= 4:
            ccbm = parts[3]
        if parts_num >= 5 and parts[4] == '1':
            status = Contact.NORMALLY_CLOSED

    return Digital(idx_cfg=index, name=name, phase=phase, ccbm=ccbm, contact=status)
