#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 - 2024 张松贵, Inc. All Rights Reserved
# 提供多个comtrade文件合并成一个comtrade文件方法。
# TODO： 目前仅实现同一采样频率的简单合并，后期增加采样频率归一化和采样点偏移的功能
import argparse
import datetime
import logging
import os

from py3comtrade.merge.merge_comtrade import MergeComtrade
from py3comtrade.utils.cfg_to_file import cfg_to_file
from py3comtrade.utils.dat_to_file import write_dat_ascii


def check_directory(path: str):
    """检查并报告目录是否存在以及是否为目录类型。
    Args:
        path (str): 要检查的目录路径。
    Returns:
        bool: 如果路径存在且为目录则返回True，否则返回False。
    """
    if os.path.isdir(path):
        return True
    else:
        print(f"路径问题: '{path}' 不存在或不是一个目录")
        return False


# 设置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def parse_arguments():
    parser = argparse.ArgumentParser(description='合并文件。')
    parser.add_argument('directory', type=str, help='待合并文件的目录路径')
    parser.add_argument('dist_name', nargs='?',
                        default=f"实训站_仿真设备{datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')}",
                        help='合并后文件名，默认为合并后的文件名，不带后缀名')
    return parser.parse_args()


def main():
    args = parse_arguments()
    directory = args.directory
    dist_name = args.dist_name
    logging.info(f"要处理的目录：{directory}")
    if not check_directory(directory):
        logging.error(f'指定待合并文件目录存在问题，跳过操作。')
        return
    mc = MergeComtrade(directory)
    cfg = mc.merge_cfg_data()
    cfg_to_file(cfg, dist_name + '.cfg')
    dat = mc.merge_dat_data()
    write_dat_ascii(dat, dist_name + '.dat')
    print(f'{dist_name}文件生成成功！')


if __name__ == '__main__':
    main()
