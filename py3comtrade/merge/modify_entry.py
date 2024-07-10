#!/usr/bin/env python
# -*- coding: utf-8 -*-
from py3comtrade.parser.analog_channel import AnalogChannel
from py3comtrade.parser.digital_channel import DigitalChannel
from py3comtrade.parser.fault_header import FaultHeader
from py3comtrade.parser.sample_info import SampleInfo


class ModifyEntry:
    # TODO: 修改参数实体，最多有哪些参数，哪些参数默认值，如果要修改，需要实例化该类，然后放入列表
    def __init__(self, fault_header: FaultHeader = None, analog_channels: [AnalogChannel] = None,
                 digital_channels: [DigitalChannel] = None, sample_info: SampleInfo = None):
        self._fault_header = fault_header
        self._analog_channels = analog_channels
        self._digital_channels = digital_channels
        self._sample_info = sample_info

    @property
    def fault_header(self):
        return self._fault_header

    @fault_header.setter
    def fault_header(self, value: FaultHeader):
        self._fault_header = value

    @property
    def analog_channels(self):
        return self._analog_channels

    @analog_channels.setter
    def analog_channels(self, value: [AnalogChannel]):
        self._analog_channels = value

    @property
    def digital_channels(self):
        return self._digital_channels

    @digital_channels.setter
    def digital_channels(self, value: [DigitalChannel]):
        self._digital_channels = value

    @property
    def sample_info(self):
        return self._sample_info

    @sample_info.setter
    def sample_info(self, value: SampleInfo):
        self._sample_info = value
