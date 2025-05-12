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


class ConfigHeader(BaseModel):
    """
    cfg文件头部信息，变电站名称，录波设备名称和录波格式版本号
    """

    station_name: str = Field(default="变电站", description="变电站名称")
    recorder_name: str = Field(default="录波设备", description="录波设备名称")
    version: int = Field(default=1991, description="录波格式版本号")

    def clear(self):
        """清除模型中所有字段"""
        for field in self.model_fields.keys():
            setattr(self, field, None)

    def __str__(self):
        return f"{self.station_name},{self.recorder_name},{self.version}"
