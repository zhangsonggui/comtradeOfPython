#!/usr/bin/env python
# -*- coding: utf-8 -*-

class FaultHeader:

    def __init__(self, station_name: str = '变电站', rec_dev_id: str = '录波设备', rev_year: int = 1999,
                 channel_total_num: int = 0, analog_channel_num: int = 0, digital_channel_num: int = 0):
        self._station_name = station_name
        self._rec_dev_id = rec_dev_id
        self._rev_year = rev_year
        self._analog_channel_num = analog_channel_num
        self._digital_channel_num = digital_channel_num
        if channel_total_num != analog_channel_num + digital_channel_num:
            self._channel_total_num = analog_channel_num + digital_channel_num
        self._channel_total_num = channel_total_num

    def clear(self):
        self._station_name = ''
        self._rec_dev_id = ''
        self._rev_year = 1991
        self._channel_total_num = 0
        self._analog_channel_num = 0
        self._digital_channel_num = 0

    @property
    def station_name(self):
        """
        变电站名称
        """
        return self._station_name

    @station_name.setter
    def station_name(self, value):
        """
        修改变电站名称
        """
        self._station_name = value

    @property
    def rec_dev_id(self):
        """
        采集设备ID
        """
        return self._rec_dev_id

    @rec_dev_id.setter
    def rec_dev_id(self, value):
        """
        修改采集设备ID
        """
        self._rec_dev_id = value

    @property
    def rev_year(self):
        """
        版本信息
        """
        return self._rev_year

    @rev_year.setter
    def rev_year(self, value):
        """
        修改版本信息
        """
        self._rev_year = value

    @property
    def channel_total_num(self):
        """
        通道总数
        """
        return self._channel_total_num

    @channel_total_num.setter
    def channel_total_num(self, value):
        """
        修改通道总数
        """
        self._channel_total_num = value

    @property
    def analog_channel_num(self):
        """
        模拟通道数
        """
        return self._analog_channel_num

    @analog_channel_num.setter
    def analog_channel_num(self, value):
        """
        修改模拟通道数
        """
        self._analog_channel_num = value

    @property
    def digital_channel_num(self):
        """
        数字通道数
        """
        return self._digital_channel_num

    @digital_channel_num.setter
    def digital_channel_num(self, value):
        """
        修改数字通道数
        """
        self._digital_channel_num = value

    def to_string(self):
        """从对象生成字符串"""
        return (f'{self.station_name},{self.rec_dev_id},{str(self.rev_year)}\n' +
                f'{str(self.channel_total_num)},{str(self.analog_channel_num)}A,{str(self.digital_channel_num)}D')


def parse_header(header_str):
    fs = header_str[0].rstrip()
    fs = fs.split(',')
    nums = header_str[1].rstrip()
    nums = nums.split(',')
    station_name = fs[0]
    rec_dev_id = fs[1]
    rev_year = 1991
    if len(fs) > 2:
        rev_year = int(fs[2])
    channel_total_num = int(nums[0])
    analog_channel_num = int(nums[1].strip('A'))
    digital_channel_num = int(nums[2].strip('D'))
    return FaultHeader(station_name=station_name, rec_dev_id=rec_dev_id, channel_total_num=channel_total_num,
                       analog_channel_num=analog_channel_num, digital_channel_num=digital_channel_num,
                       rev_year=rev_year)


def generate_fault_header_str(fault_header_obj):
    """
    直接使用对象的方法生成字符串
    """
    return fault_header_obj.to_string()
