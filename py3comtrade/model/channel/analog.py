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

import numpy as np
from pydantic import Field, field_validator

from py3comtrade.dispose.channel_name import analog_channel_classification
from py3comtrade.model.channel.channel import ChannelBase
from py3comtrade.model.exceptions import ComtradeDataFormatException
from py3comtrade.model.type import Phase
from py3comtrade.model.type.analog_enum import AnalogFlag, PsType, Unit
from py3comtrade.model.type.types import IdxType, ValueType
from py3comtrade.utils import parse_float, safe_float_convert


class Analog(ChannelBase):
    unit: Unit = Field(default=Unit.NONE, description="通道单位")
    a: float = Field(default=1.0, description="通道增益系数")
    b: float = Field(default=0.0, description="通道偏移系数")
    skew: float = Field(default=0.0, description="通道时滞（us）")
    min_val: float = Field(default=0.0, description="通道最小值")
    max_val: float = Field(default=0.0, description="通道最大值")
    primary: float = Field(default=1.0, description="通道互感器变比一次系数")
    secondary: float = Field(default=1.0, description="通道互感器变比二次系数")
    ps: PsType = Field(default=PsType.P, description="一次还是二次值标识")
    ratio: float = Field(default=1.0, description="通道比率")

    def clear(self) -> None:
        """清除模型中所有字段"""
        super().clear()
        for field in self.__class__.model_fields.keys():
            setattr(self, field, None)

    @classmethod
    @field_validator('secondary')
    def secondary_must_not_be_zero(cls, v):
        if v == 0:
            raise ValueError(f"secondary属性不能为0")
        return v

    def is_enable(self) -> bool:
        """根据通道名称和变比判断该通道是否使用"""
        return super().is_enable() and self.ratio > 1

    def channel_flag(self) -> AnalogFlag:
        """根据通道名称和单位判断通道类型"""
        return analog_channel_classification(self.name, self.unit)

    def is_selected(self, target: list = None, target_type: IdxType = IdxType.INDEX):
        """判断通道是否被选中"""
        if target is None:
            self.selected = self.is_enable()
            return self.selected
        return super().is_selected(target, target_type)

    def convert_values_type(self, target_value_type: ValueType) -> list:
        """原始采样值瞬时值间转换"""
        # 判断是否存在values属性,如果属性不存在或为空直接返回空列表
        if self.hasattr_values:
            if target_value_type == self.values_type:
                return self.values
            if target_value_type == ValueType.RAW:
                self.values = np.round(self.values).astype(int).tolist()
            else:
                self.values = [(v * self.a + self.b) for v in self.values]
            self.values_type = target_value_type
            return self.values
        return []

    def convert_values_ps(self, target_ps: PsType) -> list[float]:
        """一二次值转换"""
        self.convert_values_type(ValueType.INSTANT)
        if target_ps == self.ps:
            return self.values
        if target_ps == PsType.P:
            self.values = [v * self.ratio for v in self.values]
        else:
            self.values = [v / self.ratio for v in self.values]
        self.ps = target_ps
        return self.values

    @classmethod
    def from_string(cls, data_str: str) -> 'Analog':
        """
        从字符串创建Analog对象
        :param data_str: 包含Analog对象属性的字符串
        :return: Analog对象实例
        :raises ComtradeDataFormatException: 当数据格式不正确时
        :raises ValueError: 当参数类型转换失败时
        """
        if not data_str or not isinstance(data_str, str):
            raise ComtradeDataFormatException(f"输入必须是非空字符串，当前类型: {type(data_str).__name__}")

        parts = data_str.split(',')
        if len(parts) < 10:
            raise ComtradeDataFormatException(
                f"数据格式不正确，需要至少10个字段，当前有{len(parts)}个: {data_str}"
            )

        try:
            # 基础参数解析和验证
            idx_cfg = int(parts[0])
            name = f"chid-{idx_cfg}" if not parts[1].strip() else parts[1]

            # 主要参数构建
            base_params = {
                'idx_cfg': idx_cfg,
                'name'   : name,
                'phase'  : Phase.from_string(parts[2], default=Phase.NO_PHASE),
                'ccbm'   : parts[3],
                'unit'   : Unit.from_string(parts[4], default=Unit.NONE),
                'a'      : parse_float(parts[5], 1.0),
                'b'      : parse_float(parts[6], 0.0),
                'skew'   : parse_float(parts[7], 0.0),
                'min_val': parse_float(parts[8], 0.0),
                'max_val': parse_float(parts[9], 0.0)
            }

            # 创建基础对象
            analog = cls(**base_params)

            # 扩展参数处理
            if len(parts) > 11:
                primary = parse_float(parts[10], 1.0)
                secondary = parse_float(parts[11], 1.0)

                # 预先验证secondary不为0
                if secondary == 0:
                    raise ValueError("secondary属性不能为0")

                analog.primary = primary
                analog.secondary = secondary
                analog.ps = PsType.from_string(parts[12], default=PsType.S) if len(parts) > 12 else PsType.S
                analog.ratio = primary / secondary

            return analog

        except ValueError as e:
            raise ValueError(f"参数转换失败: {str(e)}, 数据: {data_str}") from e
        except Exception as e:
            if isinstance(e, (ComtradeDataFormatException, ValueError)):
                raise
            raise ComtradeDataFormatException(f"创建Analog对象时发生错误: {str(e)}") from e

    @classmethod
    def from_dict(cls, data_dict: dict) -> 'Analog':
        """
        从字典创建Analog对象
        
        :param data_dict: 包含Analog对象属性的字典
        :return: Analog对象实例
        :raises TypeError: 当输入不是字典时
        :raises ValueError: 当参数类型转换失败时
        :raises ComtradeDataFormatException: 当数据格式不正确时
        """
        if not data_dict or not isinstance(data_dict, dict):
            raise TypeError(f"期望字典类型输入，实际得到: {type(data_dict).__name__}")

        try:
            # 基础参数构建
            base_params = {
                'idx_cfg': int(data_dict.get('idx_cfg', 0)),
                'name'   : str(data_dict.get('name', f"chid-{data_dict.get('idx_cfg', 0)}")),
                'phase'  : Phase.from_string(str(data_dict.get('phase', '')), default=Phase.NO_PHASE),
                'ccbm'   : str(data_dict.get('ccbm', '')),
                'unit'   : Unit.from_string(str(data_dict.get('unit', '')), default=Unit.NONE),
                'a'      : safe_float_convert(data_dict.get('a'), 'a', 1.0),
                'b'      : safe_float_convert(data_dict.get('b'), 'b', 0.0),
                'skew'   : safe_float_convert(data_dict.get('skew'), 'skew', 0.0),
                'min_val': safe_float_convert(data_dict.get('min_val'), 'min_val', 0.0),
                'max_val': safe_float_convert(data_dict.get('max_val'), 'max_val', 0.0)
            }

            # 验证必填字段
            if not base_params['name'].strip():
                raise ValueError("通道名称不能为空")

            # 创建基础对象
            analog = cls(**base_params)

            # 处理一二次值参数
            if 'primary' in data_dict and 'secondary' in data_dict:
                primary = safe_float_convert(data_dict['primary'], 'primary')
                secondary = safe_float_convert(data_dict['secondary'], 'secondary')

                if secondary == 0:
                    raise ValueError("secondary属性不能为0，会导致除零错误")

                analog.primary = primary
                analog.secondary = secondary
                analog.ps = PsType.from_string(str(data_dict.get('ps', '')), default=PsType.S)
                analog.ratio = primary / secondary

            return analog

        except (ValueError, TypeError) as e:
            # 直接传递这些特定异常，提供更具体的错误信息
            raise
        except Exception as e:
            # 包装其他异常为ComtradeDataFormatException
            raise ComtradeDataFormatException(f"从字典创建Analog对象时发生错误: {str(e)}") from e

    def __str__(self):
        return (
                super().__str__()
                + f",{self.unit.code},{self.a},{self.b},{self.skew},{self.min_val},{self.max_val}"
                + f",{self.primary},{self.secondary},{self.ps.code}"
        )
