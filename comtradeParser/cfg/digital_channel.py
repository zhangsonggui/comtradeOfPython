#!/usr/bin/env python
# -*- coding: utf-8 -*-


class DigitalChannel:
    """
    开关量通道对象
    """
    _dn: int = 0
    _chid: str = ''
    _ph: str = ''
    _ccbm: str = ''
    _y: int = 0

    def __init__(self, dn, chid, ph, ccbm, y):
        self.clear()
        self._dn = dn
        self._chid = chid
        self._ph = ph
        self._ccbm = ccbm
        self._y = y

    def clear(self):
        self._dn = 0
        self._chid = ''
        self._ph = ''
        self._ccbm = ''
        self._y = 0

    def to_string(self):
        """从对象生成字符串"""
        parts = [str(self._dn), self._chid, self._ph, self._ccbm, self._y]
        # 移除末尾的空字符串以保持与原始解析逻辑一致
        while parts and not parts[-1]:
            parts.pop()
        return ','.join(parts)

    @property
    def dn(self):
        return self._dn

    @dn.setter
    def dn(self, value):
        self._dn = value

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
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value


def parse_digital_channel(channel_str):
    """从字符串解析成对象"""
    channel_info = channel_str.split(',')
    return DigitalChannel(
        dn=int(channel_info[0]),
        chid=channel_info[1],
        ph=channel_info[2],
        ccbm=channel_info[3],
        y=channel_info[4].rstrip(),
    )


def generate_analog_channel_str(analog_channel_obj):
    """直接使用对象的方法生成字符串"""
    return analog_channel_obj.to_string()
