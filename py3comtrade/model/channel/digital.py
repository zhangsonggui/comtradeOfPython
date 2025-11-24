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
from typing import List

from pydantic import BaseModel, Field

from py3comtrade.model.channel.channel import ChannelBase
from py3comtrade.model.exceptions import ComtradeDataFormatException
from py3comtrade.model.type import Phase
from py3comtrade.model.type.digital_enum import Contact
from py3comtrade.model.type.types import IdxType


class StatusRecord(BaseModel):
    """表示一个变为记录的模型类，包含时间戳和状态"""
    sample_point: int = Field(description="采样点")
    timestamp: int = Field(description="时间戳")
    status: int = Field(description="状态")


class Digital(ChannelBase):
    """
    开关量通道类
    """
    contact: Contact = Field(default=Contact.NORMALLY_OPEN, description="状态通道正常状态")
    change_status: List[StatusRecord] = Field(default_factory=list, description="变位记录")

    def clear(self) -> None:
        """清除模型中所有字段"""
        super().clear()
        for field in self.model_fields.keys():
            setattr(self, field, None)

    def is_change(self):
        return len(self.change_status) > 1

    def is_enable(self):
        return super().is_enable() or self.is_change()

    def is_selected(self, target: list = None, target_type: IdxType = IdxType.INDEX):
        """判断通道是否被选中"""
        if target is None:
            self.selected = self.is_change()
            return self.selected
        return super().is_selected(target, target_type)

    @classmethod
    def from_string(cls, data_str: str) -> 'Digital':
        """
        从字符串创建Digital对象
        :param data_str: 包含Digital对象属性的字符串
        :return: Digital对象实例
        """
        if not data_str or not isinstance(data_str, str):
            raise ComtradeDataFormatException(f"输入字符串不能为空或不是字符串类型")

        parts = data_str.strip().split(',')
        if len(parts) < 3:
            raise ComtradeDataFormatException(f"输入字符串格式错误，期望3个逗号分隔的字段，实际得到{len(parts)}个")
        try:
            idx_cfg = int(parts[0])
            name = f"chid-{idx_cfg}" if not parts[1].strip() else parts[1]
            digital = cls(idx_cfg=idx_cfg, name=name)

            if len(parts) == 3 and parts[2] == '1':
                digital.contact = Contact.NORMALLY_CLOSED
            if len(parts) >= 3:
                digital.phase = Phase.from_string(parts[2], default=Phase.NO_PHASE)
            if len(parts) >= 4:
                digital.ccbm = parts[3]
            if len(parts) >= 5 and parts[4] == '1':
                digital.contact = Contact.NORMALLY_CLOSED
            return digital
        except ValueError as e:
            raise ValueError(f"创建Digital对象时发生错误: {str(e)}") from e

    @classmethod
    def from_dict(cls, data_dict: dict) -> 'Digital':
        """
        从字典创建Digital对象
        :param data_dict: 包含Digital对象属性的字典
        :return: Digital对象实例
        """
        if not data_dict or not isinstance(data_dict, dict):
            raise ComtradeDataFormatException(f"输入字典不能为空或不是字典类型")
        try:
            base_params = {
                "idx_cfg": data_dict.get("idx_cfg", 0),
                "name"   : data_dict.get("name", f"chid-{data_dict.get('idx_cfg', 0)}"),
                "phase"  : data_dict.get("phase", Phase.NO_PHASE),
                "ccbm"   : data_dict.get("ccbm", ""),
                "contact": data_dict.get("contact", Contact.NORMALLY_OPEN)
            }
            digital = cls(**base_params)
            return digital
        except ValueError as e:
            raise ValueError(f"创建Digital对象时发生错误: {str(e)}") from e

    def __str__(self):
        contact_code = 1 if self.contact == Contact.NORMALLY_CLOSED else 0
        return super().__str__() + f",{contact_code}"
