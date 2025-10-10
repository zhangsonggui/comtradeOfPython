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
        self._filtered_config = copy.deepcopy(comtrade)

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
        self._filtered_config.digitals = []
        return self

    def digital_only(self) -> 'ComtradeFilter':
        """
        只保留开关量通道
        
        返回值:
            过滤器实例，支持链式调用
        """
        self._filtered_config.analogs = []
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
            self._filtered_config.analogs = [
                a for a in self._filtered_config.analogs if a.index in analog_index
            ]
            # 重新设置索引
            for i, analog in enumerate(self._filtered_config.analogs):
                analog.index = i

        # 处理开关量通道索引筛选
        if digital_index is not None:
            if not isinstance(digital_index, list):
                digital_index = [digital_index]

            # 筛选开关量通道
            self._filtered_config.digitals = [
                d for d in self._filtered_config.digitals if d.index in digital_index
            ]
            # 重新设置索引
            for i, digital in enumerate(self._filtered_config.digitals):
                digital.index = i

        # 更新通道数量信息
        self._filtered_config.channel_num.analog_num = len(self._filtered_config.analogs)
        self._filtered_config.channel_num.digital_num = len(self._filtered_config.digitals)

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
            self._filtered_config.analogs = [
                a for a in self._filtered_config.analogs if a.idx_cfg in analog_cfgan
            ]
            # 重新设置索引
            for i, analog in enumerate(self._filtered_config.analogs):
                analog.index = i

        # 处理开关量通道cfgan筛选
        if digital_cfgan is not None:
            if not isinstance(digital_cfgan, list):
                digital_cfgan = [digital_cfgan]

            # 筛选开关量通道
            self._filtered_config.digitals = [
                d for d in self._filtered_config.digitals if d.idx_cfg in digital_cfgan
            ]
            # 重新设置索引
            for i, digital in enumerate(self._filtered_config.digitals):
                digital.index = i

        # 更新通道数量信息
        self._filtered_config.channel_num.analog_num = len(self._filtered_config.analogs)
        self._filtered_config.channel_num.digital_num = len(self._filtered_config.digitals)

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
        self._filtered_config.analogs = [
            a for a in self._filtered_config.analogs if a.selected == is_selected
        ]
        # 重新设置索引
        for i, analog in enumerate(self._filtered_config.analogs):
            analog.index = i

        # 筛选开关量通道
        self._filtered_config.digitals = [
            d for d in self._filtered_config.digitals if d.selected == is_selected
        ]
        # 重新设置索引
        for i, digital in enumerate(self._filtered_config.digitals):
            digital.index = i

        # 更新通道数量信息
        self._filtered_config.channel_num.analog_num = len(self._filtered_config.analogs)
        self._filtered_config.channel_num.digital_num = len(self._filtered_config.digitals)

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
        for analog in self._filtered_config.analogs:
            analog.values = []
        # 移除开关量采样值
        for digital in self._filtered_config.digitals:
            digital.values = []
        return self

    def build(self) -> 'Comtrade':
        """
        构建并返回过滤后的Comtrade对象
        
        返回值:
            过滤后的Comtrade对象
        """
        return self._filtered_config
