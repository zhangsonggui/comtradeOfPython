#!/usr/bin/python3
# _*_ coding: utf-8 _*_
#
# Copyright (C) 2024 - 2024 张松贵, Inc. All Rights Reserved
#
# @Time    : 2024/3/23 11:27
# @Author  : 张松贵
# @File    : channel_to_group.py
# @IDE     : PyCharm
import logging

from py3comtrade.parser.cfg_parser import CfgParser
from py3comtrade.parser.dmf_parser import DmfParser


class ChannelGroupParser:
    """
    解析通道分组信息
    """
    _MASKEY = ["高频", "模拟量", "高抗", "电抗", "单量", "母联", "分段", "开关量", "电压", "电流"]
    _cfg = None
    _dmf = None
    _lines_model = []  # 线路分组信息
    _lines_name = []  # 线路名称分组
    _buses_model = []  # 母线分组信息
    _buses_name = []  # 母线名称分组
    _trans_model = []  # 主变分组信息
    _trans_name = []  # 主变名称分组

    def __init__(self, cfg: CfgParser, dmf: DmfParser):
        """
        初始化通道分组信息
        @param cfg: cfg文件对象
        @param dmf: dmf文件对象
        """
        logging.info("初始化通道分组信息")
        self.clear()
        self._cfg = cfg
        self._dmf = dmf
        if self._dmf is None:
            self._load_configuration_from_cfg()
        else:
            self._load_configuration_from_dmf()

    def clear(self):
        """
        清除已有的通道分组信息
        """
        self._cfg = None
        self._dmf = None
        self._lines_model = []
        self._lines_name = []
        self._buses_model = []
        self._buses_name = []

    def _load_configuration_from_dmf(self):
        """
        从DMF文件中加载配置信息
        """
        self._load_line_from_dmf()
        self._load_bus_from_dmf()
        self._load_trans_from_dmf()

    def _load_line_from_dmf(self):
        """
        从DMF文件中加载线路信息
        """
        lines = self._dmf.get_lines_name()
        lines_name = []
        lines_model = []
        for line in lines:
            line_idx = self._dmf.get_line_index(line)
            lines_name.append(line)
            lines_model.append(self._dmf.get_line(line_idx))
        self._lines_name = lines_name
        self._lines_model = lines_model

    def _load_bus_from_dmf(self):
        # 从DMF文件中加载母线信息
        buses = self._dmf.get_buses_name()
        buses_name = []
        buses_model = []
        for bus in buses:
            bus_idx = self._dmf.get_bus_index_of_name(bus)
            buses_name.append(bus)
            buses_model.append(self._dmf.get_bus(bus_idx))
        self._buses_name = buses_name
        self._buses_model = buses_model

    def _load_trans_from_dmf(self):
        """
        从DMF文件中加载主变信息
        """
        pass

    def _load_configuration_from_cfg(self):
        """
        从cfg文件中加载配置信息
        """
        analog_names = self._cfg.get_channel_info(key="__chid")
        analog_ccbms = self._cfg.get_channel_info(key="__ccbm")
        for i in range(0, len(analog_names), 4):
            if analog_names[i] in self._MASKEY:
                continue
            for j in range(i, i + 4):
                if analog_ccbms[j] == '' or analog_ccbms[j] == 'kV' or analog_ccbms[j] == 'kA':
                    analog_ccbms[j] = analog_names[i]
        self._lines_name = list(set(analog_ccbms))
        self._lines_name.sort(key=analog_ccbms.index)

    def _load_line_from_cfg(self):
        pass

    #     for i in range(0, len(analog_names), 4):
    #         if analog_names[i] in self.MASKEY:
    #             continue
    #         for j in range(i, i + 4):
    #             if ccbms[j] == '' or ccbms[j] == 'kV' or ccbms[j] == 'kA':
    #                 ccbms[j] = analog_names[i]
    #     self._lines_name = list(set(ccbms))
    #     self._lines_name.sort(key=ccbms.index)
    #     # 循环监视通道，当通道为使用状态生成字典，添加到数组
    #     for group_name in self._lines_name:
    #         cfg_an = self.__cfg.get_analog_ccbm(group_name)
    #         if self.__cfg.get_analog_usage(cfg_an):
    #             self._lines_model.append({
    #                 "cfg_an": cfg_an,
    #                 "name": group_name,
    #                 "_type": self.__cfg.get_analog_type(cfg_an),
    #                 "isUse": True,
    #                 "accchn": self.__cfg.get_channels_group(cfg_an)
    #             })

    def _load_bus_from_cfg(self):
        pass

    def _load_trans_from_cfg(self):
        pass

    def get_lines_name(self):
        """
        获取所有线路分组名称
        @return: 线路名称数组
        """
        return self._lines_name

    def get_line_index(self, name):
        """
        根据线路名称获取对应的索引号
        @param name: 线路分组名称
        @return: 线路分组索引号
        """
        return self._lines_name.index(name)

    def get_lines_model(self, idx: int = -1):
        """
        获取线路分组信息
        @param idx: 线路索引号，默认为-1，返回所有线路分组信息
        @return: 返回指定线路分组信息
        """
        if idx == -1:
            return self._lines_model
        else:
            return [self._lines_model[idx]]

    def get_buses_name(self):
        """
        获取所有线路分组名称
        @return: 线路名称数组
        """
        return self._buses_name

    def get_bus_index(self, name):
        """
        根据母线名称获取对应的索引号
        @param name: 母线分组名称
        @return: 母线分组索引号
        """
        return self._buses_name.index(name)

    def get_buses_model(self, idx: int = -1):
        """
        获取母线分组信息
        @param idx: 母线索引号，默认为-1，返回所有线路分组信息
        @return: 返回指定母线分组信息
        """
        if idx == -1:
            return self._buses_model
        else:
            return [self._buses_model[idx]]

    def get_trans_name(self):
        """
        获取所有母线分组名称
        @return: 母线名称数组
        """
        return self._trans_name

    def get_tran_index(self, name):
        """
        根据主变名称获取对应的索引号
        @param name: 主变分组名称
        @return: 主变分组索引号
        """
        return self._trans_name.index(name)

    def get_trans_model(self, idx: int = -1):
        """
        获取母线分组信息
        @param idx: 母线索引号，默认为-1，返回所有线路分组信息
        @return: 返回指定母线分组信息
        """
        if idx == -1:
            return self._trans_model
        else:
            return [self._trans_model[idx]]
