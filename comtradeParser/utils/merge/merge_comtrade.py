#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np

from comtradeParser.cfg.cfg_parser import CfgParser
from comtradeParser.fault_record import FaultRecord
from comtradeParser.utils.file_tools import file_finder


def read_cfgs(directory: str, extension: str = '.cfg'):
    """
    读取指定目录下的cfg文件目录，并将文件实例化
    :return:cfg实例化对象的数组
    """
    cfg_files = file_finder(directory, extension)
    cfgs = []
    for cfg_file in cfg_files:
        item = {
            "file_name": cfg_file,
            "cfg": CfgParser(cfg_file)
        }
        cfgs.append(item)
    return cfgs


class MergeComtrade:
    """
    合并comtrade文件
    """

    def __init__(self, directory: str, extension: str = '.cfg'):
        """
        初始化类
        :param directory: comtrade文件所在目录
        :param extension: comtrade文件扩展名，默认为.cfg
        """
        self._cfgs = read_cfgs(directory, extension)

    @property
    def cfgs(self):
        return self._cfgs

    @cfgs.setter
    def cfgs(self, value):
        self._cfgs = value

    def merge_cfg_data(self):
        """
        合并cfg文件
        """
        merge_cfg: CfgParser = None
        for idx, cfg in enumerate(self.cfgs):
            # 将要修改的通道信息传入通道修改类中
            cfg = cfg.get('cfg')
            # 第一个文件返回cfg全部对象
            if idx == 0:
                merge_cfg = cfg
            # 第二个以后的文件只返回模拟量通道信息和开关量信息
            else:
                merge_cfg.analog_channels.extend(cfg.analog_channels)
                merge_cfg.digital_channels.extend(cfg.digital_channels)
        # 统一修改合并后cfg文件的模拟量通道编号,从1开始编号
        merge_cfg.fault_header.analog_channel_num = merge_cfg.analog_channel_num
        merge_cfg.fault_header.digital_channels_num = merge_cfg.digital_channel_num
        merge_cfg.fault_header.channel_total_num = merge_cfg.analog_channel_num + merge_cfg.digital_channel_num
        for idx, an in enumerate(merge_cfg.analog_channels):
            an.an = idx + 1
        # 统一修改合并后cfg文件的开关模拟量通道编号,从1开始编号
        for idx, dn in enumerate(merge_cfg.digital_channels):
            dn.dn = idx + 1
        return merge_cfg

    def merge_dat_data(self):
        """
        todo:要实现合并通道数量，采样点范围，要修改那几个通道的幅值
        """
        merge_ssz = []
        for idx, cfg in enumerate(self.cfgs):
            # TODO: 该处应该接收modify_analogs和modify_digitals两个列表中的参数，临时直接获取全部的通道
            file_name = cfg.get('file_name')
            fr = FaultRecord(file_name)  # 解析cfg文件
            an = fr.cfg.get_channel_info(key='an')  # 获取所有通道信息，后续通过界面获取
            samp_times = fr.get_sample_relative_time_list()
            if idx == 0:
                merge_ssz.append(samp_times)
            ssz = fr.get_analog_ssz(an, primary=True)
            merge_ssz.append(ssz)
        merge_ssz = np.concatenate(merge_ssz)
        return merge_ssz.T
