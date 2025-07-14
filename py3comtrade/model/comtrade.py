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
from typing import Union

import numpy as np
from pydantic import BaseModel, Field

from py3comtrade.model.dmf import DMF
from .analog import Analog
from .configure import Configure
from .digital import Digital
from .digital_change_status import StatusRecord
from .type import FilePath, FloatArray32, IntArray32
from .type import PsType
from .type import SampleMode
from ..reader.data_reader import DataReader
from ..reader.dmf_reader import dmf_parser
from ..utils.cfg_to_dmf import CfgToDmf


class Comtrade(BaseModel):
    file_path: FilePath = Field(default=None, description="录波文件路径")
    configure: Configure = Field(default=None, description="Comtrade配置对象")
    data: DataReader = Field(default=None, description="Comtrade数据对象")
    dmf: DMF = Field(default=None, description="Comtrade数据对象")
    digital_change: list = Field(default_factory=list, description="变位开关量通道记录")

    def read_data(self):
        """
        获取dat数据
        """
        self.data = DataReader(file_path=self.file_path.get("dat_path"), sample=self.configure.sample)
        self.data.read()

    def read_dmf(self):
        """
        获取dmf数据
        """
        if self.file_path.get("dmf_path") is None:
            self.dmf = CfgToDmf(self.configure)
        else:
            self.dmf = dmf_parser(self.file_path.get("dmf_path"))

    def get_raw_by_analog_index(self, index: int, start_point: int = 0, end_point: int = None) -> FloatArray32:
        """
        获取指定模拟量通道、指定采样点的原始采样值\n
        :param index: 模拟量通道索引值
        :param start_point: 采样点开始位置
        :param end_point: 采样点结束位置
        :return: 原始采样值numpy数组
        """
        index = self._validate_index(index)
        start_point, end_point, _ = self.configure.get_cursor_sample_range(start_point, end_point)
        return self.data.analog_value.T[index:index + 1, start_point:end_point + 1]

    def get_raw_by_analog_indices(self, index: list[int] = None, start_point: int = 0,
                                  end_point: int = None) -> FloatArray32:
        """
        获取指定模拟量通道、指定采样点的原始采样值\n
        :param index: 模拟量通道索引值数组，当index为空时，默认为所有模拟量通道
        :param start_point: 采样点开始位置
        :param end_point: 采样点结束位置
        :return: 原始采样值numpy数组
        """
        # 当index为空时，默认获取所有模拟量通道
        analog_num_max = self.configure.channel_num.analog_num
        ids = list(range(analog_num_max)) if index is None else index
        if 0 <= max(ids) < analog_num_max:
            start_point, end_point, _ = self.configure.get_cursor_sample_range(start_point, end_point)
            return self.data.analog_value.T[ids, start_point:end_point + 1]
        raise ValueError(f"模拟量通道索引值超出范围！当前索引值: {index}, 允许范围: [0, {analog_num_max})")

    def get_raw_by_digital_index(self, index: int, start_point: int = 0, end_point: int = None) -> IntArray32:
        """
        获取指定开关量通道、指定采样点的原始采样值\n
        :param index: 开关量通道索引值
        :param start_point: 采样点开始位置
        :param end_point: 采样点结束位置
        :return: 原始采样值numpy数组
        """
        index = self._validate_index(index, is_analog=False)
        start_point, end_point, _ = self.configure.get_cursor_sample_range(start_point, end_point)
        return self.data.digital_value.T[index:index + 1, start_point:end_point + 1]

    def get_raw_by_digital_indices(self, index: list[int] = None, start_point: int = 0,
                                   end_point: int = None) -> IntArray32:
        """
        获取指定开关量通道、指定采样点的原始采样值\n
        :param index: 开关量通道索引值数组，当index为空时，默认为所有模拟量通道
        :param start_point: 采样点开始位置
        :param end_point: 采样点结束位置
        :return: 原始采样值numpy数组
        """
        digital_num_max = self.configure.channel_num.digital_num
        index = list(range(digital_num_max)) if index is None else index
        if 0 <= max(index) < digital_num_max:
            start_point, end_point, _ = self.configure.get_cursor_sample_range(start_point, end_point)
            return self.data.digital_value.T[index, start_point:end_point + 1]
        raise ValueError(f"开关量通道索引值超出范围！当前索引值: {index}, 允许范围: [0, {digital_num_max})")

    def get_instant_by_analog(self, analog: Analog, start_point: int = 0, end_point: int = None,
                              cycle_num: float = None, mode: SampleMode = SampleMode.FORWARD,
                              primary: bool = False) -> FloatArray32:
        """
        获取指定通道、指定采样点的瞬时采样值\n
        :param analog: 通道对象
        :param start_point: 采样点开始位置,默认为0
        :param end_point: 采样点结束位置,默认为None,代表全部采样点
        :param cycle_num: 采样周期数,默认为None,代表全部采样周期
        :param mode: 模式,默认为1,代表向后取值,0为前后取值,1为向前取值
        :param primary: 是否输出主变比值,默认为False,代表输出变比值
        :return: 瞬时值采样值numpy数组
        """
        start_point, end_point, _ = self.configure.get_cursor_sample_range(start_point, end_point, cycle_num, mode)
        # 获取原始值
        vs = self.get_raw_by_analog_index(analog.index, start_point, end_point)
        vs = vs[0] * analog.a + analog.b
        if primary:
            vs = vs if analog.ps == PsType.P else vs * analog.ratio
        else:
            vs = vs / analog.ratio if analog.ps == PsType.P else vs
        return np.around(vs, 3)

    def get_instant_by_multi_analog(self, analogs: list[Analog] = None, start_point: int = 0, end_point: int = None,
                                    cycle_num: float = None, mode: SampleMode = SampleMode.FORWARD,
                                    primary: bool = False) -> FloatArray32:
        """
        获取多个通道列表、指定采样点的瞬时采样值\n
        :param analogs: 通道对象列表,当列表为空获取全部的模拟量通道
        :param start_point: 采样点开始位置,默认为0
        :param end_point: 采样点结束位置,默认为None,代表全部采样点
        :param cycle_num: 采样周期数,默认为None,代表全部采样周期
        :param mode: 模式,默认为1,代表向后取值,0为前后取值,1为向前取值
        :param primary: 是否输出主变比值,默认为False,代表输出变比值
        :return 返回二维数组，x轴为通道索引，y轴为采样点
        """
        if analogs is None:
            analogs = self.configure.analogs
        start_point, end_point, _ = self.configure.get_cursor_sample_range(start_point, end_point, cycle_num, mode)
        vs = []
        for analog in analogs:
            vs.append(self.get_instant_by_analog(analog, start_point, end_point, cycle_num, mode, primary))
        return np.around(vs, 3)

    def get_instant_by_digital_index(self, index: int, start_point: int = 0, end_point: int = None,
                                     cycle_num: float = None, mode: SampleMode = SampleMode.FORWARD) -> IntArray32:
        """
        获取指定开关量、指定采样点的原始采样值\n
        :param index: 开关量通道索引值
        :param start_point: 采样点开始位置,默认为0
        :param end_point: 采样点结束位置,默认为None,代表全部采样点
        :param cycle_num: 采样周期数,默认为None,代表全部采样周期
        :param mode: 模式,默认为1,代表向后取值,0为前后取值,1为向前取值
        :return: 原始采样numpy数组
        """
        index = self._validate_index(index, is_analog=False)
        start_point, end_point, _ = self.configure.get_cursor_sample_range(start_point, end_point, cycle_num, mode)
        return self.data.digital_value.T[index:index + 1, start_point:end_point + 1]

    def get_instant_by_digital_indices(self, index: list[int] = None, start_point: int = 0,
                                       end_point: int = None, cycle_num: float = None,
                                       mode: SampleMode = SampleMode.FORWARD) -> IntArray32:
        """
        获取指定开关量、指定采样点的原始采样值\n
        :param index: 开关量通道索引值数组
        :param start_point: 采样点开始位置,默认为0
        :param end_point: 采样点结束位置,默认为None,代表全部采样点
        :param cycle_num: 采样周期数,默认为None,代表全部采样周期
        :param mode: 模式,默认为1,代表向后取值,0为前后取值,1为向前取值
        :return: 原始采样numpy数组
        """
        digital_num_max = self.configure.channel_num.digital_num
        index = list(range(digital_num_max)) if index is None else index
        if 0 <= max(index) < digital_num_max:
            start_point, end_point, _ = self.configure.get_cursor_sample_range(start_point, end_point, cycle_num, mode)
            return self.data.digital_value.T[index, start_point:end_point + 1]
        raise ValueError(f"开关量通道索引值超出范围！当前索引值: {index}, 允许范围: [0, {digital_num_max})")

    def get_instant_by_digital(self, digital: Digital, start_point: int = 0, end_point: int = None,
                               cycle_num: float = None, mode: SampleMode = SampleMode.FORWARD) -> np.ndarray:
        """
        获取指定通道、指定采样点的瞬时采样值
        :param digital: 通道对象
        :param start_point: 采样点开始位置,默认为0
        :param end_point: 采样点结束位置,默认为None,代表全部采样点
        :param cycle_num: 采样周期数,默认为None,代表全部采样周期
        :param mode: 模式,默认为1,代表向后取值,0为前后取值,1为向前取值
        """
        return self.get_instant_by_digital_index(digital.index, start_point, end_point, cycle_num, mode)

    def get_instant_by_multi_digital(self, digitals: list[Digital] = None, start_point: int = 0, end_point: int = None,
                                     cycle_num: float = None, mode: SampleMode = SampleMode.FORWARD) -> IntArray32:
        """
        获取指定通道列表、指定采样点的瞬时采样值\n
        :param digitals: 通道对象列表
        :param start_point: 采样点开始位置,默认为0
        :param end_point: 采样点结束位置,默认为None,代表全部采样点
        :param cycle_num: 采样周波数量
        :param mode: 取值方式
        """
        digital_num_max = self.configure.channel_num.digital_num
        index = list(range(digital_num_max)) if digitals is None else [d.index for d in digitals if hasattr(d, 'index')]
        if 0 <= max(index) < digital_num_max:
            start_point, end_point, _ = self.configure.get_cursor_sample_range(start_point, end_point, cycle_num, mode)
            return self.data.digital_value.T[index, start_point:end_point + 1]
        raise ValueError(f"开关量通道索引值超出范围！当前索引值: {index}, 允许范围: [0, {digital_num_max})")

    def get_instant_digital_change_digital(self):
        self.analyze_digital_change_status()
        return self.get_instant_by_multi_digital(self.digital_change)

    def analyze_digital_change_status(self):
        """
        获取发生变位的开关量对象列表\n
        """
        self.digital_change = []
        for ch in range(self.data.digital_value.shape[1]):
            col = self.data.digital_value[:, ch]
            digital = self.configure.digitals[ch]
            status_record = StatusRecord(timestamp=0, status=col[0].item())
            digital.change_status.append(status_record)
            if col.min() != col.max():
                # 找出变化点：当前值与前一个值不同
                change_indices = np.where(col[:-1] != col[1:])[0] + 1
                # 获取变化后的值
                change_vs = col[change_indices]
                for i in range(len(change_vs)):
                    status_record = StatusRecord(timestamp=change_indices[i].item(), status=change_vs[i].item())
                    digital.change_status.append(status_record)
                self.digital_change.append(digital)

    def get_instant_by_segment(self, segment_index, primary: bool = False,
                               analog: Union[Analog, list[Analog]] = None):
        """
        获取指定采样段、指定通道的瞬时采样值
        :param segment_index: 分段索引
        :param primary: 是否输出主变比值,默认为False,代表输出变比值
        :param analog: 通道对象,默认为None,代表输出全部通道
        :return: 瞬时值采样值numpy数组
        """
        segment = self.configure.sample.nrates[segment_index]
        if isinstance(analog, Analog):
            return self.get_instant_by_analog(analog, segment.start_point, segment.end_point, primary)
        if isinstance(analog, list):
            return self.get_instant_by_multi_analog(analog, segment.start_point, segment.end_point, primary)
        if analog is None:
            return self.get_instant_by_multi_analog(self.configure.analogs, segment.start_point, segment.end_point,
                                                    primary)

    def _validate_index(self, index: int, is_analog: bool = True) -> int:
        """
        模拟量通道索引值合法性检测
        :param index: 通道索引值
        :param is_analog: 检查模拟量类型
        """
        if not isinstance(index, int):
            raise TypeError(f"通道索引值类型错误！需要 int 类型，但收到 {type(index).__name__}。")
        index_max = self.configure.channel_num.analog_num if is_analog else self.configure.channel_num.digital_num
        if not (0 <= index < index_max):
            raise ValueError(f"通道索引值超出范围！当前索引值: {index}, 允许范围: [0, {index_max})")
        return index
