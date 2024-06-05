#!/usr/bin/python3
# _*_ coding: utf-8 _*_
#
# Copyright (C) 2024 - 2024 张松贵, Inc. All Rights Reserved
#
# @Time    : 2024/3/23 11:27
# @Author  : 张松贵
# @File    : DMFParser.py
# @IDE     : PyCharm
import logging

import xmltodict


class DMFParser:
    """
    这是用于读取IEEE Comtrade dmf文件的python类
    """
    _file_handler = ''  # 文件处理
    # 1.模拟量信息
    _ans = []  # 模拟量信息数组
    # 2.开关量信息
    _dns = []  # 开关量信息数组
    # 3.母线模型信息
    _buses_model = []  # 母线模型数组
    _buses_idx = []  # 母线DMF编号
    _buses_name = []  # 母线名称
    _buses_acvchn = []  # 母线分组电压通道数组
    _buses_stachn = []  # 母线分组开关量数组
    # 4.线路模型信息
    _lines_model = []
    _lines_idx = []  # 线路DMF编号
    _lines_name = []  # 线路名称
    _lines_bus = []  # 线路关联母线ID（dmf编号）
    _lines_linlen = []  # 线路长度
    _lines_accchn = []  # 线路分组电压通道数组
    _lines_stachn = []  # 线路分组开关量数组
    _lines_rx = []  # 线路分组阻抗数组
    # 5.主变模型信息
    _trans = []  # 主变信息数组
    _trans_idx = []  # 主变DMF编号
    _trans_name = []  # 主变名称

    def __init__(self, file_name):
        """
        构造函数：初始化解析DMF文件的实例。
        @param file_name:DMF文件的路径字符串。
        """
        logging.info(f"解析{file_name}文件。")
        self.clear()
        self._parse_dmf(file_name)

    def clear(self):
        """
        清除类内部的私有变量
        @return:
        """
        # 清理母线模型信息
        self._file_handler = ''  # 文件处理
        # 1.模拟量信息
        self._ans = []  # 模拟量信息数组
        # 2.开关量信息
        self._dns = []  # 开关量信息数组
        # 3.母线模型信息
        self._buses_model = []  # 母线模型数组
        self._buses_idx = []  # 母线DMF编号
        self._buses_name = []  # 母线名称
        self._buses_acvchn = []  # 母线分组电压通道数组
        self._buses_stachn = []  # 母线分组开关量数组
        # 4.线路模型信息
        self._lines_model = []
        self._lines_idx = []  # 线路DMF编号
        self._lines_name = []  # 线路名称
        self._lines_bus = []  # 线路关联母线ID（dmf编号）
        self._lines_linlen = []  # 线路长度
        self._lines_accchn = []  # 线路分组电压通道数组
        self._lines_stachn = []  # 线路分组开关量数组
        self._lines_rx = []  # 线路分组阻抗数组
        # 5.主变模型信息
        self._trans = []  # 主变信息数组
        self._trans_idx = []  # 主变DMF编号
        self._trans_name = []  # 主变名称

    def _parse_dmf(self, file_name):
        """
        解析DMF文件
        @param file_name:DMF文件的路径字符串。
        @return:
        """
        with open(file_name, 'r', encoding='utf-8') as dmf_file:
            self._file_handler = xmltodict.parse(dmf_file.read())
            if isinstance(self._file_handler, dict) and "scl:ComtradeModel" in self._file_handler:
                self._file_handler = self._file_handler["scl:ComtradeModel"]
            else:
                logging.error(f"{dmf_file}文件结构不正确!")
                raise
        # 解析母线节点
        if isinstance(self._file_handler, dict) and "scl:Bus" in self._file_handler:
            self._parse_bus(self._file_handler["scl:Bus"])
        # 解析线路节点
        if isinstance(self._file_handler, dict) and "scl:Line" in self._file_handler:
            self._parse_line(self._file_handler["scl:Line"])
        # 解析主变节点
        if isinstance(self._file_handler, dict) and "scl:Transformer" in self._file_handler:
            self._trans = self._file_handler["scl:Transformer"]
        # 解析模拟量通道参数
        if isinstance(self._file_handler, dict) and "scl:AnalogChannel" in self._file_handler:
            self._ans = self._file_handler["scl:AnalogChannel"]
        # 解析开关量通道参数
        if isinstance(self._file_handler, dict) and "scl:StatusChannel" in self._file_handler:
            self._dns = self._file_handler["scl:StatusChannel"]

    @staticmethod
    def _get_stachn_channels(stachxml):
        """
        解析节点中开关量通道
        @param stachxml:母线中的开关量通道节点
        @return:返回开关量通道的数组
        """
        if not stachxml:
            return []
        return [int(sta.get("@idx_cfg")) for sta in stachxml]

    def _parse_bus(self, buses_xml):
        for bus_idx, bus in enumerate(buses_xml, start=1):
            # 获取母线中的电压通道
            acvchn = bus.get("scl:ACVChn")
            acvchns = [int(acvchn.get(f"@{attr}")) for attr in ["ua_idx", "ub_idx", "uc_idx", "un_idx"]]
            self._buses_acvchn.append(acvchns)
            bus_name = bus.get("@bus_name")
            self._buses_idx.append(bus_idx)  # 获取电压分组在dmf中的编号
            self._buses_name.append(bus_name)  # 获取电压分组名称
            # 获取电压分组中的开关量编号
            stachn = bus.get("scl:StaChn")
            stachns = self._get_stachn_channels(stachn)
            self._buses_stachn.append(stachns)
            # 生成母线模型
            self._buses_model.append({
                "idx": bus_idx,
                "name": bus_name,
                "type": 'V',
                "isUse": True,
                "acvchn": acvchns,
                "stachn": stachns
            })

    def _parse_line(self, lines_xml):
        """
        解析线路节点
        @param lines_xml:线路节点
        @return:
        """
        for line in lines_xml:
            # 获取线路通道信息
            line_idx = int(line.get("@idx"))
            self._lines_idx.append(line_idx)
            line_name = line.get("@line_name")
            self._lines_name.append(line_name)
            line_bus = int(line.get("@bus_ID"))
            self._lines_bus.append(line_bus)
            self._lines_linlen.append(float(line.get("@LinLen")))
            # 获取电流通道信息
            accchns = []
            if int(line.get("@bran_num")) == 1:
                branchn = line.get("scl:ACC_Bran")
                accchns = [int(branchn.get("@ia_idx")), int(branchn.get("@ib_idx")),
                           int(branchn.get("@ic_idx")), int(branchn.get("@in_idx"))]
                self._lines_accchn.append(accchns)
            else:
                pass  # 分电流模式暂时还没有遇到，暂时不解析
            # 获取开关量通道信息
            stachn = line.get("scl:StaChn")
            stachns = self._get_stachn_channels(stachn)
            self._lines_stachn.append(stachns)
            # 获取线路单位阻抗信息
            rx = line.get("scl:RX")
            rx = {'r1': rx.get("@r1"), 'x1': rx.get("@x1"),
                  'r0': rx.get("@r0"), 'x0': rx.get("@x0")}
            self._lines_rx.append(rx)
            # 生成线路模型
            bus_idx = self.get_bus_index_of_dmf_id(line_bus)
            self._lines_model.append({
                "idx": line_idx,
                "name": line_name,
                "bus_idx": line_bus,
                "bus_name": self.get_bus_name(bus_idx),
                "type": 'A',
                "isUse": True,
                "acvchn": self.get_bus_voltage_channels(bus_idx),
                "accchn": accchns,
                "stachn": stachns,
                "rx": rx
            })

    def get_line(self, index):
        """
        获取dmf中指定的线路模型
        :param index: DMF中线路的索引值
        :return: 返回指定索引的线路模型，如果索引值为-1，返回空
        """
        if index != -1:
            return self._lines_model[index]
        else:
            return None

    def get_lines_name(self):
        """
        获取dmf线路名称列表
        @return: 线路名称数组
        """
        return self._lines_name

    def get_line_index(self, name: str) -> int:
        """
        根据线路名称获取对应的索引
        @param name: 线路名称
        @return:线路所对应的索引,当传入的名称不存在返回-1
        """
        if name in self._lines_name:
            return self._lines_name.index(name)
        else:
            return -1

    def get_buses_name(self) -> list:
        """
        获取dmf中所有母线名称
        @return: 母线名称列表
        """
        return self._buses_name

    def get_bus_index_of_dmf_id(self, dmf_id: int) -> int:
        """
        根据母线编号获取母线索引位置
        @param dmf_id: 母线在dmf文件中编号，非运行编号
        @return: 母线在dmf中索引位置，母线编号错误返回-1
        """
        if dmf_id in self._buses_idx:
            return self._buses_idx.index(dmf_id)
        else:
            return -1

    def get_bus_index_of_name(self, name: str) -> int:
        """
        根据母线名称获取母线索引位置
        @param name: 母线名称
        @return: 母线在dmf中索引位置，母线编号错误返回-1
        """
        if name in self._buses_name:
            return self._buses_name.index(name)
        else:
            return -1

    def get_bus_name(self, bus_idx: int) -> str:
        """
        根据母线分组索引号获取母线名称
        @param bus_idx: 母线分组索引号
        @return: 母线名称，母线编号错误返回空
        """
        if bus_idx != -1:
            return self._buses_name[bus_idx]
        else:
            return ''

    def get_bus_voltage_channels(self, bus_idx: int) -> list:
        """
        根据母线分组索引号获取所属电压通道号
        @param bus_idx: 母线分组索引号
        @return: 母线所属电压通道号列表
        """
        if bus_idx != -1:
            return self._buses_acvchn[bus_idx]
        else:
            return []

    def get_bus(self, index):
        if index != -1:
            return self._buses_model[index]
        else:
            return None
