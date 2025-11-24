#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据解析工具函数模块
包含通用的数据类型转换和解析功能
"""


def _convert_to_float(value, default=0.0, key=None):
    """
    内部通用浮点数转换函数
    
    :param value: 要转换的值
    :param default: 当值为None或空字符串时的默认值
    :param key: 可选的键名，用于错误信息
    :return: 转换后的浮点数
    :raises ValueError: 当值无法转换为浮点数时
    """
    # 处理空字符串和None
    if value is None or (isinstance(value, str) and not value.strip()):
        return default

    try:
        return float(value)
    except (ValueError, TypeError):
        # 根据是否提供key生成适当的错误信息
        if key is not None:
            raise ValueError(f"无法将'{key}'的值 '{value}' 转换为浮点数")
        else:
            raise ValueError(f"无法将'{value}'转换为浮点数")


def safe_float_convert(value, key, default=0.0):
    """
    安全地将值转换为浮点数
    
    :param value: 要转换的值
    :param key: 键名，用于错误信息
    :param default: 当值为None时的默认值
    :return: 转换后的浮点数
    :raises ValueError: 当值无法转换为浮点数时
    """
    return _convert_to_float(value, default=default, key=key)


def parse_float(value, default=0.0):
    """
    解析字符串值为浮点数，处理空字符串情况
    
    :param value: 要解析的字符串值
    :param default: 当值为空字符串或无法转换时的默认值
    :return: 解析后的浮点数
    :raises ValueError: 当值非空但无法转换为浮点数时
    """
    return _convert_to_float(value, default=default, key=None)
