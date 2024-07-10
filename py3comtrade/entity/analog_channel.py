#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright (C) 2024 - 2024 张松贵, Inc. All Rights Reserved
# 模拟量通道类
# @FileName  :analog_channel.py
# @Time      :2024/07/05 13:52:31
# @Author    :张松贵

class AnalogChannel:
    """
    模拟量通道类

    """

    def __init__(self, an: int, chid: str, ph: str, ccbm: str, uu: str, a: float, b: float, skew: float, min_val: float,
                 max_val: float, primary: float = 0.0, secondary: float = 0.0, ps: str = "S", ratio: float = 0.0):
        """
        模拟量通道类
        :param an: 模拟通道索引号，必选，数字，整数
        :param chid: 通道标识符，必选，字符串，最大长度128个字符
        :param ph: 通道相别标识，可选，字母、数字，最小0个字符，最大长度2个字符
        :param ccbm: 被监视的电路元件，可选，字母、数字，最小0个字符，最大长度64个字符
        :param uu: 通道单位，如kV、V、kA、A RMS、 A Peak,必选，字母，最小长度1个
        :param a: 通道增益系数，必选，实数，数字，最小长度1个字符，最大长度32个字符，可以使用标准浮点标记法
        :param b: 通道偏移系数，必选，实数，数字，最小长度1个字符，最大长度32个字符，可以使用标准浮点标记法
        :param skew: 通道时滞（us），必选，实数，数字，最小长度1个字符，最大长度32个字符，可以使用标准浮点标记法
        :param min_val: 通道最小值，必选，实数，数字，最小长度1个字符，最大长度32个字符，可以使用标准浮点标记法
        :param max_val: 通道最大值，必选，实数，数字，最小长度1个字符，最大长度32个字符，可以使用标准浮点标记法
        :param primary: 通道互感器变比一次系数，必选，实数，数字，最小长度1个字符，最大长度32个字符
        :param secondary: 通道互感器变比二次系数，必选，实数，数字，最小长度1个字符，最大长度32个字符
        :param ps: 一次还是二次值标识,表明通道转换因子方程ax+b得到的值
        :param ratio: 通道变比，必选，实数，数字，最小长度1个字符，最大长度32个字符
        """
        self.clear()
        self.__an = an
        self.__chid = chid
        self.__ph = ph
        self.__ccbm = ccbm
        self.__uu = uu
        self.__a = a
        self.__b = b
        self.__skew = skew
        self.__min = min_val
        self.__max = max_val
        self.__primary = primary
        self.__secondary = secondary
        self.__ps = ps
        self.__ratio = ratio

    def clear(self):
        self.__an = 0
        self.__chid = ''
        self.__ph = ''
        self.__ccbm = ''
        self.__uu = ''
        self.__a = 0.0
        self.__b = 0.0
        self.__skew = 0.0
        self.__min = 0.0
        self.__max = 0.0
        self.__primary = 0.0
        self.__secondary = 0.0
        self.__ps = ''
        self.__ratio = 0.0

    def to_string(self):
        """从对象生成字符串"""
        parts = [str(self.__an), self.__chid, self.__ph, self.__ccbm, self.__uu,
                 str(self.__a), str(self.__b), str(self.__skew), str(self.__min),
                 str(self.__max), str(self.__primary), str(self.__secondary), self.__ps]
        # 移除末尾的空字符串以保持与原始解析逻辑一致
        while parts and not parts[-1]:
            parts.pop()
        return ','.join(parts)

    @property
    def an(self):
        """
        模拟通道索引号，必选，数字，整数
        """
        return self.__an

    @an.setter
    def an(self, value):
        """
        设置模拟通道索引号，数字、整数，最小长度1个字符，最大长度6个字符
        不要求前导零或空格，从1开始顺序计数到模拟通道总数A
        """
        self.__an = value

    @property
    def chid(self):
        """
        通道标识符，必选，字符串，最大长度128个字符
        """
        return self.__chid

    @chid.setter
    def chid(self, value):
        """
        通道标识符，必选，字符串，最大长度128个字符
        """
        self.__chid = value

    @property
    def ph(self):
        """
        通道相别标识，可选，字母、数字，最小0个字符，最大长度2个字符
        """
        return self.__ph

    @ph.setter
    def ph(self, value):
        """
        通道相别标识符
        """
        self.__ph = value

    @property
    def ccbm(self):
        """
        被监视的电路元件，可选，字母、数字，最小0个字符，最大长度64个字符
        """
        return self.__ccbm

    @ccbm.setter
    def ccbm(self, value):
        """
        设置被监视的电路元件，可选，字母、数字，最小0个字符，最大长度64个字符
        """
        self.__ccbm = value

    @property
    def uu(self):
        """
        通道单位，如kV、V、kA、A RMS、 A Peak,必选，字母，最小长度1个字符，最大32个字符
        """
        return self.__uu

    @uu.setter
    def uu(self, value):
        """
        设置通道单位，如kV、V、kA、A RMS、 A Peak,必选，字母，最小长度1个字符，最大32个字符
        none 表示无量纲值的单位
        """
        self.__uu = value

    @property
    def a(self):
        """
        通道增益系数，必选，实数，数字，最小长度1个字符，最大长度32个字符，可以使用标准浮点标记法
        """
        return self.__a

    @a.setter
    def a(self, value):
        """
        设置通道增益系数，必选，实数，数字，最小长度1个字符，最大长度32个字符，可以使用标准浮点标记法
        """
        self.__a = value

    @property
    def b(self):
        """
        通道偏移系数，必选，实数，数字，最小长度1个字符，最大长度32个字符，可以使用标准浮点标记法
        """
        return self.__b

    @b.setter
    def b(self, value):
        """
        设置通道偏移系数，必选，实数，数字，最小长度1个字符，最大长度32个字符，可以使用标准浮点标记法
        """
        self.__b = value

    @property
    def skew(self):
        """
        从采样时刻开始的通道时滞（us），必选，实数，数字，最小长度1个字符，最大长度32个字符，可以使用标准浮点标记法
        各通道采样时差信息，单位为微秒，必须为正数，不能超过采样周期
        """
        return self.__skew

    @skew.setter
    def skew(self, value):
        """
        设置从采样时刻开始的通道时滞（us），必选，实数，数字，最小长度1个字符，最大长度32个字符，可以使用标准浮点标记法
        各通道采样时差信息，单位为微秒，必须为正数
        """
        self.__skew = value

    @property
    def min(self):
        """
        该通道数字范围的最小值，必选、数字（整数或实数），最小长度1个字符，最大长度13个字符
        """
        return self.__min

    @min.setter
    def min(self, value):
        """
        设置该通道数字范围的最小值，必选、数字（整数或实数），最小长度1个字符，最大长度13个字符
        """
        self.__min = value

    @property
    def max(self):
        """
        该通道数字范围的最大值，必选、数字（整数或实数），最小长度1个字符，最大长度13个字符
        """
        return self.__max

    @max.setter
    def max(self, value):
        """
        通道数字范围的最大值，必选、数字（整数或实数），最小长度1个字符，最大长度13个字符
        """
        self.__max = value

    @property
    def primary(self):
        """
        通道互感器变比一次系数，必选，实数，数字，最小长度1个字符，最大长度32个字符
        """
        return self.__primary

    @primary.setter
    def primary(self, value):
        """
        设置通道互感器变比一次系数，必选，实数，数字，最小长度1个字符，最大长度32个字符
        """
        self.__primary = value

    @property
    def secondary(self):
        """
        通道互感器变比二次系数，必选，实数，数字，最小长度1个字符，最大长度32个字符
        """
        return self.__secondary

    @secondary.setter
    def secondary(self, value):
        """
        设置通道互感器变比二次系数，必选，实数，数字，最小长度1个字符，最大长度32个字符
        """
        if value != 0:
            self.__secondary = value
        else:
            raise Exception("二次值不能为0")

    @property
    def ps(self):
        """表明通道转换因子方程ax+b得到的值还原为一次还是二次值标识"""
        return self.__ps

    @ps.setter
    def ps(self, value):
        """
        设置通道转换因子方程ax+b得到的值还原为一次还是二次值标识
        """
        self.__ps = value

    @property
    def ratio(self):
        """
        通道互感器变比系数，必选，实数，数字，最小长度1个字符，最大长度32个字符
        """
        self.ratio = self.primary / self.secondary
        return self.__ratio

    @ratio.setter
    def ratio(self, value):
        """
        设置通道互感器变比系数，必选，实数，数字，最小长度1个字符，最大长度32个字符
        """
        self.__ratio = value
