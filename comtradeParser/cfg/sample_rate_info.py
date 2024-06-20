#!/usr/bin/env python
# -*- coding: utf-8 -*-
from comtradeParser.cfg.fault_nrate import FaultNrate, parse_nrate


class SampleRateInfo:
    def __init__(self, lf: int, nrate_num: int, sample_total_num: int, nrates):
        """
        :param lf: 频率
        :param nrate_num: 采样段数量
        :param nrates: 各采样段的信息
        """
        self.clear()
        self._lf = lf
        self._nrate_num = nrate_num
        self._sample_total_num = sample_total_num
        self._nrates = nrates

    def clear(self):
        self._lf = 0
        self._nrate_num = 0
        self._sample_total_num = 0
        self._nrates = []

    @property
    def lf(self):
        return self._lf

    @property
    def nrate_num(self):
        return self._nrate_num

    @property
    def sample_total_num(self):
        return self._sample_total_num

    @sample_total_num.setter
    def sample_total_num(self, value):
        self._sample_total_num = value

    @property
    def nrates(self):
        return self._nrates

    @nrates.setter
    def nrates(self, value):
        self._nrates = value

    def sample_rate_to_string(self):
        return f'{str(self._lf)}\n{str(self._nrate_num)}'

    def nrates_to_string(self):
        """各采样段的采样率原始信息"""
        return ''.join([nrate.to_string() for nrate in self._nrates])


def parse_sample_rate_info(sample_rate_infos):
    """从字符串解析成对象"""
    lf = int(sample_rate_infos[0].rstrip())
    nrate_num = int(sample_rate_infos[1].rstrip())

    nrates = []  # 各采样段的采样率原始信息
    # 循环实例化各采样段的采样率信息
    for i in range(2, nrate_num + 2):
        nrates.append(parse_nrate(sample_rate_infos[i].rstrip()))

    # 计算各采样段采样率及采样点信息
    for i in range(0, nrate_num):
        nrate: FaultNrate = nrates[i]
        # 每个周波采多少个点数
        nrate.cycle_sample_num = int(nrate.samp / lf)
        # 每段包含多少个采样点数
        nrate.sample_num = nrate.end_point if i == 0 else nrate.end_point - nrates[i - 1].end_point
        # 每段开始的采样点号
        nrate.start_point = 0 if i == 0 else nrates[i - 1].end_point
        # 计算采样段一共用了多少时间
        nrate.waste_time = nrate.sample_num / nrate.cycle_sample_num * 20
        # 计算每个采样段结束是的时间
        nrate.end_time = nrate.waste_time if i == 0 else nrate.waste_time + nrates[i - 1].end_time
    sample_total_num = nrates[-1].end_point
    return SampleRateInfo(lf=lf, nrate_num=nrate_num, sample_total_num=sample_total_num, nrates=nrates)


def generate_sample_rate_info_str(sample_rate_obj):
    """直接使用对象的方法生成字符串"""
    return sample_rate_obj.sample_rate_to_string() + '\n' + sample_rate_obj.nrates_to_string()
