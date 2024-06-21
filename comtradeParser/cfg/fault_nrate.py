#!/usr/bin/env python
# -*- coding: utf-8 -*-


class FaultNrate:
    def __init__(self, samp: int, end_point: int, cycle_sample_num: int = None, sample_num: int = None,
                 start_point: int = None, waste_time: int = None, end_time: int = None):
        self.clear()
        self._samp = samp
        self._end_point = end_point
        self._cycle_sample_num = cycle_sample_num
        self._sample_num = sample_num
        self._start_point = start_point
        self._waste_time = waste_time
        self._end_time = end_time

    def clear(self):
        self._samp = 0
        self._end_point = 0
        self._cycle_sample_num = 0
        self._sample_num = 0
        self._start_point = 0
        self._waste_time = 0
        self._end_time = 0

    def to_string(self):
        return f'{str(self._samp)},{str(self._end_point)}\n'

    @property
    def samp(self):
        return self._samp

    @samp.setter
    def samp(self, value):
        self._samp = value

    @property
    def end_point(self):
        return self._end_point

    @end_point.setter
    def end_point(self, value):
        self._end_point = value

    @property
    def cycle_sample_num(self):
        return self._cycle_sample_num

    @cycle_sample_num.setter
    def cycle_sample_num(self, value):
        self._cycle_sample_num = value

    @property
    def sample_num(self):
        return self._sample_num

    @sample_num.setter
    def sample_num(self, value):
        self._sample_num = value

    @property
    def start_point(self):
        return self._start_point

    @start_point.setter
    def start_point(self, value):
        self._start_point = value

    @property
    def waste_time(self):
        return self._waste_time

    @waste_time.setter
    def waste_time(self, value):
        self._waste_time = value

    @property
    def end_time(self):
        return self._end_time

    @end_time.setter
    def end_time(self, value):
        self._end_time = value


def parse_nrate(nrate_str):
    nrate_info = nrate_str.split(',')
    return FaultNrate(samp=int(nrate_info[0]),
                      end_point=int(nrate_info[1].rstrip()))


def generate_nrate_str(nrate_obj):
    """
    直接使用对象的方法生成字符串
    """
    return nrate_obj.to_string()
