#!/usr/bin/env python
# -*- coding: utf-8 -*-
from comtradeParser.cfg.fault_nrate import FaultNrate, parse_nrate, generate_nrate_str
from comtradeParser.cfg.fault_time import FaultTime, parse_fault_time, generate_fault_time_str


class SampleInfo:
    """
    故障采样信息类
    """

    def __init__(self, lf: int, nrate_num: int, sample_total_num: int, ft: str, timemult: float, nrates: list,
                 fault_time: FaultTime, bit_width: int, analog_bytes: int = 0, digital_bytes: int = 0,
                 total_bytes: int = 0):
        self._lf = lf
        self._nrate_num = nrate_num
        self._sample_total_num = sample_total_num
        self._ft = ft
        self._timemult = timemult
        self._nrates = nrates
        self._fault_time = fault_time
        self._bit_width = bit_width
        self._analog_bytes = analog_bytes
        self._digital_bytes = digital_bytes
        self._total_bytes = total_bytes

    def clear(self) -> None:
        self._lf = 0
        self._nrate_num = 0
        self._sample_total_num = 0
        self._ft = ''
        self._timemult = 1.0
        self._nrates = []
        self._fault_time = None
        self._bit_width = 2
        self._analog_bytes = 0
        self._digital_bytes = 0
        self._total_bytes = 0

    @property
    def lf(self):
        """
        获取系统频率
        """
        return self._lf

    @lf.setter
    def lf(self, value):
        """
        修改系统频率
        """
        self._lf = value

    @property
    def nrate_num(self):
        """
        获取采样段数量
        """
        return self._nrate_num

    @nrate_num.setter
    def nrate_num(self, value):
        """
        修改采样段数量
        """
        self._nrate_num = value

    @property
    def sample_total_num(self):
        """
        获取采样点总数
        """
        return self._sample_total_num

    @sample_total_num.setter
    def sample_total_num(self, value):
        """
        修改采样点总数
        """
        self._sample_total_num = value

    @property
    def ft(self):
        """
        获取采样格式
        """
        return self._ft

    @ft.setter
    def ft(self, value):
        """
        修改采样格式
        """
        self._ft = value

    @property
    def timemult(self):
        """
        获取采样时间因子
        """
        return self._timemult

    @timemult.setter
    def timemult(self, value):
        """
        修改采样时间因子
        """
        self._timemult = value

    @property
    def nrates(self):
        """
        获取各采样段采样信息
        """
        return self._nrates

    @nrates.setter
    def nrates(self, value):
        """
        修改各采样段采样信息
        """
        self._nrates = value

    @property
    def fault_time(self):
        """
        获取故障时间信息
        """
        return self._fault_time

    @fault_time.setter
    def fault_time(self, value):
        """
        修改故障时间信息
        """
        self._fault_time = value

    @property
    def bit_width(self):
        """
        获取采样格式
        """
        return self._bit_width

    @bit_width.setter
    def bit_width(self, value):
        """
        修改采样格式
        """
        self._bit_width = value

    @property
    def analog_bytes(self):
        """
        获取采样格式
        """
        return self._analog_bytes

    @analog_bytes.setter
    def analog_bytes(self, value):
        """
        修改采样格式
        """
        self._analog_bytes = value

    @property
    def digital_bytes(self):
        """
        获取采样格式
        """
        return self._digital_bytes

    @digital_bytes.setter
    def digital_bytes(self, value):
        """
        修改采样格式
        """
        self._digital_bytes = value

    @property
    def total_bytes(self):
        """
        获取采样格式
        """
        ad = self.analog_bytes + self.digital_bytes * 2
        if self._total_bytes != ad:
            return ad + 8
        return self._total_bytes

    @total_bytes.setter
    def total_bytes(self, value):
        """
        修改采样格式
        """
        self._total_bytes = value

    def nrates_to_string(self):
        """
        修改各采样段采样信息
        """
        nrate_str = ''
        for nrate in self._nrates:
            nrate_str = generate_nrate_str(nrate) + '\n'
        return nrate_str

    def fault_time_to_string(self):
        """故障时间信息转字符串"""
        return generate_fault_time_str(self._fault_time)

    def to_string(self) -> str:
        """对象转字符串"""
        nrates_str = self.nrates_to_string()
        fault_time_str = self.fault_time_to_string()
        return f'{self.lf}\n{self.nrate_num}\n{nrates_str}{fault_time_str}\n{self.ft}\n{str(self.timemult)}'


def parse_sample_info(sample_infos):
    """从字符串解析成对象"""
    lf = int(sample_infos[0].rstrip())
    nrate_num = int(sample_infos[1].rstrip())

    nrates = []  # 各采样段的采样率原始信息
    # 循环实例化各采样段的采样率信息
    for i in range(2, nrate_num + 2):
        nrates.append(parse_nrate(sample_infos[i].rstrip()))

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
    fault_time = None
    ft = ''
    timemult = 1.0
    # 实例化故障时间和采样格式
    if len(sample_infos) >= nrate_num + 4:
        fault_time = parse_fault_time(sample_infos[nrate_num + 2:nrate_num + 4])
        ft = sample_infos[nrate_num + 4].strip('\n').upper()
    bit_width = 2
    if ft in ['BINARY32', 'FLOAT32']:
        bit_width = 4
    if len(sample_infos) >= nrate_num + 5:
        timemult = parse_timemult(sample_infos[nrate_num + 4])

    return SampleInfo(lf=lf, nrate_num=nrate_num, sample_total_num=sample_total_num, ft=ft, timemult=timemult,
                      nrates=nrates, fault_time=fault_time, bit_width=bit_width)


def parse_timemult(timemult_str):
    """从字符串解析成对象"""
    try:
        timemult = float(timemult_str.strip('\n'))
    except ValueError:
        timemult = 1.0
    return timemult


def generate_sample_info_str(sample_info_obj):
    """
    直接使用对象的方法生成字符串
    """
    return sample_info_obj.to_string()
