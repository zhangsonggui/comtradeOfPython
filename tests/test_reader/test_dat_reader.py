#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest

from py3comtrade.reader.config_reader import config_reader
from py3comtrade.reader.data_reader import DataReader


class TestDataReader(unittest.TestCase):

    def setUp(self):
        cfg_name = r'../data/xtz.cfg'
        dat_name = r'../data/xtz.dat'
        self.cfg = config_reader(cfg_name)
        self.dat = DataReader(file_path=dat_name, sample=self.cfg.sample)

    def test_read_file(self):
        pass
