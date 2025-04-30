#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field

from py3comtrade.model.analog import Analog
from py3comtrade.model.comtrade import Comtrade
from py3comtrade.model.configure import Configure
from py3comtrade.reader.data_reader import DataReader


class Modify(BaseModel):
    comtrade: Comtrade = Field(description="Comtrade对象")

    def modify_configure(self, configure: Configure) -> Comtrade:
        """
        修改配置文件
        """
        self.comtrade.configure = configure
        return self.comtrade

    def modify_data(self, data: DataReader) -> Comtrade:
        """
        修改数据文件
        """
        self.comtrade.data = data
        return self.comtrade

    def modify_analog(self, index: int, analog: Analog) -> Analog:
        """
        修改模拟量通道
        """
        analog = self.comtrade.configure.analogs[index]
        return analog
