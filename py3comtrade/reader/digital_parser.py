#!/usr/bin/env python
# -*- coding: utf-8 -*-

from py3comtrade.model.channel.digital import Digital
from py3comtrade.model.exceptions import ComtradeDataFormatException
from py3comtrade.model.type.digital_enum import Contact
from py3comtrade.model.type.phase_code import Phase


def digital_from_str(_dn_str: str) -> Digital | None:
    """
    从一行文本字符串中生成数字通道对象
    :param _dn_str: 配置文件中一行数字通道字符串
    :return: 数字通道对象
    """
    _dn_str = _dn_str.strip().split(",")
    if len(_dn_str) < 3:
        raise ComtradeDataFormatException(f"数据格式不正确")
    parts_num = len(_dn_str)

    idx_cfg = int(_dn_str[0])
    name = _dn_str[1]
    if idx_cfg == 0 and name == "":
        return None
    phase = Phase.NO_PHASE
    ccbm = ""
    status = Contact.NORMALLY_OPEN
    if len(_dn_str) == 3 and _dn_str[2] == '1':
        status = Contact.NORMALLY_CLOSED
        return Digital(idx_cfg=idx_cfg, name=name, phase=phase, ccbm=ccbm, contact=status)
    if parts_num >= 3:
        phase = Phase.from_string(_dn_str[2], default=Phase.NO_PHASE)
    if parts_num >= 4:
        ccbm = _dn_str[3]
    if parts_num >= 5 and _dn_str[4] == '1':
        status = Contact.NORMALLY_CLOSED
    return Digital(idx_cfg=idx_cfg, name=name, phase=phase, ccbm=ccbm, contact=status)


def digital_from_dict(_dn_dict: dict) -> Digital | None:
    """从字典表生成开关量Digital对象"""
    idx_cfg = _dn_dict.get("idx_cfg", 0)
    name = _dn_dict.get("name", '')
    if idx_cfg == 0 or name == "":
        return None

    digital = Digital(
        index=_dn_dict.get("index", 0),
        idx_cfg=idx_cfg,
        name=name,
        phase=Phase.from_string(_dn_dict.get("phase", ''), default=Phase.NO_PHASE),
        ccbm=_dn_dict.get("ccbm", ''),
        contact=Contact.from_string(_dn_dict.get("contact", ''), default=Contact.NORMALLY_OPEN)
    )
    digital.values = _dn_dict.get("values", [])
    return digital
