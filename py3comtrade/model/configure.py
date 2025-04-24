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

from pydantic import BaseModel, Field

from py3comtrade.model.analog import Analog
from py3comtrade.model.channel_num import ChannelNum
from py3comtrade.model.config_header import ConfigHeader
from py3comtrade.model.config_sample import ConfigSample
from py3comtrade.model.digital import Digital
from py3comtrade.model.nrate import Nrate
from py3comtrade.model.precision_time import PrecisionTime
from py3comtrade.model.timemult import TimeMult


class Configure(BaseModel):
    """
    配置文件类，用于存储配置文件信息
    """

    header: ConfigHeader = Field(default=ConfigHeader(), description="配置文件头")
    channel_num: ChannelNum = Field(default=None, description="通道数量")
    analogs: list[Analog] = Field(default=[], description="模拟通道列表")
    digitals: list[Digital] = Field(default=[], description="开关量通道列表")
    sample: ConfigSample = ConfigSample()
    file_start_time: PrecisionTime = Field(default=None, description="文件起始时间")
    fault_time: PrecisionTime = Field(default=None, description="故障时间")
    timemult: TimeMult = TimeMult(timemult=1)

    def __init__(self, file_path):
        super().__init__()
        self.__file_path = file_path

    def clear(self):
        """清除模型中所有字段"""
        for field in self.__fields__.keys():
            setattr(self, field, None)

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
                                cycle_num: float = None, mode: int = 1) -> tuple:
        """
        获取游标采样点位置开始、结束采样取值范围、采样点个数\n
        当end_point不为空且大于开始采样点，以end_point采样点为准，
        当end_point不合法且cycle_num为空时，获取全部采样点，
        当cycle_num不为空按周波倍数默认向后取值。
        :param point1: 采样起始点，默认为0
        :param point2: 采样终止点，不含终止点，默认为None 代表全部采样点
        :param cycle_num: 采样周波数量，当end_point为空时生效
        :param mode: 取值模式，仅在按周波取值时生效，默认为1：代表向采样点后方取值，-1：代表向采样点前方取值，0：代表向采样点两边取值
        :return: 返回一个元祖，分别代表开始采样点、结束采样点、采样点数量
        """
        # 检查mode的有效性
        if mode not in [-1, 0, 1]:
            raise ValueError("mode参数错误,必须是-1,0,1")
        if point1 < 0:
            raise ValueError("point1参数错误,不能小于0")
        if point2 is not None and point1 > point2:
            raise ValueError("point2参数错误,不能小于point1")
        start_point = point1
        # 当end_point不为空时，且end_point大于start_point时，以end_point为最后采样点
        if point2 is not None and point2 > start_point:
            end_point = point2
        # 当point2不合法，且cycle_num都为空时，获取全部采样点
        elif cycle_num is None:
            end_point = self.sample.count - 1
        # 当cycle_num不为空时，优先按周波计算采样点范围，当跨采样段取该段的最后一个值，如果向前取值开始采样点为该段的第一个值
        else:
            start_point, end_point = self.get_cursor_cycle_sample_range(point1, cycle_num, mode)
        samp_num = end_point - start_point
        return start_point, end_point, samp_num + 1

    def get_cursor_cycle_sample_range(self, point1: int, cycle_num: float = 1, mode: int = 1):
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
        if mode == -1:
            point1 = point1 - samp_num if point1 >= samp_num else 0
            point2 = point1 + samp_num
        elif mode == 0:
            offset_point = samp_num // 2
            point1 = point1 - offset_point if point1 >= offset_point else 0
            point2 = point1 + samp_num
        else:
            point2 = point1 + samp_num
        # 判断两点采样频率是否相等
        if not self.equal_two_point_samp_rate(point1, point2):
            if mode == 1:
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
        return

    def get_analog_by_index(self, index: int) -> Analog:
        """
        根据索引获取模拟量
        :param index: 索引
        :return: 模拟量对象
        """
        if 0 <= index < len(self.analogs):
            return self.analogs[index]
        raise IndexError("索引超出范围")

    def get_analog_by_an(self, an: int) -> Analog:
        """
        根据an获取模拟量
        :param an: 模拟量an
        :return: 模拟量对象
        """
        for analog in self.analogs:
            if analog.cfg_index == an:
                return analog

    def add_analog(self, analog: Analog, index: int = None):
        """
        添加模拟量
        :param analog: 模拟量通道对象
        :param index: 添加的位置，当为空时从列表的尾部添加
        """
        if index is not None:
            self.analogs.insert(index, analog)
        else:
            analog.index = len(self.analogs)
            self.analogs.append(analog)

    def get_digital_by_index(self, index: int) -> Digital:
        """
        根据索引获取开关量
        :param index: 索引
        :return: 开关量对象
        """
        if 0 <= index < len(self.digitals):
            return self.digitals[index]
        raise IndexError("索引超出范围")

    def get_digital_by_dn(self, dn: int) -> Digital:
        """
        根据dn获取开关量
        :param dn: 开关量dn
        :return: 开关量对象
        """
        for digital in self.digitals:
            if digital.cfg_index == dn:
                return digital

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
