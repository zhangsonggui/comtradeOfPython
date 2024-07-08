#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (C) 2024 - 2024 张松贵, Inc. All Rights Reserved
# 开关量通道类
# @FileName  :digital_channel.py
# @Time      :2024/07/05 13:53:42
# @Author    :张松贵

class DigitalChannel:
    """
    开关量通道对象
    """

    def __init__(self, dn: int, chid: str, ph: str, ccbm: str, y: int):
        """
        :param dn: 状态通道索引号，必选，整数，不要求前导0或空格。顺序计数范围从1开始
        :param chid: 通道名，必选，字母数字，最小长度1个字符，最大128个字符
        :param ph: 通道相别标识，可选，字母数字，最小长度0个字符，最大2个字符
        :param ccbm: 被监视电路元件，可选，字母数字，最小长度0个字符，最大64个字符
        :param y: 状态通道正常状态，必选，整数，数字，0表示低电平，1表示高电平
        """
        self.clear()
        self.__dn = dn
        self.__chid = chid
        self.__ph = ph
        self.__ccbm = ccbm
        self.__y = y

    def clear(self):
        self.__dn = 0
        self.__chid = ''
        self.__ph = ''
        self.__ccbm = ''
        self.__y = 0

    def to_string(self):
        """从对象生成字符串"""
        parts = [str(self.__dn), self.__chid, self.__ph, self.__ccbm, self.__y]
        # 移除末尾的空字符串以保持与原始解析逻辑一致
        while parts and not parts[-1]:
            parts.pop()
        return ','.join(parts)

    @property
    def dn(self):
        """状态通道索引号"""
        return self.__dn

    @dn.setter
    def dn(self, value):
        """状态通道索引号"""
        self.__dn = value

    @property
    def chid(self):
        """通道名"""
        return self.__chid

    @chid.setter
    def chid(self, value):
        """通道名"""
        self.__chid = value

    @property
    def ph(self):
        """通道相别标识"""
        return self.__ph

    @ph.setter
    def ph(self, value):
        """通道相别标识"""
        self.__ph = value

    @property
    def ccbm(self):
        """被监视电路元件"""
        return self.__ccbm

    @ccbm.setter
    def ccbm(self, value):
        """被监视电路元件"""
        self.__ccbm = value

    @property
    def y(self):
        """状态通道正常状态"""
        return self.__y

    @y.setter
    def y(self, value):
        """状态通道正常状态"""
        self.__y = value
