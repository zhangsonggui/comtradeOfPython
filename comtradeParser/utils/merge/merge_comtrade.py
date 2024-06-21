#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np

from comtradeParser.ComtradeParser import ComtradeParser
from comtradeParser.cfg.cfg_parser import CfgParser
from comtradeParser.cfg.fault_time import generate_fault_time_str
from comtradeParser.cfg.sample_info import generate_sample_info_str
from comtradeParser.utils.file_tools import file_finder
from comtradeParser.utils.merge.modify_channel import ModifyChannel
from comtradeParser.cfg.analog_channel import generate_analog_channel_str
from comtradeParser.cfg.digital_channel import generate_digital_channel_str


class MergeComtrade():
    """
    合并comtrade文件
    """

    def __init__(self, directory: str, extension: str = '.cfg', cfg_path: list = None):
        """
        初始化类
        :param directory: comtrade文件所在目录
        :param extension: comtrade文件扩展名，默认为.cfg
        :param cfg_path: 要合并文件的cfg文件路径列表，默认为空。
        """
        if cfg_path is not None:
            self._cfg_files = cfg_path
        elif directory is not None:
            self._cfg_files = file_finder(directory, extension)
        else:
            raise Exception("没有选择文件！")

    @property
    def cfg_files(self):
        return self._cfg_files

    @cfg_files.setter
    def cfg_files(self, value):
        self._cfg_files = value

    def merge_cfg_data(self, modify_analogs: list = None, modify_digitals: list = None):
        """
        :param modify_analogs: 模拟量修改信息，默认为空，表示不修改模拟量通道，列表元素为字典，key为属性名，value为属性值
        :param modify_digitals: 开关量修改信息，默认为空，表示不修改模拟量通道，列表元素为字典，key为属性名，value为属性值
        """
        cfg_new = None
        for idx, cfg_path in enumerate(self.cfg_files):
            cfg = CfgParser(cfg_path)
            mc = ModifyChannel(cfg, modify_analogs, modify_digitals)
            if idx == 0:
                cfg_new = mc.cfg
            else:
                cfg_new.analog_channels.extend(mc.analog_channels)
                cfg_new.digital_channels.extend(mc.digital_channels)
        for idx, an in enumerate(cfg_new.analog_channels):
            an.an = idx + 1
        return cfg_new

    def merge_dat_data(self, modify_analogs: list = None, modify_digitals: list = None):
        """
        todo:要实现合并通道数量，采样点范围，要修改那几个通道的幅值
        :param modify_analogs: 模拟量修改信息，默认为空，表示不修改模拟量通道，列表元素为字典，key为属性名，value为属性值
        :param modify_digitals: 开关量修改信息，默认为空，表示不修改模拟量通道，列表元素为字典，key为属性名，value为属性值
        """
        sszs = []
        for idx, cfg_file in enumerate(self.cfg_files):
            record = ComtradeParser(cfg_file)  # 解析cfg文件
            an = record.cfg.get_channel_info(key='_an')  # 获取所有通道信息，后续通过界面获取
            samp_times = record.get_sample_relativetime_list()
            if idx == 0:
                sszs.append(samp_times)
            ssz = record.get_analog_ssz(an, primary=True)
            sszs.append(ssz)
        sszs = np.concatenate(sszs)
        return sszs.T

    def cfg_to_file(self, cfg: CfgParser, filename: str):
        pass
        # with open(filename, 'w', encoding='gbk') as f:
        # f.write(cfg.header_to_string())
        # f.write('\n')
        # f.write(cfg.channel_to_string())
        # f.write('\n')
        # for channel in cfg.analog_channels:
        #     f.write(generate_analog_channel_str(channel))
        #     f.write('\n')
        # for digital in cfg.digital_channels:
        #     f.write(generate_digital_channel_str(digital))
        #     f.write('\n')
        # f.write(generate_sample_rate_info_str(cfg.sample_rate_segments))
        # f.write(generate_fault_time_str(cfg.fault_time))
        # f.write('\n')
        # f.write(cfg.data_format_type)
        # f.write('\n')
        # f.write(str(cfg.timemult))
        # return f'{filename}文件生成成功！'

    def dat_to_file(self, dat: np.ndarray, filename: str):
        pass
