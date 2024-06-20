#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime

time_format = '%d/%m/%Y,%H:%M:%S.%f'  # 时间格式字符串


class FaultTime:
    def __init__(self, start_time: datetime, trigger_time: datetime, zero_time: int):
        self.clear()
        self._start_time = start_time
        self._trigger_time = trigger_time
        self._zero_time = zero_time

    def clear(self):
        self._start_time = None
        self._trigger_time = None
        self._zero_time = 0

    @property
    def start_time(self):
        return self._start_time

    @property
    def trigger_time(self):
        return self._trigger_time

    @property
    def zero_time(self):
        return self._zero_time

    def to_string(self):
        return f"{self._start_time.strftime(time_format)}\n{self._trigger_time.strftime(time_format)}"


def parse_fault_time(fault_time_strs):
    try:
        str_time = fault_time_strs[0].strip()
        start_time = datetime.strptime(str_time, time_format)
        str_time = fault_time_strs[1].strip()
        trigger_time = datetime.strptime(str_time, time_format)
    except ValueError as e:
        raise ValueError(f"时间格式错误:{e}")
    zero_time = (trigger_time - start_time).microseconds
    return FaultTime(start_time=start_time,
                     trigger_time=trigger_time,
                     zero_time=zero_time)


def generate_fault_time_str(fault_time_obj):
    return fault_time_obj.to_string()
