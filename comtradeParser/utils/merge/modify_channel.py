#!/usr/bin/env python
# -*- coding: utf-8 -*-
from comtradeParser.cfg.cfg_parser import CfgParser


class ModifyChannel:
    """
    修改comtrade通道信息
    """

    def __init__(self, cfg: CfgParser, modify_analogs: list = None, modify_digitals: list = None):
        """
        根据修改列表的内容修改cfg对象
        :param cfg: cfg对象
        :param modify_analogs: 模拟量修改信息，默认为空，表示不修改模拟量通道，列表元素为字典，key为属性名，value为属性值
        :param modify_digitals: 开关量修改信息，默认为空，表示不修改模拟量通道，列表元素为字典，key为属性名，value为属性值
        """
        self.clear()
        self.cfg = self.modify_cfg(cfg, modify_analogs, modify_digitals)

    def clear(self):
        self.cfg = None

    @property
    def cfg(self):
        """
        获取cfg对象
        :return : cfg对象
        """
        return self._cfg

    @cfg.setter
    def cfg(self, cfg):
        """
        设置cfg对象
        :param cfg: cfg对象
        """
        self._cfg = cfg

    @property
    def analog_channels(self):
        """
        获取模拟量通道信息列表
        :return : 模拟量通道信息列表
        """
        return self._cfg.analog_channels

    @property
    def digital_channels(self):
        """
        获取开关量通道信息列表
        :return : 开关量通道信息列表
        """
        return self._cfg.digital_channels

    @analog_channels.setter
    def analog_channels(self, analog_channels):
        """
        设置模拟量通道信息列表
        :param analog_channels: 模拟量通道信息列表
        """
        self._cfg.analog_channels = analog_channels

    @digital_channels.setter
    def digital_channels(self, digital_channels):
        """
        设置开关量通道信息列表
        :param digital_channels: 开关量通道信息列表
        """
        self._cfg.digital_channels = digital_channels

    def modify_cfg(self, cfg: CfgParser, modify_analogs: list = None, modify_digitals: list = None):
        """
        根据修改列表的内容修改cfg对象
        :param cfg: cfg对象
        :param modify_analogs: 模拟量修改信息，默认为空，返回原通道信息，当不为空时返回列表内包含通道和要修改后的属性
        :param modify_digitals: 开关量修改信息，默认为空，返回原通道信息，当不为空时返回列表内包含通道和要修改后的属性
        :return: cfg对象
        """
        # 循环模拟量修改列表，根据修改列表的内容修改cfg对象
        if modify_analogs is not None:
            analog_channels = []
            for idx, ma in enumerate(modify_analogs):
                an = cfg.analog_channels[idx]
                for key, value in ma.items():
                    if value != getattr(an, key):
                        setattr(an, key, value)
                analog_channels.append(an)
            cfg.analog_channels = analog_channels
        # 循环开关量修改列表，根据修改列表的内容修改cfg对象
        if modify_digitals is not None:
            digital_channels = []
            for idx, md in enumerate(modify_digitals):
                dn = cfg.digital_channels[idx]
                for key, value in md.items():
                    if value != getattr(dn, key):
                        setattr(dn, key, value)
                digital_channels.append(dn)
            cfg.digital_channels = digital_channels
        return cfg

    def modify_sysconfig(self, modify_sysconfig: dict):
        """
        根据修改列表的内容修改cfg对象
        :param modify_sysconfig: 系统配置修改信息，默认为空，返回原通道信息，当不为空时返回列表内包含通道和要修改后的属性
        :return: cfg对象
        """
