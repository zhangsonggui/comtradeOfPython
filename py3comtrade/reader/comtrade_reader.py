#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  Copyright (c) [2019] [name of copyright holder]
#  [py3comtrade] is licensed under Mulan PSL v2.
#  You can use this software according to the terms and conditions of the Mulan
#  PSL v2.
#  You may obtain a copy of Mulan PSL v2 at:
#           http://license.coscl.org.cn/MulanPSL2
#  THIS SOFTWARE IS PROVIDED ON CFGAN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY
#  KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
#  NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
#  See the Mulan PSL v2 for more details.
import os

from py3comtrade.model import Comtrade
from py3comtrade.model.type import FilePath
from py3comtrade.model.type import ReadMode
from py3comtrade.reader.config_reader import config_reader
from py3comtrade.reader.data_reader import data_reader


def get_comtrade_path(_file_path: str) -> FilePath:
    """
    根据传入的文件路径获取不同后缀名的一组文件。
    :param _file_path: 指定文件路径
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
        return FilePath(cfg_path=cfg_path, dat_path=dat_path, dmf_path=dmf_path)
    except (TypeError, ValueError) as e:
        print(f"文件名解析失败!!!", e)
        return FilePath(cfg_path="", dat_path="", dmf_path="")


def comtrade_reader(_file_path: str, read_mode: ReadMode = ReadMode.FULL) -> Comtrade:
    """
    读取Comtrade数据

    参数:
        _file_path(str): 文件路径
        read_mode: 读取模式
    返回:
        Comtrade对象
    """
    files = get_comtrade_path(_file_path)
    cfg = config_reader(files.get("cfg_path"))
    _comtrade: Comtrade = Comtrade(file_path=files,
                                   header=cfg.header,
                                   channel_num=cfg.channel_num,
                                   analogs=cfg.analogs,
                                   digitals=cfg.digitals,
                                   sample=cfg.sample,
                                   file_start_time=cfg.file_start_time,
                                   fault_time=cfg.fault_time,
                                   timemult=cfg.timemult)
    if read_mode in [ReadMode.DAT, ReadMode.FULL]:
        try:
            dat = data_reader(files.get("dat_path"), cfg.sample)
            _comtrade.sample_time = dat.sample_time.tolist()
            for analog in _comtrade.analogs:
                analog.raw = dat.analog_value.T[analog.index, :].tolist()
                # analog.instants = np.round(vs * analog.a + analog.b, 3).tolist()
            for digital in _comtrade.digitals:
                digital.raw = dat.digital_value.T[digital.index, :].tolist()
        except ValueError as e:
            raise f"{_file_path}文件解析失败：{e}"
        _comtrade.analyze_digital_change_status()
    if read_mode in [ReadMode.DMF, ReadMode.FULL]:
        pass
    return _comtrade


if __name__ == '__main__':
    file_path = r'D:\codeArea\gitee\comtradeOfPython\tests\data\xtz.cfg'
    comtrade = comtrade_reader(file_path, ReadMode.DAT)
    raw_a = comtrade.get_raw_by_analog_indices()
    raw_d = comtrade.get_instant_by_digital_indices()
    for dc in comtrade.digital_change:
        print(dc.name, dc.idx_cfg, dc.phase)
