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

import copy
from typing import TYPE_CHECKING, Union

from py3comtrade.model.type.analog_enum import PsType
from py3comtrade.model.type.types import ValueType

if TYPE_CHECKING:
    from py3comtrade.model.comtrade import Comtrade


class ComtradeFilter:
    """
    Comtrade对象过滤器类，用于链式调用筛选配置对象中的通道
    """

    def __init__(self, comtrade: 'Comtrade'):
        """
        初始化过滤器
        
        参数:
            Comtrade: 要过滤的Comtrade对象
        """
        self._filtered_comtrade = copy.deepcopy(comtrade)

    def filter_by_channel_type(self, channel_type: str) -> 'ComtradeFilter':
        """
        根据通道类型筛选
        
        参数:
            channel_type: 通道类型，可选值：'analog', 'digital'
        
        返回值:
            过滤器实例，支持链式调用
        """
        if channel_type.lower() == 'analog':
            return self.analog_only()
        elif channel_type.lower() == 'digital':
            return self.digital_only()
        return self

    def analog_only(self) -> 'ComtradeFilter':
        """
        只保留模拟通道
        
        返回值:
            过滤器实例，支持链式调用
        """
        self._filtered_comtrade.digitals = []
        return self

    def digital_only(self) -> 'ComtradeFilter':
        """
        只保留开关量通道
        
        返回值:
            过滤器实例，支持链式调用
        """
        self._filtered_comtrade.analogs = []
        return self

    def by_index(self, analog_index: Union[int, list[int]] = None,
                 digital_index: Union[int, list[int]] = None) -> 'ComtradeFilter':
        """
        根据通道index索引筛选
        
        参数:
            analog_index: 模拟通道索引或索引列表
            digital_index: 开关量通道索引或索引列表
        
        返回值:
            过滤器实例，支持链式调用
        """
        # 处理模拟通道索引筛选
        if analog_index is not None:
            if not isinstance(analog_index, list):
                analog_index = [analog_index]

            # 筛选模拟通道
            self._filtered_comtrade.analogs = [
                a for a in self._filtered_comtrade.analogs if a.index in analog_index
            ]
            # 重新设置索引
            for i, analog in enumerate(self._filtered_comtrade.analogs):
                analog.index = i

        # 处理开关量通道索引筛选
        if digital_index is not None:
            if not isinstance(digital_index, list):
                digital_index = [digital_index]

            # 筛选开关量通道
            self._filtered_comtrade.digitals = [
                d for d in self._filtered_comtrade.digitals if d.index in digital_index
            ]
            # 重新设置索引
            for i, digital in enumerate(self._filtered_comtrade.digitals):
                digital.index = i

        # 更新通道数量信息
        self._filtered_comtrade.channel_num.analog_num = len(self._filtered_comtrade.analogs)
        self._filtered_comtrade.channel_num.digital_num = len(self._filtered_comtrade.digitals)

        return self

    def by_cfgan(self, analog_cfgan: Union[int, list[int]] = None,
                 digital_cfgan: Union[int, list[int]] = None) -> 'ComtradeFilter':
        """
        根据通道cfgan筛选
        
        参数:
            analog_cfgan: 模拟通道cfgan或cfgan列表
            digital_cfgan: 开关量通道cfgan或cfgan列表
        
        返回值:
            过滤器实例，支持链式调用
        """
        # 处理模拟通道cfgan筛选
        if analog_cfgan is not None:
            if not isinstance(analog_cfgan, list):
                analog_cfgan = [analog_cfgan]

            # 筛选模拟通道
            self._filtered_comtrade.analogs = [
                a for a in self._filtered_comtrade.analogs if a.idx_cfg in analog_cfgan
            ]
            # 重新设置索引
            for i, analog in enumerate(self._filtered_comtrade.analogs):
                analog.index = i

        # 处理开关量通道cfgan筛选
        if digital_cfgan is not None:
            if not isinstance(digital_cfgan, list):
                digital_cfgan = [digital_cfgan]

            # 筛选开关量通道
            self._filtered_comtrade.digitals = [
                d for d in self._filtered_comtrade.digitals if d.idx_cfg in digital_cfgan
            ]
            # 重新设置索引
            for i, digital in enumerate(self._filtered_comtrade.digitals):
                digital.index = i

        # 更新通道数量信息
        self._filtered_comtrade.channel_num.analog_num = len(self._filtered_comtrade.analogs)
        self._filtered_comtrade.channel_num.digital_num = len(self._filtered_comtrade.digitals)

        return self

    def by_selected(self, is_selected: bool) -> 'ComtradeFilter':
        """
        根据通道selected状态筛选
        
        参数:
            is_selected: 是否选中
        
        返回值:
            过滤器实例，支持链式调用
        """
        # 筛选模拟通道
        self._filtered_comtrade.analogs = [
            a for a in self._filtered_comtrade.analogs if a.selected == is_selected
        ]
        # 重新设置索引
        for i, analog in enumerate(self._filtered_comtrade.analogs):
            analog.index = i

        # 筛选开关量通道
        self._filtered_comtrade.digitals = [
            d for d in self._filtered_comtrade.digitals if d.selected == is_selected
        ]
        # 重新设置索引
        for i, digital in enumerate(self._filtered_comtrade.digitals):
            digital.index = i

        # 更新通道数量信息
        self._filtered_comtrade.channel_num.analog_num = len(self._filtered_comtrade.analogs)
        self._filtered_comtrade.channel_num.digital_num = len(self._filtered_comtrade.digitals)

        return self

    def values_type(self, target_value_type: str):
        """
        根据目标数值类型,对通道采样值进行转换

        参数:
            target_value_type: 目标数值类型,可选择是raw、instant

        返回值:
            过滤器实例，支持链式调用
        """
        target_value_type = ValueType.from_string(target_value_type)
        for analog in self._filtered_comtrade.analogs:
            analog.convert_values_type(target_value_type)
        self._filtered_comtrade.sample.value_type = target_value_type
        return self

    def values_ps(self, target_ps: str):
        """
        对通道采样值进行一二次值转换

        参数:
            target_ps: 目标数值类型,可选择是p、s

        返回值:
            过滤器实例，支持链式调用
        """
        target_ps = PsType.from_string(target_ps)
        for analog in self._filtered_comtrade.analogs:
            analog.convert_values_ps(target_ps)
        return self

    def by_samp_point(self, start_point: int, end_point: int):
        """
        根据采样点对采样值进行切片
        参数:
            start_point: 开始采样点
            end_point: 结束采样点
        返回值:
            过滤器实例,支持链式调用
        """
        start_point, end_point, _ = self._filtered_comtrade.get_cursor_sample_range(start_point, end_point)
        # 切片模拟量采样值
        for analog in self._filtered_comtrade.analogs:
            analog.values = analog.values[start_point:end_point]
        # 切片开关量采样值
        for digital in self._filtered_comtrade.digitals:
            digital.values = digital.values[start_point:end_point]
        return self

    def by_segment(self, segment: int):
        """
        根据采样段对采样值进行切片
        参数:
            segment: 采样段号
        返回值:
            过滤器实例,支持链式调用
        """
        if 0 <= segment <= self._filtered_comtrade.sample.nrate_num:
            nrate = self._filtered_comtrade.sample.nrates[segment]
            start_point = nrate.start_point
            end_point = nrate.end_point
            # 切片模拟量采样值
            for analog in self._filtered_comtrade.analogs:
                analog.values = analog.values[start_point:end_point]
            # 切片开关量采样值
            for digital in self._filtered_comtrade.digitals:
                digital.values = digital.values[start_point:end_point]
        return self

    def clear_channel_values(self) -> 'ComtradeFilter':
        """
        删除对象中的采样值信息

        参数:
            无

        返回值:
            过滤器实例，支持链式调用
        """
        # 移除模拟量采样值
        for analog in self._filtered_comtrade.analogs:
            analog.values = []
        # 移除开关量采样值
        for digital in self._filtered_comtrade.digitals:
            digital.values = []
        return self

    def build(self) -> 'Comtrade':
        """
        构建并返回过滤后的Comtrade对象
        
        返回值:
            过滤后的Comtrade对象
        """
        return self._filtered_comtrade
