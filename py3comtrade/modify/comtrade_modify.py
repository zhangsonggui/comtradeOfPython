from typing import Generic, TypeVar

from py3comtrade.model.analog import Analog
from py3comtrade.model.comtrade import Comtrade
from py3comtrade.model.digital import Digital

T = TypeVar("T", Analog, Digital)


class ComtradeModify(Comtrade, Generic[T]):

    def add_channel(self, channel: T, index: int = None, *, is_analog: bool = True):
        """
        添加模拟量或开关量通道
        :param channel: 通道对象（Analog 或 Digital）
        :param index: 插入位置
        :param is_analog: 是否为模拟量通道
        :return:
        """
        if is_analog:
            analogs = self.configure.analogs
            if index is None or index >= len(analogs):
                analogs.append(channel)
            else:
                analogs.insert(index, channel)
        else:
            digitals = self.configure.digitals
            if index is None or index >= len(digitals):
                digitals.append(channel)
            else:
                digitals.insert(index, channel)

    def edit_channel(self, channel: T, index: int):
        """
        修改通道对象
        :param channel: 待修改的通道对象
        :param index: 修改位置
        :return:
        """
        if isinstance(channel, Analog):
            pass
