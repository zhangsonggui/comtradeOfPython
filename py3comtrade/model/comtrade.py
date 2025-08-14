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
from typing import Union

import numpy as np
from pydantic import Field

from py3comtrade.computation.basic_calc import raw_to_instant
from py3comtrade.model.dmf import DMF
from .analog import Analog
from .configure import Configure
from .digital import Digital
from .digital_change_status import StatusRecord
from .type import FilePath
from .type import PsType
from .type.types import IdxType, ChannelType


class Comtrade(Configure):
    file_path: FilePath = Field(default=None, description="录波文件路径")
    dmf: DMF = Field(default=None, description="Comtrade数据对象")
    sample_time: list = Field(default_factory=list, description="采样时间")
    digital_change: list = Field(default_factory=list, description="变位开关量通道记录")

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
            status_record = StatusRecord(timestamp=0, status=raw[0].item())
            digital.change_status.append(status_record)
            if raw.min() != raw.max():
                # 找出变化点：当前值与前一个值不同
                change_indices = np.where(raw[:-1] != raw[1:])[0] + 1
                # 获取变化后的值
                change_vs = raw[change_indices]
                for i in range(len(change_vs)):
                    status_record = StatusRecord(timestamp=change_indices[i].item(), status=change_vs[i].item())
                    digital.change_status.append(status_record)
                self.digital_change.append(digital)
