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

from ..model.configure import ConfigSample
from ..model.type.data_file_type import DataFileType


def digital_pack(digitals: list) -> int:
    """
    将开关量数组打包成整数
    :param digitals: 开关量数组
    :return: 打包后的整数
    """
    packed = 0
    for bit in digitals:
        packed = (packed << 1) | bit
    return packed


class DataWriter:
    """
    写入文件
    """

    def __init__(self, file_path, sample: ConfigSample):
        self.__file_path = file_path
        self.__sample = sample

    def write_file(self, sample_time: np.ndarray, analog_value: np.ndarray, digital_value: np.ndarray):
        if DataFileType.ASCII == self.sample.data_file_type.value:
            self.write_ascii(sample_time, analog_value, digital_value)
        else:
            self.write_binary(sample_time, analog_value, digital_value)

    def write_ascii(self, sample_time: np.ndarray, analog_value: np.ndarray, digital_value: np.ndarray):
        with open(self.file_path, 'w') as f:
            for i in range(self.sample.count):
                line = [str(sample_time[i, 0]), str(sample_time[i, 1])]
                line.extend(map(str, analog_value[i]))
                line.extend(map(str, digital_value[i]))
                f.write(','.join(line) + '\n')

    def write_binary(self, sample_time: np.ndarray, analog_value: np.ndarray, digital_value: np.ndarray):
        str_struct = f"ii{self.sample.analog_sampe_word // 2}h{self.sample.digital_sampe_word // 2}H"
        with open(self.file_path, 'wb') as f:
            for i in range(self.sample.count):
                time_bytes = struct.pack("ii", *sample_time[i])
                analog_bytes = struct.pack(f"{self.sample.analog_sampe_word // 2}h", *analog_value[i])
                digital_packed = [digital_pack(digital_value[i][j:j + 16]) for j in range(0, len(digital_value[i]), 16)]
                digital_bytes = struct.pack(f"{self.sample.digital_sampe_word // 2}H", *digital_packed)
                f.write(time_bytes + analog_bytes + digital_bytes)

# 使用示例
# cfg_file_name = r'/tests/data/xtz.cfg'
# dat_file_name = r'/tests/data/xtz_out.dat'
# configure = config_reader(cfg_file_name)
# writer = DataWriter(dat_file_name, configure.sample)

# 假设我们有一些数据要写入
# sample_time = np.array([[1, 2], [3, 4]], dtype=np.int32)
# analog_value = np.array([[1.1, 2.2], [3.3, 4.4]], dtype=np.float32)
# digital_value = np.array([[1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0], [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]], dtype=np.int32)

# writer.write_file(sample_time, analog_value, digital_value)
# print('写入完毕')
