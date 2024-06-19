#!/usr/bin/env python
# -*- coding: utf-8 -*-
from enum import Enum, auto


class DataFormatType(Enum):
    """
   数据格式类型枚举
   """
    BINARY = auto(), "binary", 2
    BINARY32 = auto(), "binary32", 4
    FLOAT32 = auto(), "binary32", 4  # 假设 FLOAT32 和 BINARY32 对应相同的逻辑
    ASCII = auto(), "ascii", 0
    UNKNOWN = auto(), "unknown", -1