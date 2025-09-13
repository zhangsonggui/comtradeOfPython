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

from pydantic import BaseModel, Field

from py3comtrade.model.analog import Analog
from py3comtrade.model.channel_num import ChannelNum
from py3comtrade.model.config_header import ConfigHeader
from py3comtrade.model.config_sample import ConfigSample
from py3comtrade.model.digital import Digital
from py3comtrade.model.nrate import Nrate
from py3comtrade.model.precision_time import PrecisionTime
from py3comtrade.model.timemult import TimeMult
from py3comtrade.model.type.mode_enum import SampleMode
from py3comtrade.model.type.types import ChannelType, IdxType


class Configure(BaseModel):
    """
    配置文件类，用于存储配置文件信息
    """
    header: ConfigHeader = Field(default=ConfigHeader(), description="配置文件头")
    channel_num: ChannelNum = Field(default=None, description="通道数量")
    analogs: list[Analog] = Field(default_factory=list, description="模拟通道列表")
    digitals: list[Digital] = Field(default_factory=list, description="开关量通道列表")
    sample: ConfigSample = ConfigSample()
    file_start_time: PrecisionTime = Field(default=None, description="文件起始时间")
    fault_time: PrecisionTime = Field(default=None, description="故障时间")
    timemult: TimeMult = TimeMult(timemult=1)

    def clear(self):
        """清除模型中所有字段"""
        for field in self.model_fields.keys():
            setattr(self, field, None)

    def __str__(self):
        """
        生成cfg文件字符串
        @return: cfg文件字符串
        """
        cfg_content = ''
        cfg_content += self.header.__str__() + "\n"
        cfg_content += self.channel_num.__str__() + "\n"
        for ac in self.analogs:
            cfg_content += ac.__str__() + '\n'
        for dc in self.digitals:
            cfg_content += dc.__str__() + '\n'
        cfg_content += self.sample.__str__() + "\n"
        cfg_content += self.file_start_time.__str__() + "\n"
        cfg_content += self.fault_time.__str__() + "\n"
        cfg_content += self.sample.data_file_type.value + "\n"
        cfg_content += self.timemult.__str__()

        return cfg_content

    def write_cfg_file(self, output_file_path: str):
        with open(output_file_path, 'w', encoding='gbk') as f:
            f.write(self.__str__())

    def get_cursor_in_segment(self, cursor_site: int) -> int:
        """
        获取游标位置所在的采样段
        :param cursor_site: 游标采样点位置
        :return: 游标位置所在的采样段,当采样点位置传入错误是返回-1
        """
        for nrate in self.sample.nrates:
            if nrate.start_point <= cursor_site <= nrate.end_point:
                return nrate.index
        return -1

    def get_two_point_between_segment(self, point1: int, point2: int) -> list[Nrate]:
        """
        获取两个点之间的采样段
        :param point1: 开始采样点
        :param point2: 结束采样点
        :return: 采样段列表
        """
        point1_segment = self.get_cursor_in_segment(point1)
        point2_segment = self.get_cursor_in_segment(point2)
        return self.sample.nrates[point1_segment:point2_segment + 1]

    def equal_two_point_samp_rate(self, point1: int, point2: int) -> bool:
        """
        判断两个点之间是否是相同的采样率
        :param point1: 开始采样点
        :param point2: 结束采样点
        :return: True:采样率相同,False:采样率不同
        """
        segments = self.get_two_point_between_segment(point1, point2)
        for segment in segments:
            if segment.samp != segments[0].samp:
                return False
        return True

    def get_cursor_cycle_point(self, cursor_site: int) -> int:
        """
        获取游标位置的每周波采样点数
        :param cursor_site: 游标采样点位置
        :return: 游标位置每周波采样点数,当采样点位置传入错误是返回-1
        """
        for nrate in self.sample:
            if nrate.start_point <= cursor_site <= nrate.end_point:
                return nrate.cycle_point
        return -1

    def get_cursor_sample_range(self, point1: int = 0, point2: int = None,
                                cycle_num: float = None, mode: SampleMode = SampleMode.FORWARD) -> tuple:
        """
        获取游标采样点位置开始、结束采样取值范围、采样点个数\n
        当end_point不为空且大于开始采样点，以end_point采样点为准，
        当end_point不合法且cycle_num为空时，获取全部采样点，
        当cycle_num不为空按周波倍数默认向后取值。
        :param point1: 采样起始点，默认为0
        :param point2: 采样终止点，不含终止点，默认为None 代表全部采样点
        :param cycle_num: 采样周波数量，当end_point为空时生效
        :param mode: 取值模式，仅在按周波取值时生效，默认为FORWARD向后取值
        :return: 返回一个元祖，分别代表开始采样点、结束采样点、采样点数量
        """
        if not isinstance(point1, int):
            raise TypeError(f"采样点开始位置类型错误！需要 int 类型，但收到 {type(point1).__name__}。")
        if not (0 <= point1 < self.sample.count):
            raise ValueError(
                f"采样点开始位置超出录波采样范围！当前采样点位置: {point1}, 允许范围: [0, {self.sample.count})")
        start_point = point1
        if cycle_num is not None:  # 当采样周波不为空时，直接按照周波数计算出采样点位置
            start_point, end_point = self.get_cursor_cycle_sample_range(point1, cycle_num, mode)
        elif point2 is None:  # 当采样点结束位置为空时，默认采样点结束位置为采样点总数减1
            end_point = self.sample.count - 1
        else:
            if not isinstance(point2, int):
                raise TypeError(f"采样点结束位置类型错误！需要 int 类型，但收到 {type(point2).__name__}。")
            if not (0 <= point2 < self.sample.count):
                raise ValueError(
                    f"采样点结束位置超出录波采样范围！当前采样点位置: {point2}, 允许范围: [0, {self.sample.count})")
            if point2 < point1:
                raise ValueError("采样点结束位置小于采样点开始位置！")
            end_point = point2
        samp_num = end_point - start_point
        return start_point, end_point, samp_num + 1

    def get_cursor_cycle_sample_range(self, point1: int, cycle_num: float = 1, mode: SampleMode = SampleMode.FORWARD):
        """
        获取游标采样点所在周波获取采样取值范围
        :param point1:游标位置
        :param cycle_num:周波数量
        :param mode:取值模式，仅在按周波取值时生效，默认为1：代表向采样点后方取值，-1：代表向采样点前方取值，0：代表向采样点两边取值
        :return 返回起始点和终止点
        """
        point1_segment = self.get_cursor_in_segment(point1)
        point1_cycle_samp = self.get_cursor_cycle_point(point1)
        # 根据采样点1的每周波采样数获取采样数量
        if point1_cycle_samp == 1:  # 当每周波采样数为1工频采样时，取两个点
            samp_num = 2
        elif point1_cycle_samp % 2 == 0:  # 当每周波采样数为偶数时，取周波数的倍数-1
            samp_num = int(cycle_num * point1_cycle_samp) - 1
        else:  # 当每周波采样数为奇数时，取周波数的倍数
            samp_num = int(cycle_num * point1_cycle_samp)
        # 根据取值模式，计算采样点
        if mode == SampleMode.BACKWARD:
            point1 = point1 - samp_num if point1 >= samp_num else 0
            point2 = point1 + samp_num
        elif mode == SampleMode.CENTERED:
            offset_point = samp_num // 2
            point1 = point1 - offset_point if point1 >= offset_point else 0
            point2 = point1 + samp_num
        else:
            point2 = point1 + samp_num
        # 判断两点采样频率是否相等
        if not self.equal_two_point_samp_rate(point1, point2):
            if mode == SampleMode.FORWARD:
                point2 = self.sample.nrates[point1_segment].end_point - 1
                point1 = point2 - samp_num
            else:
                point1 = 0 if point1_segment == 0 else self.sample.nrates[point1_segment].end_point - 1
                point2 = point1 + samp_num
        return point1, point2

    def get_zero_point(self):
        """
        获取零时刻采样值采样点位置。
        使用零时刻相对时间除以每周波的时间，在乘以零时刻所在采样段每个周波的采样点
        @return: 零时刻采样点位置
        """
        time_diff = (self.fault_time.time - self.file_start_time.time).total_seconds() * 1000
        fault_point = 0
        for nrate in self.sample.nrates:
            if time_diff < nrate.end_time:
                cycle_point = self.get_cursor_cycle_point(0)
                return fault_point + int(time_diff / 20 * cycle_point)
            fault_point += nrate.end_point
        return fault_point

    def get_channel_obj(self, index: Union[int, list[int]] = None,
                        channel_type: ChannelType = ChannelType.ANALOG,
                        idx_type: IdxType = IdxType.INDEX) -> Union[Analog, Digital, list[Analog], list[Digital]]:
        """
        根据通道索引获取通道对象，含采样数据

        参数:
            index（int,list[int]）通道索引值（index）、通道标识（cfgan）、通道索引值列表或通道标识列表
            channel_type:(ChannelType)通道类型，默认为模拟量通道ANALOG,支持模拟量和开关量
            idx_type:(IdxType)通道标识类型，默认使用数组索引值INDEX，支持按照通道数组索引值和cfg通道标识an两种方式
        返回值:
            选择的通道对象或通道对象数组（模拟量、开关量）
        """
        is_analog = channel_type == ChannelType.ANALOG
        # 索引如果为None，返回模拟量或开关量的所有通道
        if index is None:
            return self.analogs if is_analog else self.digitals
        # 根据通道类型获取该类型的最大通道数量
        channel_num_max = self.channel_num.analog_num if is_analog else self.channel_num.digital_num
        # 如果索引值为int，判断索引值是否合法，如果合法返回该索引的通道对象
        if isinstance(index, int):
            if not (0 <= index < channel_num_max):
                raise ValueError(f"索引超出范围！当前索引: {index}, 允许范围: [0, {channel_num_max})")
            # 如果是按照索引值查找，返回对应的通道对象
            if idx_type == IdxType.INDEX:
                return self.analogs[index] if is_analog else self.digitals[index]
            # 如果按照通道标识符查找，返回对应的通道对象数组
            else:
                return next((analog for analog in self.analogs if analog.idx_cfg == index),
                            None) if is_analog else next(
                    (digital for digital in self.digitals if digital.idx_cfg == index), None)

        # 如果索引值为list，判断索引值是否合法，如果合法返回该索引的通道对象数组
        if isinstance(index, list):
            if idx_type == IdxType.INDEX:
                return [self.analogs[i] for i in index] if is_analog else [self.digitals[i] for i in index]
            else:
                return [self.analogs[i] for i in index if self.analogs[i].idx_cfg == index] if is_analog else [
                    self.digitals[i] for i in index if self.digitals[i].idx_cfg == index]
        raise TypeError("索引类型错误！需要 int 或 list 类型，但收到 {type(channel_idx).__name__}。")

    def get_channel_selector(self, analog_ids: Union[int, list[int]] = None,
                        digital_ids: Union[int, list[int]] = None,
                        idx_type: IdxType = IdxType.INDEX):
        """
        获取通道选择器，返回全部通道对象，不含采样值，选择通道selected为True
        参数:
            analog_ids: 模拟通道ID列表
            digital_ids: 开关量ID列表
            idx_type: 通道标识类型，默认使用数组索引值INDEX，支持按照通道数组索引值和cfg通道标识an两种方式
        返回值:
            通道选择器列表
        """
        channels = []
        for analog in self.analogs:
            is_selected = analog.is_selected(analog_ids, idx_type)
            analog_new = copy.copy(analog) if is_selected else copy.copy(analog).remove_fields("values")
            channels.append(analog_new)
        for digital in self.digitals:
            is_selected = digital.is_selected(digital_ids, idx_type)
            analog_new = copy.copy(digital) if is_selected else copy.copy(digital).remove_fields("values")
            analog_new.index = len(channels)
            channels.append(analog_new)
        return channels

    def add_analog(self, analog: Analog, index: int = None):
        if index is not None:
            self.analogs.insert(index, analog)
        else:
            analog.index = len(self.analogs)
            self.analogs.append(analog)

    def add_digital(self, digital: Digital, index: int = None):
        """
        添加开关量
        :param digital: 开关量通道对象
        :param index: 添加的位置，当为空时从列表的尾部添加
        """
        if index is not None:
            self.digitals.insert(index, digital)
        else:
            digital.index = len(self.digitals)
            self.digitals.append(digital)
