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
import numpy as np
import pandas as pd
from pydantic import BaseModel, Field, ConfigDict

from py3comtrade.model.config_sample import ConfigSample


class Data(BaseModel):
    file_path: str = Field(description="文件路径")
    size: int = Field(default=0, description="文件大小")
    sample_time: np.ndarray = Field(default=None, description="采样时间")
    analog_value: np.ndarray = Field(default=None, description="模拟量值")
    digital_value: np.ndarray = Field(default=None, description="开关量值")

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def write_ascii(self, output_file_path: str):
        """
        将数据写入ASCII格式文件

        参数:
            output_file_path: 输出文件路径
        """
        # 组合数据
        data = np.column_stack((
            self.sample_time.reshape(-1, 2),
            self.analog_value,
            self.digital_value
        ))

        # 写入CSV文件
        pd.DataFrame(data).to_csv(output_file_path, header=False, index=False)

    def write_binary(self, output_file_path: str, sample: ConfigSample):
        """
        将数据写入二进制格式文件

        参数:
            output_file_path: 输出文件路径
            sample: 采样信息
        """
        # 自定义dtype结构，与parse_binary方法兼容
        dt = np.dtype([
            ('timestamp', np.int32, 2),  # 2个int作为时间戳
            ('analog', np.int16, sample.channel_num.analog_num),  # 模拟量
            ('digital', np.uint16, sample.channel_num.digital_num // 16),  # 开关量
        ])

        # 创建空数组
        data = np.empty(sample.count, dtype=dt)

        # 填充数据
        data['timestamp'] = self.sample_time
        data['analog'] = self.analog_value.astype(np.int16)

        # 处理开关量 - 将位重新打包成uint16
        # 确保digital_value是正确的形状
        digital_shape = self.digital_value.shape
        if len(digital_shape) == 1:
            # 重塑为2D数组
            self.digital_value = self.digital_value.reshape(-1, 1)

        # 计算需要的字节数
        bytes_needed = (self.digital_value.shape[1] + 7) // 8
        digital_packed = np.zeros((self.digital_value.shape[0], bytes_needed), dtype=np.uint8)

        # 手动打包位
        for i in range(self.digital_value.shape[1]):
            byte_idx = i // 8
            bit_idx = i % 8
            digital_packed[:, byte_idx] |= (self.digital_value[:, i] << bit_idx)

        # 确保digital_packed的形状与data['digital']匹配
        if digital_packed.shape[1] != data['digital'].shape[1]:
            # 调整形状
            digital_packed = digital_packed.reshape(data['digital'].shape)

        data['digital'] = digital_packed.view(np.uint16)

        # 写入文件
        with open(output_file_path, 'wb') as f:
            f.write(data.tobytes())
