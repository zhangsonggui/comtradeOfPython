#!/usr/bin/env python
# -*- coding: utf-8 -*-
from py3comtrade.parser.analog_channel import AnalogChannel
from py3comtrade.parser.cfg_parser import CfgParser
from py3comtrade.merge.modify_entry import ModifyEntry


# TODO: 该文件最终要完成对cfg文件的整体修改
# TODO: 通道数量的选择，决定哪些通道保留
# TODO: 通道参数的修改
# TODO: 系统参数里面，应该


def modify_analog_channels(cfg_ans: list[AnalogChannel], modify_ans: list[AnalogChannel]):
    """
    修改模拟量通道属性
    :param cfg_ans: 模拟量通道对象
    :param modify_ans: 模拟量要修改信息
    :return: cfg模拟量通道数组
    """
    ans = [getattr(obj, 'an') for obj in cfg_ans]
    for modify_an in modify_ans:
        an = modify_an.an
        try:
            attr_name = modify_an.attr_name
            new_value = modify_an.new_value
            setattr(cfg_an, attr_name, new_value)
        except KeyError:
            print(f"模拟量通道{modify_an.obj_an}不存在")
    return cfg_ans


def modify_digital_channels(cfg_dns: list[AnalogChannel], modify_dns: list[AnalogChannel]):
    """
    修改开关量量通道属性
    :param cfg_dns: 模拟量通道对象
    :param modify_dns: 模拟量要修改信息
    :return: cfg开关量通道数组
    """
    cfg_index = {obj.dn: obj for obj in cfg_dns}
    for modify_dn in modify_dns:
        try:
            cfg_dn = cfg_index[modify_dn.obj_dn]
            attr_name = modify_dn.attr_name
            new_value = modify_dn.new_value
            setattr(cfg_dn, attr_name, new_value)
        except KeyError:
            print(f"开关量通道{modify_dn.obj_dn}不存在")
    return cfg_dns


class ModifyCfg:
    """
    修改comtrade通道信息
    """

    def __init__(self, cfg: CfgParser, modify_entry: ModifyEntry):
        """
        根据修改列表的内容修改cfg对象
        :param cfg: cfg对象
        :param modify_entry: cfg修改实体类
        """
        self.clear()
        self._cfg = cfg
        self._modify_entry = modify_entry
        self.modify_cfg(modify_entry)

    def clear(self):
        self.cfg = None

    def modify_cfg(self, modify_entry: ModifyEntry):
        """
        根据修改列表的内容修改cfg对象
        :param modify_entry: 模拟量修改信息，默认为空，返回原通道信息，当不为空时返回列表内包含通道和要修改后的属性
        :return: cfg对象
        """

        analog_channels = modify_analog_channels(self.cfg.analog_channels, modify_entry.analog_channels)
        digital_channels = modify_digital_channels(self.cfg.digital_channels, modify_entry.digital_channels)

    def modify_sysconfig():
        pass

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
    def modify_entry(self):
        """
        获取cfg修改实体类
        :return : cfg修改实体类
        """
        return self._modify_entry

    @modify_entry.setter
    def modify_entry(self, modify_entry):
        """
        设置cfg修改实体类
        :param modify_entry: cfg修改实体类
        """
        self._modify_entry = modify_entry
