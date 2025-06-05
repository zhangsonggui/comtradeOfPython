#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

from py3comtrade.model.configure import Configure
from py3comtrade.model.type.types import FloatArray32, IntArray32


def validate_data(configure: Configure, sample_time: IntArray32, analog_values: FloatArray32,
                  digital_values: IntArray32):
    if sample_time.shape[1] != analog_values.shape[1] != digital_values.shape[1]:
        raise ValueError("数据长度不匹配")
    if len(configure.analogs) != analog_values.shape[0]:
        raise ValueError("数据长度不匹配")
    if len(configure.digitals) != digital_values.shape[0]:
        raise ValueError("数据长度不匹配")
    return True


def np_concatenate(sample_time: IntArray32, analog_values: FloatArray32,
                   digital_values: IntArray32) -> FloatArray32:
    assert sample_time.shape[1] == analog_values.shape[1] == digital_values.shape[1]
    combined_array = np.concatenate((sample_time, analog_values, digital_values), axis=0)
    return combined_array.T


def data_to_ascii(configure: Configure, data: FloatArray32, filename: str):
    assert len(configure.analogs) + len(configure.digitals) + 2 == data.shape[1]
    df = pd.DataFrame(data)
    df.iloc[:, 0] = pd.to_numeric(df.iloc[:, 0], errors='coerce').fillna(0).astype(int)
    df.to_csv(filename, index=False, header=False, sep=',')


def data_to_ascii_file(configure: Configure, sample_time: IntArray32, analog_values: FloatArray32,
                       digital_values: IntArray32, filename: str):
    """
    将sample_time、analog_values、digital_values三个numpy数组使用逗号写入文件，第一行为sample_time的第一个
    :param configure: 数组对象
    :param sample_time: 采样点及时间戳
    :param analog_values: 模拟量采样值
    :param digital_values: 开关量采样值
    :param filename: 保存的文件名，含目录、文件名和后缀
    :return:
    """
    validate_data(configure, sample_time, analog_values, digital_values)
    lines = []

    for col in range(sample_time.shape[1]):
        line_parts = []
        # 添加 sample_time 数据
        for row in range(sample_time.shape[0]):
            line_parts.append(str(sample_time[row, col]))

        # 添加 analog_values 数据
        for row in range(analog_values.shape[0]):
            line_parts.append(str(analog_values[row, col]))

        # 添加 digital_values 数据
        for row in range(digital_values.shape[0]):
            line_parts.append(str(digital_values[row, col]))

        lines.append(','.join(line_parts))

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
    except Exception as e:
        raise RuntimeError(f"写入文件 {filename} 失败: {e}")

    return f'{filename}文件生成成功！'


def write_dat_binary(dat: np.ndarray, filename: str):
    pass


def write_dat_binary32(dat: np.ndarray, filename: str):
    pass
