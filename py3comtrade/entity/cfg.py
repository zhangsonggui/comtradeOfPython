#!/usr/bin/python3
# _*_ coding: utf-8 _*_
#
# Copyright (C) 2024 - 2024 张松贵, Inc. All Rights Reserved
#
# @Time    : 2024/6/27 11:27
# @Author  : 张松贵
# @File    : cfg.py
from typing import List

from py3comtrade.entity.analog_channel import AnalogChannel
from py3comtrade.entity.digital_channel import DigitalChannel
from py3comtrade.entity.fault_header import FaultHeader
from py3comtrade.entity.sample_info import SampleInfo


class Cfg:
    """
    cfg配置文件实体类
    """

    def __init__(self, fault_header: FaultHeader = None, analog_channels: List[AnalogChannel] = None,
                 digital_channels: List[DigitalChannel] = None, sample_info: SampleInfo = None):
        """
        构造函数：初始化解析CFG文件的实例
        @parm fault_header: 头信息
        @parm analog_channels: 模拟通道信息
        @parm digital_channels: 开关量信息
        @parm sample_info: 采样信息
        """
        self.clear()
        self._fault_header = fault_header
        self._analog_channels = analog_channels
        self._digital_channels = digital_channels
        self._sample_info = sample_info

    def clear(self):
        """
        清除类内部的私有变量
        @return:
        """
        self._fault_header = None
        self._analog_channels = []
        self._digital_channels = []
        self._sample_info = None

    @property
    def fault_header(self):
        """
        获取头信息，含变电站名称、录波设备信息、录波文件版本、模拟量采样数量和开始采样序号、开关量采样数量和开始采样序号，采样通道总数
        """
        return self._fault_header

    @fault_header.setter
    def fault_header(self, value):
        """
        设置头信息，含变电站名称、录波设备信息、录波文件版本、模拟量采样数量和开始采样序号、开关量采样数量和开始采样序号，采样通道总数
        :param value:FaultHeader类的属性
        """
        self._fault_header = value

    @property
    def analog_channels(self):
        """
        获取模拟量通道信息
        """
        return self._analog_channels

    @analog_channels.setter
    def analog_channels(self, value):
        """
        设置模拟量通道信息
        :param value: AnalogChannel类
        """
        self._analog_channels = value

    @property
    def digital_channels(self):
        """
        获取开关量通道信息
        """
        return self._digital_channels

    @digital_channels.setter
    def digital_channels(self, value):
        """
        设置开关量通道信息
        :param value: DigitalChannel类
        """
        self._digital_channels = value

    @property
    def sample_info(self):
        """
        获取采样信息
        """
        return self._sample_info

    @sample_info.setter
    def sample_info(self, value):
        """
        设置采样信息
        :param value: SampleInfo类
        """
        self._sample_info = value

    def get_cursor_sample_range(self, point1: int = 0, point2: int = None,
                                cycle_num: float = None, mode=1) -> tuple:
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
        start_point = point1
        # 当end_point不为空时，且end_point大于start_point时，以end_point为最后采样点
        if point2 is not None and point2 > start_point:
            end_point = point2
        # 当point2不合法，且cycle_num都为空时，获取全部采样点
        elif cycle_num is None:
            end_point = self.sample_info.sample_total_num - 1
        # 当cycle_num不为空时，优先按周波计算采样点范围，当跨采样段取该段的最后一个值，如果向前取值开始采样点为该段的第一个值
        else:
            start_point, end_point = self.get_cursor_cycle_sample_range(point1, cycle_num, mode)
        samp_num = end_point - start_point
        return start_point, end_point, samp_num + 1

    def get_cursor_cycle_sample_range(self, point1: int = 0, cycle_num: float = 1, mode=1) -> tuple:
        """
        获取游标采样点所在周波获取采样取值范围
        :param point1:游标位置
        :param cycle_num:周波数量
        :param mode:取值模式，仅在按周波取值时生效，默认为1：代表向采样点后方取值，-1：代表向采样点前方取值，0：代表向采样点两边取值
        :return 返回起始点和终止点
        """
        point1_segment = self.get_cursor_point_in_segment(point1)
        point1_cycle_samp_num = self.get_cursor_cycle_sample_num(point1)
        # 根据采样点1的每周波采样数获取采样数量
        if point1_cycle_samp_num == 1:  # 当每周波采样数为1工频采样时，取两个点
            samp_num = 2
        elif point1_cycle_samp_num % 2 == 0:  # 当每周波采样数为偶数时，取周波数的倍数-1
            samp_num = int(cycle_num * point1_cycle_samp_num) - 1
        else:  # 当每周波采样数为奇数时，取周波数的倍数
            samp_num = int(cycle_num * point1_cycle_samp_num)
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
        if not self.equal_samp_rate(point1, point2):
            if mode == 1:
                point2 = self.sample_info.nrates[point1_segment].end_point - 1
                point1 = point2 - samp_num
            else:
                point1 = 0 if point1_segment == 0 else self.sample_info.nrates[point1_segment].end_point - 1
                point2 = point1 + samp_num
        return point1, point2

    def get_cursor_cycle_sample_num(self, cursor_site: int) -> int:
        """
        获取游标位置的每周波采样点数
        @param cursor_site: 游标采样点位置
        @return: 游标位置采样点数
        """
        segment = self.sample_info
        for i in range(segment.nrate_num):
            nrate = segment.nrates[i]
            if nrate.start_point <= cursor_site < nrate.end_point:
                return nrate.cycle_sample_num

    def get_point_between_segment(self, point1: int, point2: int) -> list:
        """
        获取两个采样点之间的采样段列表
        @param point1: 采样点1的位置
        @param point2: 采样点2的位置
        @return: 两个采样点所在的采样段列表
        """
        segment = []
        if not isinstance(point1, int) or (
                point2 is not None and not isinstance(point2, int)):
            raise ValueError("point1 和 point2 必须是整数")
        point1_segment = self.get_cursor_point_in_segment(point1)
        point2_segment = self.get_cursor_point_in_segment(point2)
        for i in range(point1_segment, point2_segment + 1):
            segment.append(i)
        return segment

    def get_point_between_segment_sample_num(self, point1: int, point2: int) -> list:
        """
        获取两个采样点之间每个采样段所涉及的采样点
        @param point1: 采样点1的位置
        @param point2: 采样点2的位置
        @return: 两个采样点之间每段采样段的采样点列表
        """
        if point1 is None:
            point1 = 0
        if point2 is None:
            point2 = self.sample_info.sample_total_num
        if not isinstance(point1, int) or (
                point2 is not None and not isinstance(point2, int)):
            raise ValueError("point1 和 point2 必须是整数")
        # 找出两个采样点涉及的采样段
        segment = self.get_point_between_segment(point1, point2)
        # 获取采样段对象
        nrates = self.sample_info.nrates
        # 如果两个点的采样频率相同，直接返回两点的差
        points = []
        for i, n in enumerate(segment):
            if len(segment) <= 1:  # 当采样段只有1个，直接返回两点的差
                points.append(point2 - point1)
            else:
                # 当采样段为第一个，返回第一个采样段最后的采样点和开始采样点的差
                if i == 0:
                    points.append(nrates[n].end_point - point1)
                # 当采样段为最后一个，返回结束采样点到最后一个采样段开始采样点的差
                elif i == len(segment) - 1:
                    points.append(point2 - nrates[n].start_point)
                # 返回该段采样点数
                else:
                    points.append(nrates[n].sample_num)
        return points

    def get_cursor_point_in_segment(self, cursor_site: int) -> int:
        """
        获取游标采样点所在的采样段
        @param cursor_site: 采样点位置
        @return: 采样点所在的采样段
        """
        segment = self.sample_info
        for i in range(segment.nrate_num):
            nrate = segment.nrates[i]
            if nrate.start_point <= cursor_site < nrate.end_point:
                return i

    def equal_samp_rate(self, point1: int, point2: int) -> bool:
        """
        比较两个采样点所在的采样点是否一致，含中间采样段
        :param point1: 采样点1的位置
        :param point2: 采样点2的位置
        :return: True or False
        """
        segment_num = []
        point1_segment = self.get_cursor_point_in_segment(point1)
        point2_segment = self.get_cursor_point_in_segment(point2)
        for i in range(point1_segment, point2_segment + 1):
            segment_num.append(self.sample_info.nrates[i].cycle_sample_num)
        return True if len(set(segment_num)) == 1 else False

    def get_zero_in_cycle(self) -> int:
        """
        根据零时刻相对时间和每一段采样值的最后时间相比较，确定在那个采样段内
        @return: 返回零时刻所在采样段
        """
        segment = self.sample_info
        for i in range(segment.nrate_num):
            if self.sample_info.fault_time.zero_time < segment.nrates[i].end_time * 1000:
                return i

    def get_zero_point(self) -> int:
        """
        获取零时刻采样值采样点位置。
        使用零时刻相对时间除以每周波的时间，在乘以零时刻所在采样段每个周波的采样点
        @return: 零时刻采样点位置
        """
        n = self.get_zero_in_cycle()
        return round(self.sample_info.fault_time.zero_time / 20000 * self.sample_info.nrates[n].cycle_sample_num)

    def get_channel_info(self, cfg_an: int = None, key: str = None, _type: str = 'analog'):
        """
        获取模拟量通道信息
        :param cfg_an :cfg中通道标识an或dn
        :param key :cfg通道属性
        :param _type: 通道类型,默认为analog代表模拟量，其余为开关量
        :return: 模拟量通道信息
        """
        first_index, channels, class_name = self.fault_header.analog_first_index, self.analog_channels, AnalogChannel
        if _type == 'digital':
            first_index, channels, class_name = self.fault_header.digital_first_index, self.digital_channels, DigitalChannel

        result = []
        if cfg_an is None:
            if key is None:
                result = channels
            elif hasattr(class_name, key):
                result = [getattr(obj, key) for obj in channels]
        else:
            if first_index > cfg_an > self.fault_header.analog_channel_num:
                raise ValueError("cfg_id超出范围")
            if key is None:
                result = channels[cfg_an - first_index]
            elif hasattr(class_name, key):
                result = getattr(channels[cfg_an - first_index], key)
        return result

    def get_analog_obj(self, cfg_an: int):
        """
        获取模拟量通道对象
        :param cfg_an :cfg中通道标识an
        :return: 模拟量通道对象
        """

        if cfg_an is None and (self.fault_header.analog_first_index > cfg_an > self.fault_header.analog_channel_num):
            raise ValueError("cfg_an不合法")
        else:
            first_index = self.fault_header.analog_first_index
            return self.analog_channels[cfg_an - first_index]

    def get_digital_obj(self, cfg_dn: int):
        """
        获取开关量通道对象
        :param cfg_dn :cfg中通道标识dn
        :return: 开关量通道对象
        """

        if cfg_dn is None and (self.fault_header.digital_first_index > cfg_dn > self.fault_header.digital_channel_num):
            raise ValueError("cfg_dn不合法")
        else:
            first_index = self.fault_header.digital_first_index
            return self.digital_channels[cfg_dn - first_index]
