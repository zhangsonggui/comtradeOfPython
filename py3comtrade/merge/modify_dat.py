#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np


class ModifyDat:
    """
    修改dat文件数据
    """

    # TODO: 进行通道的选择
    # TODO: 进行采样点范围的选择
    # TODO: 指定通道、指定采样点范围幅值按比例变化，默认为1
    # TODO: 保存文件格式，ASCII、BINARY、BINARY32、CSV

    def __init__(self, dat: np.ndarray, modify_analogs: list = None, modify_digitals: list = None):
        self._dat = dat
