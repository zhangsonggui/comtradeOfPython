#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  Copyright (c) [2019] [name of copyright holder]
#  [py3comtrade] is licensed under Mulan PSL v2.
#  You can use this software according to the terms and conditions of the Mulan
#  PSL v2.
#  You may obtain a copy of Mulan PSL v2 at:
#           http://license.coscl.org.cn/MulanPSL2
#  THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY
#  KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
#  NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
#  See the Mulan PSL v2 for more details.
import os
from enum import Enum

from py3comtrade.model.comtrade import Comtrade
from py3comtrade.reader.config_reader import config_reader
from py3comtrade.reader.data_reader import DataReader


class ReadMode(Enum):
    FULL = (0, "comtrade所有文件")
    CFG = (1, "仅读取cfg文件")
    DAT = (2, "读取cfg和dat文件")
    DMF = (3, "读取cfg和dmf文件")


def get_files_with_different_extensions(_file_path: str) -> dict:
    """
    获取指定路径下的所有文件，并返回具有不同后缀的文件列表。
    :param _file_path: 指定路径
    :return: 具有不同后缀的文件列表
    """
    try:
        # 验证路径是否有效
        if not _file_path or not os.path.exists(_file_path):
            raise FileNotFoundError(f"路径 {_file_path} 无效或不存在。")
        # 确保路径是文件路径
        if not os.path.isfile(_file_path):
            raise ValueError(f"路径 {_file_path} 不是一个有效的文件路径。")
        # 规范化路径大小写
        normalized_path = os.path.abspath(os.path.normcase(_file_path))

        # 获取目录路径
        dir_path = os.path.dirname(normalized_path)

        # 获取文件名（包括后缀）
        _file_name = os.path.basename(normalized_path)

        # 分离文件名和后缀
        name, ext = os.path.splitext(_file_name)
        if ext in ["CFG", "DAT", "DMF"]:
            cfg_path = os.path.join(dir_path, f"{name}.CFG")
            dat_path = os.path.join(dir_path, f"{name}.DAT")
            dmf_path = os.path.join(dir_path, f"{name}.DMF")
        else:
            cfg_path = os.path.join(dir_path, f"{name}.cfg")
            dat_path = os.path.join(dir_path, f"{name}.dat")
            dmf_path = os.path.join(dir_path, f"{name}.dmf")
        return {
            "cfg_path": cfg_path if os.path.exists(cfg_path) else None,
            "dat_path": dat_path if os.path.exists(dat_path) else None,
            "dmf_path": dmf_path if os.path.exists(dmf_path) else None
        }
    except (TypeError, ValueError) as e:
        print(f"文件名解析失败!!!", e)
        return {
            "cfg_path": None,
            "dat_path": None,
            "dmf_path": None
        }


def comtrade_reader(_file_path: str, read_mode: ReadMode = ReadMode.CFG):
    files = get_files_with_different_extensions(_file_path)
    _comtrade: Comtrade = Comtrade(file_path=files)
    _comtrade.configure = config_reader(files.get("cfg_path"))
    if read_mode in [ReadMode.DAT, ReadMode.FULL]:
        _comtrade.data = DataReader(file_path=files.get("dat_path"), sample=_comtrade.configure.sample)
        _comtrade.data.read()
    if read_mode in [ReadMode.DMF, ReadMode.FULL]:
        pass
    return _comtrade


if __name__ == '__main__':
    file_path = r'../../tests/data/xtz.cfg'
    comtrade = comtrade_reader(file_path, ReadMode.DAT)
    comtrade.analyze_digital_change_status()
    for dc in comtrade.digital_change:
        print(dc)
