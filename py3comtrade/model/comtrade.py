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
import copy
import json
import os.path
import struct
from typing import Union, List

import numpy as np
import pandas as pd
from pydantic import Field

from py3comtrade.computation.basic_calc import raw_to_instant
from py3comtrade.model.analog import Analog
from py3comtrade.model.configure import Configure
from py3comtrade.model.digital import Digital
from py3comtrade.model.digital import StatusRecord
from py3comtrade.model.dmf import DMF
from py3comtrade.model.nrate import Nrate
from py3comtrade.model.type.analog_enum import PsType
from py3comtrade.model.type.base_enum import CustomEncoder
from py3comtrade.model.type.data_file_type import DataFileType
from py3comtrade.model.type.types import FilePath
from py3comtrade.model.type.types import IdxType, ChannelType
from py3comtrade.utils.file_tools import split_path


class Comtrade(Configure):
    file_path: FilePath = Field(default=None, description="录波文件路径")
    dmf: DMF = Field(default=None, description="Comtrade数据对象")
    sample_point: List[int] = Field(default_factory=list, description="采样点号")
    sample_time: List[int] = Field(default_factory=list, description="采样时间")
    digital_change: List[Digital] = Field(default_factory=list, description="变位开关量通道记录")

    def get_channel_raw_data_range(self, channel_idx: Union[int, list[int]] = None,
                                   idx_type: IdxType = IdxType.INDEX,
                                   channel_type: ChannelType = ChannelType.ANALOG,
                                   start_point: int = 0,
                                   end_point: int = None) -> Union[list[Digital], list[Analog]]:
        """
        根据指定通道标识获取指定采样范围内模拟量原始采样值

        参数:
            channel_idx(int,list[int]) 通道索引值或通道索引值列表
            idx_type:(IdxType)通道标识类型，默认使用INDEX，支持按照通道数组索引值和cfg通道标识an两种方式
            channel_type(ChannelTyep)通道类型，默认模拟量ANALOG，支持模拟量和开关量两种类型
            start_point(int) 开始采样点，默认值0，包含该点。
            end_point(int) 结束采样点，默认值为None，为录波文件最大采样点，不包含该点。
        返回值:
            通道对象数组
        """
        # 根据传入的采样值范围确定开始采样值点和结束采样点
        start_point, end_point, _ = self.get_cursor_sample_range(start_point, end_point)
        # 根据通道索引值获取模拟量通道对象
        chaneels = self.get_channel(channel_idx, channel_type, idx_type)

        if not isinstance(chaneels, list):
            chaneels = [chaneels]
        cns = []
        for chaneel in chaneels:
            chaneel_new = copy.copy(chaneel)
            chaneel_new.raw = chaneel.raw[start_point:end_point + 1]
            cns.append(chaneel_new)
        return cns

    def get_analog_instant_data_range(self, channel_idx: Union[int, list[int]] = None,
                                      idx_type: IdxType = IdxType.INDEX,
                                      channel_type: ChannelType = ChannelType.ANALOG,
                                      start_point: int = 0,
                                      end_point: int = None,
                                      output_primary: bool = False) -> Union[list[Digital], list[Analog]]:
        """
        根据指定通道标识获取指定采样范围内模拟量瞬时采样值

        参数:
            channel_idx(int,list[int]) 通道索引值或通道索引值列表
            idx_type:(IdxType)通道标识类型，默认使用INDEX，支持按照通道数组索引值和cfg通道标识an两种方式
            channel_type(ChannelTyep)通道类型，默认模拟量ANALOG，支持模拟量和开关量两种类型
            start_point(int) 开始采样点，默认值0，包含该点。
            end_point(int) 结束采样点，默认值为None，为录波文件最大采样点，不包含该点。
            output_primary(bool)输出值是否是一次值
        返回值:
            通道对象数组
        """
        channel_raw_data = self.get_channel_raw_data_range(channel_idx, idx_type, channel_type, start_point, end_point)
        if channel_type == channel_type.DIGITAL:
            return channel_raw_data
        instants = []
        for channel in channel_raw_data:
            input_primary = True if channel.ps == PsType.P else False
            channel.y = raw_to_instant(channel.raw, channel.a, channel.b, channel.primary, channel.secondary,
                                       input_primary, output_primary)
            instants.append(channel)
        return instants

    def get_digital_change(self) -> list[Digital]:
        """
        获取所有发生变位的开关量
        """
        if self.digital_change is None:
            self.analyze_digital_change_status()
        return self.digital_change

    def analyze_digital_change_status(self):
        """
        根据开关量采样值计算变化点号及幅值
        """
        self.digital_change = []
        for digital in self.digitals:
            raw = np.array(digital.raw)
            digital.change_status.append(StatusRecord(sample_point=self.sample_point[0],
                                                      timestamp=self.sample_time[0],
                                                      status=raw[0].item()))
            if raw.min() != raw.max():
                # 找出变化点：当前值与前一个值不同
                change_indices = np.where(raw[:-1] != raw[1:])[0] + 1
                # 获取变化后的值
                change_vs = raw[change_indices]
                for i in range(len(change_vs)):
                    digital.change_status.append(StatusRecord(sample_point=change_indices[i].item(),
                                                              timestamp=self.sample_time[change_indices[i].item()],
                                                              status=change_vs[i].item()))
                self.digital_change.append(digital)

    def _update_configure(self, nrates: List[Nrate] = None, data_file_type: DataFileType = DataFileType.BINARY):
        """更新配置文件参数"""
        # 更新文件格式
        self.sample.data_file_type = data_file_type
        # 根据模拟量和开关量数组长度更新通道数量
        self.channel_num.analog_num = len(self.analogs)
        self.channel_num.digital_num = len(self.digitals)
        self.sample.channel_num = self.channel_num
        # 更新采样频率
        if nrates is not None:
            self.sample.nrate_num = len(nrates)
            self.sample.nrates = nrates
            self.sample.calc_sampling()

    def save_json(self, file_path: str):
        comtrade_json = self.model_dump()
        with open(file_path, 'w', encoding='utf8') as f:
            json.dump(comtrade_json, f, ensure_ascii=False, indent=2, cls=CustomEncoder)

    def save_csv(self, file_path: str,
                 samp_point_num_title: bool = True,
                 sample_time_title: bool = True,
                 value_type: str = "instant"):
        """
        将comtrade对象保存为csv文件
        参数:
            file_path(str):保存文件路径
            samp_point_num_title(bool):是否添加采样点序号行,默认为添加
            sample_time_title(bool):是否添加采样时间行,默认为添加
            value_type(str):数值格式instant保存为瞬时值,raw保存为原始采样值,默认为瞬时值
        返回值:
        """
        with open(file_path, "w", encoding="gbk") as f:
            if samp_point_num_title:
                f.write(f'采样点号,{",".join(map(str, self.sample_point))}\n')
            if sample_time_title:
                f.write(f'采样时间,{",".join(map(str, self.sample_time))}\n')
            for analog in self.analogs:
                if value_type == "raw":
                    f.write(f'{analog.name},{",".join(map(str, analog.raw))}\n')
                else:
                    instant = [raw * analog.a + analog.b for raw in analog.raw]
                    f.write(f'{analog.name},{",".join(map(str, instant))}\n')
            for digital in self.digitals:
                f.write(f'{digital.name},{",".join(map(str, digital.raw))}\n')

    def save_comtrade(self, file_path: str, data_file_type: DataFileType = DataFileType.BINARY):
        """
        将comtrade对象保存为文件
        参数:
            file_path(str) 保存路径,后缀名可选
            data_file_type(DataFileType) 保存格式,默认保存为二进制文件
        返回:
            cfg、dat文件
        """
        # 分离文件路径为目录、文件名、文件后缀
        path, file_name, ext_name = split_path(file_path)
        self.file_path["cfg_path"] = str(os.path.join(path, file_name + ".cfg"))
        self.file_path["dat_path"] = str(os.path.join(path, file_name + ".dat"))
        self.file_path["dmf_path"] = str(os.path.join(path, file_name + ".dmf"))
        # 更换configure参数
        self._update_configure(data_file_type=data_file_type)
        # 写入cfg文件
        super().write_cfg_file(self.file_path.get("cfg_path"))
        if data_file_type == DataFileType.ASCII:
            self._write_ascii_file(self.file_path.get("dat_path"))
        else:
            self._write_binary_file(self.file_path.get("dat_path"))

    def _write_ascii_file(self, output_file_path: str):
        """
        将数据写入ASCII格式文件

        参数:
            output_file_path: 输出文件路径
        """
        analog_values = np.array([analog.raw for analog in self.analogs])
        digital_values = np.array([digital.raw for digital in self.digitals])
        # 组合数据
        data = np.column_stack((
            self.sample_point,
            self.sample_time,
            analog_values.T,
            digital_values.T
        ))

        # 写入CSV文件
        pd.DataFrame(data).to_csv(output_file_path, header=False, index=False)

    def _write_binary_file(self, output_file_path: str):
        """
        将数据写入二进制格式文件，符合COMTRADE标准格式

        参数:
            output_file_path: 输出文件路径
        """
        # 获取数据并转置，使每行代表一个采样点
        analog_values = np.array([analog.raw for analog in self.analogs]).T
        digital_values = np.array([digital.raw for digital in self.digitals]).T
        # 根据数据类型确定模拟量格式
        if self.sample.data_file_type == DataFileType.BINARY32:
            analog_fmt = '<i'  # 4个字节小端序有符号整数
        elif self.sample.data_file_type == DataFileType.FLOAT32:
            analog_fmt = '<f'  # 4个字节小端序浮点数
        else:
            analog_fmt = '<h'  # 2个字节小端序有符号短整数

        with open(output_file_path, 'wb') as f:
            # 遍历每个采样点
            for i in range(len(self.sample_point)):
                # 1. 写入采样点号 (4个字节小端序有符号整数)
                sample_point_bytes = struct.pack('<i', int(self.sample_point[i]))
                f.write(sample_point_bytes)

                # 2. 写入采样时间 (4个字节小端序浮点数)
                sample_time_bytes = struct.pack('<f', float(self.sample_time[i]))
                f.write(sample_time_bytes)

                # 3. 写入模拟量数据
                for j in range(len(self.analogs)):  # 遍历每个模拟通道
                    if i < analog_values.shape[0] and j < analog_values.shape[1]:
                        analog_value = int(analog_values[i, j])
                    else:
                        analog_value = 0
                    analog_bytes = struct.pack(analog_fmt, analog_value)
                    f.write(analog_bytes)

                # 4. 写入数字量数据 (将最多16个数字量通道状态打包成2个字节)
                for word_idx in range(int(self.sample.digital_sampe_word / 2)):
                    digital_word = 0
                    # 处理当前16位字中的每一位
                    for bit_idx in range(16):
                        channel_idx = word_idx * 16 + bit_idx
                        # 检查是否还有数字量通道需要处理
                        if channel_idx < len(self.digitals):
                            if i < digital_values.shape[0] and channel_idx < digital_values.shape[1]:
                                digital_status = int(digital_values[i, channel_idx])
                                if digital_status != 0:
                                    digital_word |= (1 << bit_idx)

                    # 将16位数字量状态打包成2个字节无符号短整数
                    digital_bytes = struct.pack('<H', digital_word)
                    f.write(digital_bytes)
