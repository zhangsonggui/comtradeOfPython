#!/usr/bin/env python
# -*- coding: utf-8 -*-

class AnalogChannel:
    """
    模拟量通道类
    """

    def __init__(self, an: int, chid: str, ph: str, ccbm: str, uu: str, a: float, b: float, skew: float, min_val: float,
                 max_val: float, primary: float = 0.0, secondary: float = 0.0, ps: str = "S", ratio: float = 0.0):
        self.clear()
        self._an = an
        self._chid = chid
        self._ph = ph
        self._ccbm = ccbm
        self._uu = uu
        self._a = a
        self._b = b
        self._skew = skew
        self._min = min_val
        self._max = max_val
        self._primary = primary
        self._secondary = secondary
        self._ps = ps
        self._ratio = ratio

    def clear(self):
        self._an = 0
        self._chid = ''
        self._ph = ''
        self._ccbm = ''
        self._uu = ''
        self._a = 0.0
        self._b = 0.0
        self._skew = 0.0
        self._min = 0.0
        self._max = 0.0
        self._primary = 0.0
        self._secondary = 0.0
        self._ps = ''
        self._ratio = 0.0

    def to_string(self):
        """从对象生成字符串"""
        parts = [str(self._an), self._chid, self._ph, self._ccbm, self._uu,
                 str(self._a), str(self._b), str(self._skew), str(self._min), str(self._max),
                 str(self._primary), str(self._secondary), self._ps]
        # 移除末尾的空字符串以保持与原始解析逻辑一致
        while parts and not parts[-1]:
            parts.pop()
        return ','.join(parts)

    @property
    def an(self):
        return self._an

    @an.setter
    def an(self, value):
        self._an = value

    @property
    def chid(self):
        return self._chid

    @chid.setter
    def chid(self, value):
        self._chid = value

    @property
    def ph(self):
        return self._ph

    @ph.setter
    def ph(self, value):
        self._ph = value

    @property
    def ccbm(self):
        return self._ccbm

    @ccbm.setter
    def ccbm(self, value):
        self._ccbm = value

    @property
    def uu(self):
        return self._uu

    @uu.setter
    def uu(self, value):
        self._uu = value

    @property
    def a(self):
        return self._a

    @a.setter
    def a(self, value):
        self._a = value

    @property
    def b(self):
        return self._b

    @b.setter
    def b(self, value):
        self._b = value

    @property
    def skew(self):
        return self._skew

    @skew.setter
    def skew(self, value):
        self._skew = value

    @property
    def min(self):
        return self._min

    @min.setter
    def min(self, value):
        self._min = value

    @property
    def max(self):
        return self._max

    @max.setter
    def max(self, value):
        self._max = value

    @property
    def primary(self):
        return self._primary

    @primary.setter
    def primary(self, value):
        self._primary = value
        self.ratio = self.primary / self.secondary

    @property
    def secondary(self):
        return self._secondary

    @secondary.setter
    def secondary(self, value):
        if value != 0:
            self._secondary = value
        else:
            raise Exception("二次值不能为0")

    @property
    def ps(self):
        return self._ps

    @ps.setter
    def ps(self, value):
        self._ps = value

    @property
    def ratio(self):
        self.ratio = self._primary / self._secondary
        return self._ratio

    @ratio.setter
    def ratio(self, value):
        self._ratio = value


def parse_analog_channel(channel_str):
    """从字符串解析成对象"""
    channel_info = channel_str.split(',')
    ps = channel_info[12].rstrip() if len(channel_info) > 12 else "S"
    uu = channel_info[4].upper()
    if uu == ['KV', 'KA']:
        ps = 'P'
    return AnalogChannel(
        an=int(channel_info[0]),
        chid=channel_info[1],
        ph=channel_info[2],
        ccbm=channel_info[3],
        uu=channel_info[4],
        a=float(channel_info[5]),
        b=float(channel_info[6]),
        skew=float(channel_info[7]),
        min_val=int(channel_info[8]),
        max_val=int(channel_info[9]),
        primary=float(channel_info[10]) if len(channel_info) > 10 else 1.0,
        secondary=float(channel_info[11]) if len(channel_info) > 11 else 1.0,
        ps=ps
    )


def generate_analog_channel_str(analog_channel_obj):
    """直接使用对象的方法生成字符串"""
    return analog_channel_obj.to_string()
