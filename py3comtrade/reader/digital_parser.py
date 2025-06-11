#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..model import Digital
from ..model.type import Contact
from ..model.type import PhaseCode


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

    # 如果字符串中有三个部分，则生成Digital对象
    if len(parts) ==3:
        index = parts[0]
        name = parts[1]
        status = Contact.from_string(parts[2])
        return Digital(cfg_index=index, name=name, contact=status)
    # 如果字符串中有五个部分，则生成Digital对象
    if len(parts) == 5:
        index = parts[0]
        name = parts[1]
        phase = PhaseCode.from_string(parts[2])
        ccbm = parts[3]
        status = Contact.from_string(parts[4])
        return Digital(cfg_index=index, name=name, phase=phase, ccbm=ccbm, contact=status)
    # 如果字符串中的部分数量不符合要求，则抛出异常
    raise ValueError("数字通道信息格式错误")
