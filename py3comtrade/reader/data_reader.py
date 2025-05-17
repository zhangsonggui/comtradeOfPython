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

import struct

import numpy as np
import pandas as pd
from pydantic import BaseModel, Field, ConfigDict

from py3comtrade.model.config_sample import ConfigSample
from py3comtrade.model.type.data_file_type import DataFileType
from py3comtrade.reader.config_reader import config_reader


def digital_split(datas: tuple) -> list:
    """
    将开关量整数数组拆分成数组
    :return: data
    """
    digitals = []
    for data in datas:
        binary_array = [(data >> i) & 1 for i in range(15, -1, -1)]
        binary_array.reverse()
        digitals.extend(binary_array)
    return digitals


class DataReader(BaseModel):
    """
    读取文件
    """
    file_path: str = Field(description="文件路径")
    sample: ConfigSample = Field(description="采样信息")
    size: int = Field(default=0, description="文件大小")
    sample_time: np.ndarray = Field(default=None, description="采样时间")
    analog_value: np.ndarray = Field(default=None, description="模拟量值")
    digital_value: np.ndarray = Field(default=None, description="开关量值")

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __init__(self, **data):
        super().__init__(**data)
        self.size = 0
        self.sample_time = np.zeros((self.sample.count, 2), dtype=np.int32)
        self.analog_value = np.zeros((self.sample.count, self.sample.channel_num.analog_num),
                                     dtype=np.float32)
        self.digital_value = np.zeros((self.sample.count, self.sample.channel_num.digital_num),
                                      dtype=np.int32)

    def read(self):
        if DataFileType.ASCII == self.sample.data_file_type.value:
            self.read_ascii()
        else:
            self.parse_binary()

    def read_ascii(self):
        with open(self.file_path, 'r') as f:
            content = pd.read_csv(f, header=None)
        self.sample_time = content[:, 0:2]
        self.analog_value = content[:, 2:self.sample.channel_num.analog_num + 2]
        self.digital_value = content[:, self.sample.channel_num.analog_num + 2:]

    def read_binary(self):
        str_struct = f"ii{self.sample.analog_sampe_word // 2}h{self.sample.digital_sampe_word // 2}H"
        with open(self.file_path, 'rb') as f:
            for i in range(self.sample.count):
                byte_str = f.read(self.sample.total_sampe_word)
                if len(byte_str) != self.sample.total_sampe_word:
                    raise ValueError("文件长度不足")
                sample_struct = struct.unpack(str_struct, byte_str)
                self.sample_time[i:] = sample_struct[0:2]
                self.analog_value[i:] = sample_struct[2:2 + self.sample.channel_num.analog_num]
                self.digital_value[i:] = digital_split(sample_struct[2 + self.sample.channel_num.analog_num:])

    def parse_binary(self):
        # 自定义 dtype 结构
        dt = np.dtype([
            ('timestamp', np.int32, 2),  # 2个int作为时间戳
            ('analog', np.int16, self.sample.channel_num.analog_num),  # 96个short作为模拟量
            ('digital', np.uint16, self.sample.channel_num.digital_num//16),  # 12个unsigned short作为开关量
        ])

        # 一次性读取并解析
        with open(self.file_path, 'rb') as f:
            buffer = f.read()

        data = np.frombuffer(buffer, dtype=dt)

        # 提取各部分
        self.sample_time = data['timestamp']
        self.analog_value = data['analog']
        self.digital_value = np.unpackbits(data['digital'].view(np.uint8), bitorder='little',axis=-1)


if __name__ == '__main__':
    cfg_file_name = r'D:\codeArea\gitee\comtradeOfPython\tests\data\hjz.cfg'
    dat_file_name = r'D:\codeArea\gitee\comtradeOfPython\tests\data\hjz.dat'
    configure = config_reader(cfg_file_name)
    dat_content = DataReader(file_path=dat_file_name, sample=configure.sample)
    dat_content.parse_binary()
    dat_content.read()
    print('解析完毕')
