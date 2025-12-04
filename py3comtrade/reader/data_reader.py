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

import struct

import numpy as np
import pandas as pd

from py3comtrade.model.config_sample import ConfigSample
from py3comtrade.model.data import Data
from py3comtrade.model.type.data_file_type import DataFileType


def digital_split(datas: tuple) -> list:
    """
    将开关量整数数组拆分成数组
    :return: dat
    """
    digitals = []
    for data in datas:
        binary_array = [(data >> i) & 1 for i in range(15, -1, -1)]
        binary_array.reverse()
        digitals.extend(binary_array)
    return digitals


def read_ascii_file(file_path: str, _sample: ConfigSample):
    """
    读取ASCII格式的数据文件并解析为样本数据

    参数:
        file_path (str): 要读取的ASCII格式的comtrade文件路径
        _sample (ConfigSample): 采样信息对象，包含采样频率、采样段信息

    返回:
        Data: 包含解析后数据的Data对象，包含以下属性：
            - file_path: 文件路径
            - sample_time: 采样时间数据（前2列）
            - analog_value: 模拟量数据（第3列到模拟量通道数+2列）
            - digital_value: 数字量数据（模拟量通道数+2列之后的所有列）

    异常:
        ValueError: 当文件数据格式与配置不匹配时抛出
    """
    # 读取CSV格式的ASCII文件内容
    try:
        content = pd.read_csv(file_path, header=None)
    except Exception as e:
        raise ValueError(f"读取数据文件失败：{str(e)}")

    # 验证数据文件的行列数是否与配置匹配
    expected_rows = _sample.count
    expected_cols = _sample.channel_num.total_num + 2
    actual_rows, actual_cols = content.shape

    if expected_rows != actual_rows or expected_cols != actual_cols:
        raise ValueError(
            f"数据文件格式错误: 期望行列数({expected_rows}, {expected_cols}), "
            f"实际行列数({actual_rows}, {actual_cols})"
        )

    # 按列分割数据：前2列为采样时间，中间为模拟量数据，剩余为数字量数据
    sample_time = content.iloc[:, 0:2]
    analog_value = content.iloc[:, 2:_sample.channel_num.analog_num + 2]
    digital_value = content.iloc[:, _sample.channel_num.analog_num + 2:]

    # 构造并返回Data对象
    return Data(sample_time=sample_time.to_numpy(),
                analog_value=analog_value.to_numpy(),
                digital_value=digital_value.to_numpy())


def read_binary_file(file_path: str, _sample: ConfigSample):
    """
    读取二进制文件并解析为结构化数据

    参数:
        file_path (str): 二进制文件的路径
        _sample (ConfigSample): 配置样本对象，包含通道数量等配置信息

    返回:
        Data: 包含解析后数据的对象，包括时间戳、模拟量和开关量数据
    """
    # 定义数据结构类型，用于解析二进制数据
    dt = np.dtype([
        ('timestamp', np.int32, 2),  # 2个int作为时间戳
        ('analog', np.int16, _sample.channel_num.analog_num),  # 模拟量
        ('digital', np.uint16, _sample.channel_num.digital_num // 16),  # 开关量
    ])

    # 读取整个二进制文件到内存缓冲区
    with open(file_path, 'rb') as f:
        buffer = f.read()

    # 将二进制数据按照定义的结构类型解析为numpy数组
    data = np.frombuffer(buffer, dtype=dt)

    # 提取各部分
    sample_time = data['timestamp']
    analog_value = data['analog']
    digital_value = np.unpackbits(data['digital'].view(np.uint8), bitorder='little', axis=-1)
    return Data(sample_time=sample_time,
                analog_value=analog_value,
                digital_value=digital_value)


def read_binary(file_path: str, _sample: ConfigSample):
    str_struct = f"ii{_sample.analog_sampe_word // 2}h{_sample.digital_sampe_word // 2}H"
    sample_time = np.zeros((_sample.count, 2), dtype=np.int32)
    analog_value = np.zeros((_sample.count, _sample.channel_num.analog_num),
                            dtype=np.float32)
    digital_value = np.zeros((_sample.count, _sample.channel_num.digital_num),
                             dtype=np.int32)
    with open(file_path, 'rb') as f:
        for i in range(_sample.count):
            byte_str = f.read(_sample.total_sampe_word)
            if len(byte_str) != _sample.total_sampe_word:
                raise ValueError("文件长度不足")
            sample_struct = struct.unpack(str_struct, byte_str)
            sample_time[i:] = sample_struct[0:2]
            analog_value[i:] = sample_struct[2:2 + _sample.channel_num.analog_num]
            digital_value[i:] = digital_split(sample_struct[2 + _sample.channel_num.analog_num:])
    return Data(sample_time=sample_time,
                analog_value=analog_value,
                digital_value=digital_value)


def data_reader(file_path: str, _sample: ConfigSample) -> Data:
    if _sample.data_file_type.value == DataFileType.ASCII.value:
        return read_ascii_file(file_path, _sample)
    else:
        return read_binary_file(file_path, _sample)
