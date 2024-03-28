#!/usr/bin/python3
# _*_ coding: utf-8 _*_
#
# Copyright (C) 2024 - 2024 张松贵, Inc. All Rights Reserved
#
# @Time    : 2024/3/23 11:27
# @Author  : 张松贵
# @File    : CFG2DMF.py
# @IDE     : PyCharm
from comtradeParser.utils import constants
from comtradeParser.cfg.CFGParser import CFGParser


class CFG2DMF:
    """
    将cfg文件中的通道信息转换为模型文件
    """
    _cfg = None
    _analog_name = []
    _analog_ccbms = []
    _accbm = []

    def __init__(self, cfg: CFGParser):
        """
        cfg2dmf构造函数
        @param cfg: cfg文件对象
        """
        self._cfg = cfg

    def clear(self):
        """
        清除类内部的私有变量
        """
        self._cfg = None

    def _extract_use_group_name_from_cfg(self):
        self.analog_names = self._cfg.get_channel_info(key="chid")
        self.analog_ccbms = self._cfg.get_channel_info(key="ccbm")
        # 每隔4个通道为一组，循环读取通道名称
        for i in range(0, len(self.analog_names), 4):
            # 当通道名称包含关键字时，跳过
            if self.analog_names[i] in constants.NAME_MASKEY:
                continue
            for j in range(i, i + 4):
                # 当监视元件包含关键字时认为监视元件无效，选择4个通道中的第一个通道为监视元件名称
                if self.analog_ccbms[j] in constants.CCBM_MASKEY:
                    self.analog_ccbms[j] = self.analog_names[i]
        ccbm = list(set(self.analog_ccbms))
        return ccbm.sort(key=self.analog_ccbms.index)
