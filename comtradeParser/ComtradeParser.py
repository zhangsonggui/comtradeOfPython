#!/usr/bin/python3
# _*_ coding: utf-8 _*_
#
# Copyright (C) 2024 - 2024 张松贵, Inc. All Rights Reserved
#
# @Time    : 2024/3/23 11:27
# @Author  : 张松贵
# @File    : ComtradeParser.py
# @IDE     : PyCharm
import cmath
import math
import os
from typing import Union

import numpy as np

from comtradeParser.cfg.CFGParser import CFGParser
from comtradeParser.computation.fourier import dft_rx, dft_exp_decay
from comtradeParser.computation.sequence import phasor_to_sequence
from comtradeParser.dat.DATParser import DATParser
from comtradeParser.dmf.ChannelGroupParser import ChannelGroupParser
from comtradeParser.dmf.DMFParser import DMFParser


class ComtradeParser:
    cfg = None
    _dat = None
    _dmf = None
    cgp = None

    def __init__(self, _file_name: str):
        """
        comtrade文件读取初始化
        @param _file_name: 录波文件名
        """
        _name, _suffix = _file_name.rsplit('.', 1)
        self.clear()
        self._load_cfg_dat_file(_name)
        self._load_dmf_file(_name)
        self.cgp = ChannelGroupParser(self.cfg, self._dmf)

    def clear(self):
        """
        清除类内部的私有变量
        @return:
        """
        self.cfg = None
        self._dat = None
        self._dmf = None
        self.cgp = None

    @staticmethod
    def _check_file_with_suffix(file_name: str, suffix: str) -> str:
        """
        检查文件是否存在
        @param file_name: 文件名，不含后缀
        @param suffix: 后缀名
        @return: 存在返回文件名，不存在返回空
        """
        full_file_name = file_name + '.' + suffix
        if os.path.isfile(full_file_name):
            return full_file_name
        else:
            return ''

    def _load_cfg_dat_file(self, file_name: str):
        """
        判断是否存在cfg和dat文件
        @param file_name: 文件名，不含后缀
        """
        cfg_file = self._check_file_with_suffix(file_name, "cfg")
        dat_file = self._check_file_with_suffix(file_name, "dat")
        if cfg_file != '' and dat_file != '':
            self.cfg = CFGParser(cfg_file)
            self._dat = DATParser(self.cfg, dat_file)
        else:
            raise FileNotFoundError(f"{file_name}文件不存在！")

    def _load_dmf_file(self, file_name: str):
        """
        判断是否存在dmf文件
        :param file_name: 文件名，含后缀
        """
        dmf_file = self._check_file_with_suffix(file_name, "dmf")
        if dmf_file != '':
            self._dmf = DMFParser(dmf_file)

    def get_analog_ysz(self, ch_number: Union[int, list],
                       start_point: int = 0, end_point: int = None,
                       cycle_num: int = None, mode=1) -> np.ndarray:
        """
        读取指定模拟量通道、采样点的原始值数组。
        :param ch_number: CFG文件中的通道序号或列表
        :param start_point: 采样起始点，默认为0
        :param end_point: 采样终止点，不含终止点，默认为None 代表全部采样点
        :param cycle_num: 采样周波数量，当end_point为空时生效
        :param mode: 取值模式，仅在按周波取值时生效，默认为1：代表向采样点后方取值，-1：代表向采样点前方取值，0：代表向采样点两边取值
        :return: 返回一个二维数组，一维是通道，二维是各采样点的原始值数组
        """
        if isinstance(ch_number, int):
            ch_number = [ch_number]
        start_point, end_point, samp_point = self.cfg.get_cursor_sample_range(start_point, end_point, cycle_num, mode)
        values = np.zeros((len(ch_number), samp_point))
        for i, ch in enumerate(ch_number):
            values[i] = self._dat.get_analog_ysz_from_channel(ch)[start_point:end_point + 1]
        return values

    def get_analog_ssz(self, ch_number: Union[int, list], primary: bool = False,
                       start_point: int = 0, end_point: int = None,
                       cycle_num: int = None, mode=1) -> np.ndarray:
        """
        读取指定模拟量通道、采样点的瞬时值数组,
        当end_point和cycle_num同时为空时，获取全部采样点，
        当end_point不为空，以end_point采样点为准，
        当end_point采样点为空，cycle_num不为空时按周波数量整周波取值
        :param ch_number: CFG文件中的通道序号或列表
        :param primary: 输出值类型是一次值还是二次值，默认为False，二次值
        :param start_point: 采样起始点，默认为0
        :param end_point: 采样终止点，不含终止点，默认为None 代表全部采样点
        :param cycle_num: 采样周波数量，当end_point为空时生效
        :param mode: 取值模式，仅在按周波取值时生效，默认为1：代表向采样点后方取值，-1：代表向采样点前方取值，0：代表向采样点两边取值
        :return: 返回一个二维数组，一维是通道，二维是各采样点的瞬时值数组
        """
        if isinstance(ch_number, int):
            ch_number = [ch_number]
        start_point, end_point, samp_point = self.cfg.get_cursor_sample_range(start_point, end_point, cycle_num, mode)
        values = np.zeros((len(ch_number), samp_point))
        for i, ch in enumerate(ch_number):
            values[i] = self._dat.get_analog_ssz_from_channel(ch, primary)[start_point:end_point + 1]
        return np.around(values, 3)

    def get_analog_yxz(self, vs: np.ndarray = None, sample_rate: int = None, **kwargs) -> np.ndarray:
        """
        获取模拟量通道当前游标位置整周波的有效值
        :param vs: 一个周波的瞬时值数组
        :param sample_rate: 采样率，默认为None，从CFG文件中获取
        :return 返回有效值列表，索引序号和ch_number对应
        """
        if vs is None:
            vs = self.get_analog_ssz(kwargs.get('ch_number'), kwargs.get('primary'), kwargs.get('start_point'),
                                     kwargs.get('end_point'), kwargs.get('cycle_num'), kwargs.get('mode'))
        yxz = np.zeros(vs.shape[0])
        if not isinstance(vs, np.ndarray) and sample_rate != vs.shape[1]:
            raise ValueError("输入的瞬时值数组vs必须是采样率为{}的numpy数组".format(sample_rate))
        phasor = self.get_analog_phasor(vs)
        for index, item in enumerate(phasor):
            yxz[index] = abs(item)
        return np.around(yxz, 3)

    def get_analog_angle(self, vs: np.ndarray = None, sample_rate: int = None, **kwargs) -> np.ndarray:
        """
        获取模拟量通道当前游标向后的角度值
        :param vs: 一个周波的瞬时值数组
        :param sample_rate: 采样率，默认为None，从CFG文件中获取
        :return: 各通道的有效值列表
        """
        if vs is None:
            vs = self.get_analog_ssz(kwargs.get('ch_number'), kwargs.get('primary'), kwargs.get('start_point'),
                                     kwargs.get('end_point'), kwargs.get('cycle_num'), kwargs.get('mode'))
        angle = np.zeros(vs.shape[0])
        if not isinstance(vs, np.ndarray) and sample_rate != vs.shape[1]:
            raise ValueError("输入的瞬时值数组vs必须是采样率为{}的numpy数组".format(sample_rate))
        _dft_rx = self.dft_rx_channels(vs)
        for index, item in enumerate(_dft_rx):
            # 计算并获取复数的角度（以弧度表示）
            angle_radians = cmath.phase(item)
            angle_degrees = angle_radians * 180 / math.pi
            angle[index] = angle_degrees
        return np.around(angle, 3)

    def get_analog_phasor(self, vs: np.ndarray = None, sample_rate: int = None, **kwargs) -> list:
        """
        获取模拟量通道当前游标位置的相量值
        :param vs: 一个周波的瞬时值数组
        :param sample_rate: 采样率，默认为None，从CFG文件中获取
        :return 返回相量值列表，索引序号和ch_number对应
        """
        if vs is None:
            vs = self.get_analog_ssz(kwargs.get('ch_number'), kwargs.get('primary'), kwargs.get('start_point'),
                                     kwargs.get('end_point'), kwargs.get('cycle_num'), kwargs.get('mode'))
        if not isinstance(vs, np.ndarray) and sample_rate != vs.shape[1]:
            raise ValueError("输入的瞬时值数组vs必须是采样率为{}的numpy数组".format(sample_rate))
        _dft_rx = self.dft_rx_channels(vs)
        phasor = _dft_rx / np.sqrt(2.0)
        return phasor

    def get_channel_xfl_phasor(self, vs: np.ndarray = None, decay_dc: bool = False, **kwargs):
        """
        计算序分量
        :param vs: 瞬时值数组
        :param decay_dc: 是否过滤直流分量
        :return: 返回一个数组，正序、负序、零序分量值
        """
        if vs is None:
            vs = self.get_analog_ssz(kwargs.get('ch_number'), kwargs.get('primary'), kwargs.get('start_point'),
                                     kwargs.get('end_point'), kwargs.get('cycle_num'), kwargs.get('mode'))
        xfl = []
        if decay_dc:
            _dft_rx = self.eliminate_exp_decay_channels(vs)
        else:
            _dft_rx = self.dft_rx_channels(vs)
        if vs.shape[0] % 3 == 0:
            for i in range(0, vs.shape[0], 3):
                xfl.append(phasor_to_sequence(_dft_rx[i:i + 3]))
        else:
            raise ValueError('通道数量必须是3的倍数')
        return np.around(xfl, 3)

    def get_channel_xfl_magnitude(self, vs: np.ndarray = None, **kwargs):
        """
        计算序分量模值
        :param vs:
        :return: 返回一个数组，正序、负序、零序分量值
        """
        magnitude = []
        if vs is None:
            vs = self.get_channel_xfl_phasor(**kwargs)
        for item in vs:
            magnitude.append(abs(item))
        return np.around(magnitude, 3)

    def get_digital_ssz(self, ch_number: Union[int, list],
                        start_point: int = 0, end_point: int = None,
                        ) -> np.ndarray:
        """
        获取指定数字通道的采样值
        :param ch_number: CFG文件中的通道序号列表
        :param start_point: 开始采样点，默认0，第一个采样点
        :param end_point: 结束采样点，默认None，全部采样点的数据
        :return: 指定数字通道的采样值
        """
        if isinstance(ch_number, int):
            ch_number = [ch_number]
        start_point, end_point, samp_point = self.cfg.get_cursor_sample_range(start_point, end_point)
        values = np.zeros((len(ch_number), samp_point))
        for i, ch in enumerate(ch_number):
            values[i] = self._dat.get_digital_ssz_from_channel(ch)[start_point:end_point + 1]
        return values

    def get_digital_change(self, ch_number: Union[int, list]):
        """
        获取指定数字通道的波形变化
        :param ch_number: CFG文件中的通道序号列表
        :return: 指定数字通道的波形变化二维数组,一维是通道，二维是每次变化的字典信息，含所在列表的索引和值
        """
        if isinstance(ch_number, int):
            ch_number = [ch_number]
        value = []
        for i in ch_number:
            sc = self._dat.get_digital_shift_stat_channel(i)
            value.append(sc)
        return value

    def get_digital_shift_channels(self):
        """
        获取发生变位的数组通道数组
        :return:
        """
        dsc = []
        dns = self.cfg.get_channel_info(key='dn', _type='dig')
        dc = self.get_digital_change(dns)
        for index, value in enumerate(dc):
            if len(value) > 1:
                dsc.append(index)
        return dsc

    @staticmethod
    def dft_rx_channels(vs: np.ndarray) -> np.ndarray:
        """
        提供多个通道的傅里叶计算实部和虚部
        @param vs: 一个二维的numpy数组，一维是通道，二维是指定周期的瞬时值
        @return:返回一个二维数组，一维是通道列表，二维是实部虚部元祖
        """
        if not isinstance(vs, np.ndarray):
            raise Exception('vs必须为np.ndarray类型')
        dft = np.zeros(vs.shape[0], dtype=complex)
        # 获取一个周波的瞬时值
        for i in range(vs.shape[0]):
            # 进行傅里叶计算，获取实部和虚部
            dft[i] = dft_rx(vs[i], vs.shape[1], 1)
        return dft

    @staticmethod
    def eliminate_exp_decay_channels(vs: np.ndarray, sample_rate: int = None):
        """
        消除直流分量后返回对应通道的实部和虚部，需要1.5个周波的数据。
        1.[ (第三组点的实部+第二组点的虚部)/(第一组点的虚部+第二组点的实部) ] 的平方，把这个数记为a;
        2.通过第一步的运算结果a，求K1和K2，k1是 (第一组点的实部+第三组点的实部)/ (1+a):k2是(第一组点的虚部+第三组点的虚部) / (1+0).
        3.求修改后的基波分量实部和虚部，实部=第一组点的实部-k1: 虚部= 第二组点的虚部-k2
        :param vs: 瞬时值数组
        :param sample_rate:
        :return: 返回一个二维数组，一维是通道列表，二维是实部虚部元祖
        """
        dft = np.zeros(vs.shape[0], dtype=complex)
        # 获取一个周波的瞬时值
        for i in range(vs.shape[0]):
            dft[i] = dft_exp_decay(vs[i], sample_rate)
        return dft
