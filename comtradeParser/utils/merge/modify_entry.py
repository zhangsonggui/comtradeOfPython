#!/usr/bin/env python
# -*- coding: utf-8 -*-
from comtradeParser.cfg.analog_channel import AnalogChannel
from comtradeParser.cfg.digital_channel import DigitalChannel


class ModifyEntry:

    def __init__(self, analog_channels: [AnalogChannel], digital_channels: [DigitalChannel]):
        self.analog_channels = analog_channels
        self.digital_channels = digital_channels

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
