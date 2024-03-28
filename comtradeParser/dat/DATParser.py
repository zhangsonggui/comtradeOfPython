#!/usr/bin/python3
# _*_ coding: utf-8 _*_
#
# Copyright (C) 2024 - 2024 张松贵, Inc. All Rights Reserved
#
# @Time    : 2024/3/23 11:27
# @Author  : 张松贵
# @File    : ReadFaultFile.py
# @IDE     : PyCharm
import logging
import struct

import numpy as np

from comtradeParser.cfg.CFGParser import CFGParser


class DATParser:
    """
    这是用于读取IEEE Comtrade dat文件的python类
    可以解析ASCII、BINARY、BINARY32格式类型
    提供原始采样值、瞬时值的读取
    """
    _cfg = None
    _file_handler = 0  # 文件处理
    _dat_file_content = None  # dat文件内部变量
    _ft = ''  # dat文件格式类型
    _bit_width = 2  # 二进制位数，和录波文件格式有关
    _NB = 0  # 每个采样点的字节数
    _AB = 0  # 模拟量单采样点字节数
    _DB = 0  # 开关量单采样点字节数
    _N = 0  # 总采样点数
    _A = 0  # 模拟量通道数
    _D = 0  # 数字量通道数

    def __init__(self, cfg: CFGParser, dat_name):
        """
        DATParser构造函数：
        :param cfg: 与dat文件匹配的cfg文件对象
        :param dat_name: dat文件路径
        """
        logging.info("初始化解析{}文件实例!".format(dat_name))
        self.clear()
        self._load_cfg_parm(cfg)
        self._read_datafile(dat_name)

    def clear(self):
        self._cfg = None  # 清空cfg文件对象
        self._file_handler = 0  # 清空文件处理
        self._dat_file_content = None  # 清空数据文件内容
        self._ft = ''  # 清空文件格式类型
        self._bit_width = 2  # 二进制位数设为2
        self._NB = 0  # 清空每个采样点字节数
        self._AB = 0  # 模拟量单采样点字节数
        self._DB = 0  # 开关量单采样点字节数
        self._N = 0  # 清空采样点总数
        self._A = 0  # 清空模拟量通道数
        self._D = 0  # 清空开关量通道数

    def _load_cfg_parm(self, cfg: CFGParser):
        """
        解析cfg文件，获取采样点数、模拟量通道数、数字量通道数
        :param cfg: cfg文件对象
        :return: 无
        """
        if not isinstance(cfg, CFGParser):
            raise ValueError("CFG文件对象类型错误，无法解析DAT文件!")
        self._cfg = cfg
        self._A = self._cfg.get_analog_channel_num()
        self._D = self._cfg.get_digital_channel_num()
        # 获取每个周波占用的字节数
        self._ft, self._bit_width = self._cfg.get_data_format_type()
        self._AB = self._A * self._bit_width
        self._DB = int(np.ceil(float(self._D) / float(16)))
        # 获取每个周波占用的字节数
        self._NB = (4 + 4 + self._AB + self._DB * 2)
        # 获取总采样点数
        self._N = self._cfg.get_sample_num()

    def _read_datafile(self, file_name):
        """
        读取DAT文件，并将内容存入在私有变量
        访问特定的通道数据，请参照getAnalogChannelData和getDigitalChannelData方法
        """
        # 判断DAT文件的格式
        if self._ft == "ascii":
            self._file_handler = open(file_name, 'r')
            self._dat_file_content = np.loadtxt(self._file_handler, delimiter=',').T
        else:
            self._file_handler = open(file_name, 'rb')
            self._dat_file_content = self._file_handler.read()
        # 关闭DAT文件
        self._file_handler.close()
        logging.info('解析{}文件成功,关闭文件'.format(file_name))

    def get_analog_ysz_from_channel(self, ch_number: int) -> np.ndarray:
        """
        读取单个模拟量通道所有原始采样值
        @param ch_number: CFG文件中的通道序号an
        @return: 单个模拟量原始采样值数组
        """
        # 判断采样通道的合法性,获取通道对应数组的索引值
        if not isinstance(ch_number, int):
            try:
                ch_number = int(ch_number)
            except ValueError:
                raise ValueError(f"指定的模拟量通道{ch_number}不是数字类型，无法读取该通道数据!")
        if ch_number > self._A:
            raise ValueError(f"指定的模拟量通道{ch_number}大于模拟量通道{self._A}，无法读取该通道数据!")
        ch_number = self._cfg.get_channel_info(ch_number, 'index')

        # 判断文件格式，进行解析
        if self._ft == 'ascii':
            values = self._dat_file_content[ch_number:ch_number + 1, :]
        else:
            # 使用struct模块格式化字节
            str_struct = f"ii{self._A + self._DB}h"
            # 创建空的数组，指定开始点位、结束点位、采样数量，不包含结束点位
            values = np.zeros(self._N, dtype=np.int16)
            # 从DatFileContent中读取指定采样范围数据
            for i in range(self._N):
                data = struct.unpack(str_struct, self._dat_file_content[i * self._NB:(i * self._NB) + self._NB])
                values[i] = data[ch_number + 2]  # 前两个数字是采样点索引和时间戳
        return values

    def get_analog_ssz_from_channel(self, ch_number: int, primary: bool = False) -> np.ndarray:
        """
        读取单个模拟量通道全部采样点瞬时值
        @param ch_number: CFG文件中的通道序号an
        @param primary: 输出值类型是一次值还是二次值，默认为False二次值
        @return: 单个模拟量瞬时值数组
        """
        # 判断采样通道的合法性
        if not isinstance(ch_number, int):
            try:
                ch_number = int(ch_number)
            except ValueError:
                raise ValueError(f"指定的模拟量通道{ch_number}不是数字类型，无法读取该通道数据!")
        if ch_number > self._A:
            raise ValueError(f"指定的模拟量通道{ch_number}大于模拟量通道{self._A}")
        # 获取指定通道的原始采样值
        vs = self.get_analog_ysz_from_channel(ch_number)
        # 利用numpy的乘法和加法运算获取瞬时值
        ssz = vs * self._cfg.get_channel_info(ch_number, 'a') + self._cfg.get_channel_info(ch_number, 'b')
        # 获取通道的变比，避免重复计算
        ratio = self._cfg.get_analog_ratio(ch_number)
        # 获取通道是否一次值
        ch_primary = self._cfg.is_primary_analog(ch_number)
        if primary:
            result = ssz if ch_primary else ssz * ratio
        else:
            result = ssz / ratio if ch_primary else ssz
        return np.around(result, 3)

    def get_digital_ssz_from_channel(self, ch_number: int) -> list:
        """
        返回指定状态量通道的瞬时值数组
        @param ch_number: CFG文件中的通道序号
        @return: 指定通道0和1的数组
        """
        # 判断采样通道的合法性，获取通道对应数组的索引值
        if not isinstance(ch_number, int):
            try:
                ch_number = int(ch_number)
            except ValueError:
                raise ValueError(f"指定的模拟量通道{ch_number}不是数字类型，无法读取该通道数据!")
        if ch_number > self._D:
            raise ValueError("指定的开关量通道数大于开关量通道数")
        ch_number = self._cfg.get_channel_info(ch_number, 'index', 'dig')

        # 判断文件格式，进行解析
        if self._ft == 'ascii':
            values = self._dat_file_content[ch_number:ch_number + 1, :]
        else:
            # 使用struct模块格式化字节
            str_struct = f"ii{self._A}h{self._DB}H"
            # 创建一个空数组
            values = np.zeros(self._N, dtype=np.int16)
            # values = np.empty((self._N, 1), dtype=np.int16)
            # 每一个字节都包含了16个数字通道
            byte_number = ch_number // 16 + 1
            # 数字通道的值
            digital_ch_value = (1 << (ch_number - (byte_number - 1) * 16))
            # 从DatFileContent中读取字符串
            for i in range(self._N):
                data = struct.unpack(str_struct, self._dat_file_content[i * self._NB:(i * self._NB) + self._NB])
                values[i] = (digital_ch_value & data[self._A + 2 + byte_number - 1]) * 1 / digital_ch_value
        return values

    def get_digital_shift_stat_channel(self, ch_number: int):
        """
        获取单个开关量的变位情况
        @return: 返回变位的开关量列表
        """
        # 判断采样通道的合法性，获取通道对应数组的索引值
        if not isinstance(ch_number, int):
            try:
                ch_number = int(ch_number)
            except ValueError:
                raise ValueError(f"指定的模拟量通道{ch_number}不是数字类型，无法读取该通道数据!")
        if ch_number > self._D:
            raise ValueError("指定的开关量通道数大于开关量通道数")
        result = []
        ssz = self.get_digital_ssz_from_channel(ch_number)
        for i, val in enumerate(ssz):
            if i == 0 or ssz[i - 1] != val:
                result.append({"index": i, "value": val})
        return result
