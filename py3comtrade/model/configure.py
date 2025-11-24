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

from py3comtrade.model.channel.analog import Analog
from py3comtrade.model.channel.digital import Digital
from py3comtrade.model.channel_num import ChannelNum
from py3comtrade.model.config_sample import ConfigSample
from py3comtrade.model.exceptions import ChannelNotFoundException, ComtradeDataFormatException, \
    InvalidIndexException, \
    InvalidOperationException
from py3comtrade.model.header import Header
from py3comtrade.model.nrate import Nrate
from py3comtrade.model.precision_time import PrecisionTime
from py3comtrade.model.timemult import TimeMult
from py3comtrade.model.type.data_file_type import DataFileType
from py3comtrade.model.type.mode_enum import SampleMode
from py3comtrade.model.type.types import IdxType
from py3comtrade.utils.log import logger


class Configure(BaseModel):
    """
    配置文件类，用于存储配置文件信息。

    属性:
        header (Header): 配置文件头信息。
        channel_num (ChannelNum): 通道数量信息。
        analogs (list[Analog]): 模拟通道列表。
        digitals (list[Digital]): 开关量通道列表。
        sample (ConfigSample): 采样信息。
        file_start_time (PrecisionTime): 文件起始时间。
        fault_time (PrecisionTime): 故障时间。
        timemult (TimeMult): 时间倍数。

    方法:
        clear(): 清除模型中所有字段。
        __str__(): 生成 cfg 文件字符串。
        write_cfg_file(output_file_path: str): 将配置写入文件。
        get_cursor_in_segment(cursor_site: int) -> int: 获取游标位置所在的采样段。
        get_segment_range_point(segment: int): 获取采样段的起始和结束点。
        get_two_point_between_segment(point1: int, point2: int) -> list[Nrate]: 获取两个点之间的采样段。
        cut_samples_points(point1: int, point2: int) -> ConfigSample: 裁剪采样点后的采样段信息。
        equal_two_point_samp_rate(point1: int, point2: int) -> bool: 判断两个点之间是否是相同的采样率。
        get_cursor_cycle_point(cursor_site: int) -> float: 获取游标位置的每周波采样点数。
        get_cursor_sample_range(point1: int, point2: int, cycle_num: float, mode: SampleMode) -> tuple: 获取游标采样点范围。
        get_cursor_cycle_sample_range(point1: int, cycle_num: float, mode: SampleMode): 获取游标采样点所在周波的采样范围。
        get_zero_point(): 获取零时刻采样点位置。
        get_channel_obj(index: Union[int, list[int]], channel_type: str, idx_type: str) -> Union[Analog, Digital, list[Analog], list[Digital]]: 根据通道索引获取通道对象。
        get_channel_selector(analog_ids: Union[int, list[int]], digital_ids: Union[int, list[int]], idx_type: str): 获取通道选择器。
        get_analog_selector(analog_ids: Union[int, list[int]], idx_type: str, is_values: bool): 获取模拟通道选择器。
        get_digital_selector(digital_ids: Union[int, list[int]], idx_type: str, is_values: bool): 获取开关量选择器。
        add_analog(analog: Analog, index: int): 添加模拟通道。
        add_digital(digital: Digital, index: int): 添加开关量通道。
    """
    header: Header = Field(default=Header(), description="配置文件头")
    channel_num: ChannelNum = Field(default=ChannelNum(), description="通道数量")
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
        """
        将配置写入文件
        参数:
            output_file_path: 输出文件路径
        """
        with open(output_file_path, 'w', encoding='gbk') as f:
            f.write(self.__str__())

    def get_cursor_in_segment(self, cursor_site: int) -> int:
        """
        获取游标位置所在的采样段
        参数:
            cursor_site: 游标采样点位置
        返回值:
            游标位置所在的采样段,当采样点位置传入错误是返回-1
        """
        for nrate in self.sample.nrates:
            if nrate.start_point <= cursor_site <= nrate.end_point:
                return nrate.index
        return -1

    def get_segment_range_point(self, segment: int) -> Union[tuple[int, int], None]:
        """
        获取采样段的起始和结束点
        参数:
            segment: 采样段索引
        返回值:
            起始和结束点
        """
        if 0 <= segment <= self.sample.nrate_num:
            nrate = self.sample.nrates[segment]
            return nrate.start_point, nrate.end_point
        return None

    def get_two_point_between_segment(self, point1: int, point2: int) -> list[Nrate]:
        """
        获取两个点之间的采样段
        参数:
            point1: 开始采样点
            point2: 结束采样点
        返回值:
            采样段列表
        """
        point1_segment = self.get_cursor_in_segment(point1)
        point2_segment = self.get_cursor_in_segment(point2)
        return self.sample.nrates[point1_segment:point2_segment + 1]

    def cut_samples_points(self, point1: int = 0, point2: int = None) -> ConfigSample:
        """
        根据左右采样点,计算裁剪采样点后的采样段信息
        参数:
            Point1:开始采样点
            Point2:结束采样点
        返回值:
            采样信息段
        """
        if point2 is None:
            point1, point2, _ = self.get_cursor_sample_range(point1, point2)
        # 验证输入参数
        if not (0 <= point1 < self.sample.count):
            raise InvalidIndexException(point1, f"[0, {self.sample.count})")
        if not (0 <= point2 < self.sample.count):
            raise InvalidIndexException(point2, f"[0, {self.sample.count})")
        if point1 > point2:
            raise InvalidOperationException("起始点不能大于结束点")
        sample = copy.copy(self.sample)
        sample.nrates = self.get_two_point_between_segment(point1, point2)
        diff = point1 - sample.nrates[0].start_point
        for index, nrate in enumerate(sample.nrates):
            nrate.start_point = nrate.start_point - diff if nrate.start_point != 0 else 0
            nrate.end_point -= diff
        sample.nrates[-1].end_point = point2
        sample.calc_sampling()
        return sample

    def equal_two_point_samp_rate(self, point1: int, point2: int) -> bool:
        """
        判断两个点之间是否是相同的采样率
        参数:
            point1: 开始采样点
            point2: 结束采样点
        返回值:
            True:采样率相同,False:采样率不同
        """
        segments = self.get_two_point_between_segment(point1, point2)
        for segment in segments:
            if segment.samp != segments[0].samp:
                return False
        return True

    def get_cursor_cycle_point(self, cursor_site: int) -> float:
        """
        获取游标位置的每周波采样点数
        参数:
            cursor_site: 游标采样点位置
        返回值:
            游标位置每周波采样点数,当采样点位置传入错误是返回-1
        """
        for nrate in self.sample.nrates:
            if nrate.start_point <= cursor_site <= nrate.end_point:
                return nrate.cycle_point
        return -1

    def get_cursor_sample_range(self, point1: int = 0, point2: int = None,
                                cycle_num: float = None, mode: SampleMode = SampleMode.FORWARD) -> tuple:
        """
        获取游标采样点位置开始、结束采样取值范围、采样点个数
        参数:
            point1: 采样起始点，默认为0
            point2: 采样终止点，不含终止点，默认为None 代表全部采样点
            cycle_num: 采样周波数量，当end_point为空时生效
            mode: 取值模式，仅在按周波取值时生效，默认为FORWARD向后取值
        返回值:
            返回一个元祖，分别代表开始采样点、结束采样点、采样点数量
        """
        if not (0 <= point1 < self.sample.count):
            raise InvalidIndexException(point1, f"[0, {self.sample.count})")
        start_point = point1
        if cycle_num is not None:  # 当采样周波不为空时，直接按照周波数计算出采样点位置
            start_point, end_point = self.get_cursor_cycle_sample_range(point1, cycle_num, mode)
        elif point2 is None:  # 当采样点结束位置为空时，默认采样点结束位置为采样点总数减1
            end_point = self.sample.count - 1
        else:
            if not (start_point <= point2 < self.sample.count):
                raise InvalidIndexException(point2, f"[{start_point}, {self.sample.count})")
            end_point = point2
        samp_num = end_point - start_point
        return start_point, end_point, samp_num + 1

    def get_cursor_cycle_sample_range(self, point1: int, cycle_num: float = 1, mode: SampleMode = SampleMode.FORWARD):
        """
        获取游标采样点所在周波获取采样取值范围
        参数:
            point1: 采样起始点，默认为0
            cycle_num: 采样周波数量，默认为1
            mode: 取值模式，仅在按周波取值时生效，默认为FORWARD向后取值
        返回值:
            返回一个元祖，分别代表开始采样点、结束采样点
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
        获取零时刻采样值采样点位置。使用零时刻相对时间除以每周波的时间，在乘以零时刻所在采样段每个周波的采样点。
        参数:
            无
        返回值:
            零时刻采样点位置
        """
        if self.fault_time is None or self.file_start_time is None:
            return 0
        time_diff = (self.fault_time.time - self.file_start_time.time).total_seconds() * 1000
        fault_point = 0
        for nrate in self.sample.nrates:
            if time_diff < nrate.end_time:
                cycle_point = self.get_cursor_cycle_point(0)
                return fault_point + int(time_diff / 20 * cycle_point)
            fault_point += nrate.end_point
        return fault_point

    def get_channel_obj(self, index: Union[int, list[int]] = None,
                        channel_type: str = "ANALOG",
                        idx_type: str = "INDEX") -> Union[Analog, Digital, list[Analog], list[Digital]]:
        """
        根据通道索引获取通道对象，含采样数据

        参数:
            index（int,list[int]）通道索引值，可选值：通道索引（index）、通道标识（cfgan）、通道索引值列表或通道标识列表
            channel_type:(str)通道类型，可选值：ANALOG、DIGITAL、ALL，默认值为ANALOG
            idx_type: 索引类型，可选值：INDEX、CFGAN，默认值为INDEX
        返回值:
            选择的通道对象或通道对象数组（模拟量、开关量）
        """
        channel_type = channel_type.upper()
        idx_type = idx_type.upper()
        if channel_type == "ANALOG":
            channels = self.analogs
        elif channel_type == "DIGITAL":
            channels = self.digitals
        else:
            channels = self.analogs + self.digitals
        # 处理 None 或空列表情况
        if index is None or (isinstance(index, list) and len(index) == 0):
            return channels

        if idx_type == "CFGAN" and (channel_type == "ALL"):
            raise InvalidOperationException("当通道类型为ALL时，不能使用CFGAN索引")

        # 处理单个索引情况
        if isinstance(index, int):
            if idx_type == "INDEX":
                if not (0 <= index < len(channels)):
                    raise InvalidIndexException(index, f"[0, {len(channels)})")
                return channels[index]
            else:
                channels_dict = {channel.idx_cfg: channel for channel in channels}
                if index not in channels_dict:
                    raise ChannelNotFoundException(index, "CFGAN")
                return channels_dict[index]

        # 处理索引列表情况
        elif isinstance(index, list):
            if idx_type == "INDEX":
                # 检查所有索引是否在范围内
                if im := max(index) >= len(channels):
                    raise InvalidIndexException(im, f"[0, {len(channels)})")
                return [channels[idx] for idx in index]
            else:
                channels_dict = {channel.idx_cfg: channel for channel in channels}
                result = []
                for cfgan in index:
                    if cfgan not in channels_dict:
                        raise ChannelNotFoundException(cfgan, "CFGAN")
                    result.append(channels_dict[cfgan])
                return result
        else:
            raise InvalidOperationException(f"Index must be int, list[int] or None, got {type(index)}")

    def get_channel_selector(self, analog_ids: Union[int, list[int]] = None,
                             digital_ids: Union[int, list[int]] = None,
                             idx_type: str = "INDEX"):
        """
        获取通道选择器，返回全部通道对象，不含采样值，选择通道selected为True
        参数:
            analog_ids: 模拟通道ID列表
            digital_ids: 开关量ID列表
           idx_type: 索引类型，可选值：INDEX、CFGAN，默认值为INDEX
        返回值:
            通道选择器列表
        """
        channels = self.get_analog_selector(analog_ids, idx_type)
        channels.extend(self.get_digital_selector(digital_ids, idx_type))
        for index, channel in enumerate(channels):
            channel.index = index
        return channels

    def _get_selector(self, channels: list, ids: Union[int, list[int]] = None,
                      idx_type: str = "INDEX", is_values: bool = False):
        """
        私有方法：获取通道选择器的公共逻辑。

        参数:
            channels (list): 通道列表（模拟或开关量）。
            ids (Union[int, list[int]]): 通道ID列表。
            idx_type (str): 索引类型，可选值：INDEX、CFGAN，默认值为INDEX。
            is_values (bool): 是否包含采样值。

        返回值:
            list: 通道选择器列表。
        """
        idx_type = idx_type.upper()
        idx_type = IdxType.INDEX if idx_type == "INDEX" else IdxType.CFGAN
        result = []
        for channel in channels:
            is_selected = channel.is_selected(ids, idx_type)
            if is_values:
                channel_new = copy.copy(channel)
            else:
                channel_new = copy.copy(channel) if is_selected else copy.copy(channel).remove_fields("values")
            result.append(channel_new)
        return result

    def get_analog_selector(self, analog_ids: Union[int, list[int]] = None,
                            idx_type: str = "INDEX",
                            is_values: bool = False):
        """
        获取模拟通道选择器，返回模拟通道对象，不含采样值，选择通道selected为True

        参数:
            analog_ids (Union[int, list[int]]): 模拟通道ID列表。
            idx_type (str): 索引类型，可选值：INDEX、CFGAN，默认值为INDEX。
            is_values (bool): 是否包含采样值。

        返回值:
            list: 通道选择器列表。
        """
        return self._get_selector(self.analogs, analog_ids, idx_type, is_values)

    def get_digital_selector(self, digital_ids: Union[int, list[int]] = None,
                             idx_type: str = "INDEX",
                             is_values: bool = False):
        """
        获取开关量选择器，返回开关量对象，不含采样值，选择通道selected为True

        参数:
            digital_ids (Union[int, list[int]]): 开关量ID列表。
            idx_type (str): 索引类型，可选值：INDEX、CFGAN，默认值为INDEX。
            is_values (bool): 是否包含采样值。

        返回值:
            list: 通道选择器列表。
        """
        channels = self._get_selector(self.digitals, digital_ids, idx_type, is_values)
        for index, channel in enumerate(channels):
            channel.index = index
        return channels

    def add_analog(self, analog: Analog, index: int = None):
        if analog is None:
            logger.error(f"传入通道对象为空")
            raise f"传入通道对象为空"
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

    @classmethod
    def from_string(cls, data_str: str) -> 'Configure':
        if not data_str or not isinstance(data_str, str):
            raise ComtradeDataFormatException(f"输入必须是非空字符串，当前类型: {type(data_str).__name__}")
        try:
            # 将字符串分隔为数组
            cfg_content = data_str.split("\n")
            _header = Header.from_string(cfg_content[0])
            _channel_num = ChannelNum.from_string(cfg_content[1])
            # 循环读取模拟量配置
            _analogs = []
            for i in range(2, 2 + _channel_num.analog_num):
                _analog = Analog.from_string(cfg_content[i])
                _analog.index = i - 2
                _analogs.append(_analog)
            # 循环读取开关量配置
            _digitals = []
            for i in range(2 + _channel_num.analog_num, 2 + _channel_num.total_num):
                _digital = Digital.from_string(cfg_content[i])
                _digital.index = i - 2 - _channel_num.analog_num
                _digitals.append(_digital)
            # 读取采样配置, 采样频率、采样段数、采样段
            freq = int(cfg_content[2 + _channel_num.total_num])
            nrate_num = int(cfg_content[3 + _channel_num.total_num])
            sample = ConfigSample(freg=freq, nrate_num=nrate_num)
            for i in range(4 + _channel_num.total_num, 4 + _channel_num.total_num + nrate_num):
                _nrate = Nrate.from_string(cfg_content[i])
                sample.add_nrate(_nrate)
            # 读取文件起始时间、故障时间、数据文件类型
            _file_start_time = PrecisionTime(cfg_content[4 + _channel_num.total_num + nrate_num])
            _fault_time = PrecisionTime(cfg_content[5 + _channel_num.total_num + nrate_num])
            sample.data_file_type = DataFileType.from_string(cfg_content[6 + _channel_num.total_num + nrate_num])
            sample.channel_num = _channel_num
            sample.calc_sampling()
            # 读取时间倍率,如果没有则默认1.0
            if len(cfg_content) >= 7 + _channel_num.total_num + nrate_num:
                _timemult = cfg_content[7 + _channel_num.total_num + nrate_num]
            else:
                _timemult = 1.0
            return cls(header=_header, channel_num=_channel_num, analogs=_analogs, digitals=_digitals, sample=sample,
                       file_start_time=_file_start_time, fault_time=_fault_time, timemult=TimeMult(timemult=_timemult))
        except IndexError as e:
            error_str = f"配置文件行数不对应，{e}"
            logger.error(error_str)
            raise ComtradeDataFormatException(error_str)
        except Exception as e:
            logger.error(f"输入字符串格式错误，{e}")
            raise ComtradeDataFormatException(f"输入字符串格式错误，{e}")
