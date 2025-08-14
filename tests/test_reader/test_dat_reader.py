#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest

from py3comtrade.reader.config_reader import config_reader
from py3comtrade.reader.data_reader import data_reader


class TestDataReader(unittest.TestCase):

    def setUp(self):
        cfg_name = r'../data/xtz.cfg'
        dat_name = r'../data/xtz.dat'
        self.cfg = config_reader(cfg_name)
        self.dat = data_reader(dat_name, self.cfg.sample)

    def test_read_file(self):
        pass
