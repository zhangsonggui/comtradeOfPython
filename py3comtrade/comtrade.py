#!/usr/bin/python3
# _*_ coding: utf-8 _*_
#
# Copyright (C) 2024 - 2024 张松贵, Inc. All Rights Reserved
#
# @Time    : 2024/3/23 11:27
# @Author  : 张松贵
# @File    : comtrade.py
# @IDE     : PyCharm
from py3comtrade.entity.comtrade import Comtrade
from py3comtrade.parser.comtrade_parser import ComtradeParser


def read_comtrade(cfg_file_name: str, dat_file_name: str = None, dmf_file_name: str = None) -> Comtrade:
    """
    读取comtrade文件
    :param cfg_file_name: cfg文件名带后缀名,
    :param dat_file_name: dat文件名带后缀名，当该文件为空时和cfg文件名相同，后缀大小写保持一致
    :param dmf_file_name: dmf文件名带后缀名，当该文件为空时和cfg文件名相同，后缀大小写保持一致
    """
    return ComtradeParser(cfg_file_name, dat_file_name, dmf_file_name).comtrade


if __name__ == '__main__':
    file = r'../tests/data/xtz.cfg'
    ch_numbers = [1, 2, 3, 4]
    record = read_comtrade(file)
    print(record.fault_header.station_name)
    stl = record.get_sample_time_lists()
    print(stl.shape)
