#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest

from py3comtrade.model.type.analog_enum import PsType
from py3comtrade.model.type.types import ValueType
from py3comtrade.reader.comtrade_reader import comtrade_reader


class TestComtradeFilter(unittest.TestCase):
    """测试Comtrade类的链式调用筛选功能"""

    def setUp(self):
        """设置测试环境，读取测试数据文件"""
        # 使用测试数据目录中的文件
        test_data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        # 使用hjz.cfg作为测试文件
        self.test_file_path = os.path.join(test_data_dir, 'hjz')

        # 读取测试数据
        self.comtrade = comtrade_reader(self.test_file_path)

        # 保存原始通道数量，用于后续验证
        self.original_analog_count = len(self.comtrade.analogs)
        self.original_digital_count = len(self.comtrade.digitals)

    def test_filter_by_channel_type_analog_only(self):
        """测试仅保留模拟通道"""
        # 测试analog_only方法
        filtered = self.comtrade.filter(analog_only=True)

        # 验证过滤后对象不影响原对象
        self.assertEqual(len(self.comtrade.analogs), self.original_analog_count)
        self.assertEqual(len(self.comtrade.digitals), self.original_digital_count)

        # 验证过滤后只有模拟通道
        self.assertEqual(len(filtered.analogs), self.original_analog_count)
        self.assertEqual(len(filtered.digitals), 0)

        # 测试链式调用filter_by_channel_type方法
        filtered2 = self.comtrade.filter_by_channel_type('analog')
        self.assertEqual(len(filtered2.analogs), self.original_analog_count)
        self.assertEqual(len(filtered2.digitals), 0)

    def test_filter_by_channel_type_digital_only(self):
        """测试仅保留开关量通道"""
        # 测试digital_only方法
        filtered = self.comtrade.filter(digital_only=True)

        # 验证过滤后对象不影响原对象
        self.assertEqual(len(self.comtrade.analogs), self.original_analog_count)
        self.assertEqual(len(self.comtrade.digitals), self.original_digital_count)

        # 验证过滤后只有开关量通道
        self.assertEqual(len(filtered.analogs), 0)
        self.assertEqual(len(filtered.digitals), self.original_digital_count)

        # 测试链式调用filter_by_channel_type方法
        filtered2 = self.comtrade.filter_by_channel_type('digital')
        self.assertEqual(len(filtered2.analogs), 0)
        self.assertEqual(len(filtered2.digitals), self.original_digital_count)

    def test_filter_by_index(self):
        """测试根据索引筛选通道"""
        # 测试单个索引和多个索引
        single_index = 0
        multi_index = [0, 1, 2]

        # 筛选模拟通道
        filtered_analog = self.comtrade.filter(analog_index=multi_index)
        self.assertEqual(len(filtered_analog.analogs), len(multi_index))
        self.assertEqual(len(filtered_analog.digitals), self.original_digital_count)

        # 筛选开关量通道
        if self.original_digital_count > 0:
            filtered_digital = self.comtrade.filter(digital_index=single_index)
            self.assertEqual(len(filtered_digital.analogs), self.original_analog_count)
            self.assertEqual(len(filtered_digital.digitals), 1)

        # 测试链式调用filter_by_index方法
        filtered_both = self.comtrade.filter_by_index(analog_index=multi_index[:2], digital_index=single_index)
        self.assertEqual(len(filtered_both.analogs), 2)
        self.assertEqual(len(filtered_both.digitals), 1 if self.original_digital_count > 0 else 0)

        # 验证索引被重新设置
        for i, analog in enumerate(filtered_analog.analogs):
            self.assertEqual(analog.index, i)

    def test_filter_by_cfgan(self):
        """测试根据cfgan筛选通道"""
        # 获取前几个通道的cfgan值
        if self.original_analog_count >= 3:
            cfgan_values = [analog.idx_cfg for analog in self.comtrade.analogs[:3]]

            # 测试cfgan筛选
            filtered = self.comtrade.filter(analog_cfgan=cfgan_values)
            self.assertEqual(len(filtered.analogs), 3)

            # 测试链式调用filter_by_cfgan方法
            filtered2 = self.comtrade.filter_by_cfgan(analog_cfgan=cfgan_values[:2])
            self.assertEqual(len(filtered2.analogs), 2)

    def test_filter_by_selected(self):
        """测试根据选中状态筛选通道"""
        # 先设置一些通道为选中状态
        for analog in self.comtrade.analogs[:3]:
            analog.selected = True
        for digital in self.comtrade.digitals[:2]:
            digital.selected = True

        # 筛选选中的通道
        filtered_selected = self.comtrade.filter(is_selected=True)
        self.assertEqual(len(filtered_selected.analogs), 3)
        self.assertEqual(len(filtered_selected.digitals), 2)

        # 筛选未选中的通道
        filtered_not_selected = self.comtrade.filter(is_selected=False)
        self.assertEqual(len(filtered_not_selected.analogs), self.original_analog_count - 3)
        self.assertEqual(len(filtered_not_selected.digitals), self.original_digital_count - 2)

        # 测试链式调用filter_by_selected方法
        filtered_method = self.comtrade.filter_by_selected(True)
        self.assertEqual(len(filtered_method.analogs), 3)
        self.assertEqual(len(filtered_method.digitals), 2)

    def test_values_type_conversion(self):
        """测试采样值类型转换"""
        # 测试raw类型转换
        filtered_raw = self.comtrade.filter(target_value_type='raw')
        self.assertEqual(filtered_raw.sample.value_type, ValueType.RAW)

        # 测试instant类型转换
        filtered_instant = self.comtrade.filter(target_value_type='instant')
        self.assertEqual(filtered_instant.sample.value_type, ValueType.INSTANT)

        # 测试链式调用values_type方法
        filtered_method = self.comtrade.values_type('raw')
        self.assertEqual(filtered_method.sample.value_type, ValueType.RAW)

    def test_values_ps_conversion(self):
        """测试一二次值转换"""
        # 确保有模拟通道用于测试
        if self.original_analog_count > 0:
            # 测试p(一次值)转换
            filtered_p = self.comtrade.filter(target_ps='p')
            for analog in filtered_p.analogs:
                self.assertEqual(analog.ps, PsType.P)

            # 测试s(二次值)转换
            filtered_s = self.comtrade.filter(target_ps='s')
            for analog in filtered_s.analogs:
                self.assertEqual(analog.ps, PsType.S)

            # 测试链式调用values_ps方法
            filtered_method = self.comtrade.values_ps('p')
            for analog in filtered_method.analogs:
                self.assertEqual(analog.ps, PsType.P)

    def test_slice_by_samp_point(self):
        """测试根据采样点切片"""
        # 确保有通道值用于测试
        if self.original_analog_count > 0 and len(self.comtrade.analogs[0].values) > 10:
            start_point, end_point = 5, 15

            # 测试采样点切片
            filtered = self.comtrade.filter(start_point=start_point, end_point=end_point)

            # 验证所有通道的采样值都被正确切片
            for analog in filtered.analogs:
                self.assertEqual(len(analog.values), end_point - start_point)
            for digital in filtered.digitals:
                self.assertEqual(len(digital.values), end_point - start_point)

            # 测试链式调用slice_by_samp_point方法
            filtered_method = self.comtrade.slice_by_samp_point(start_point, end_point)
            for analog in filtered_method.analogs:
                self.assertEqual(len(analog.values), end_point - start_point)

    def test_slice_by_segment(self):
        """测试根据采样段切片"""
        # 测试第0段采样
        filtered = self.comtrade.filter(segment=0)

        # 测试链式调用slice_by_segment方法
        filtered_method = self.comtrade.slice_by_segment(0)

        # 验证结果不为空
        if self.original_analog_count > 0:
            self.assertTrue(hasattr(filtered.analogs[0], 'values'))
            self.assertTrue(hasattr(filtered_method.analogs[0], 'values'))

    def test_clear_channel_values(self):
        """测试清除通道值"""
        # 测试清除通道值
        filtered = self.comtrade.filter(clear_channel_values=True)

        # 验证所有通道值都被清除
        for analog in filtered.analogs:
            self.assertEqual(len(analog.values), 0)
        for digital in filtered.digitals:
            self.assertEqual(len(digital.values), 0)

        # 测试链式调用clear_channel_values方法
        filtered_method = self.comtrade.clear_channel_values()
        for analog in filtered_method.analogs:
            self.assertEqual(len(analog.values), 0)
        for digital in filtered_method.digitals:
            self.assertEqual(len(digital.values), 0)

    def test_chained_filters(self):
        """测试链式组合筛选"""
        # 测试复杂的链式调用组合
        filtered = self.comtrade.filter(
            analog_only=True,
            analog_index=[0, 1, 2],
            target_value_type='raw',
            target_ps='p'
        )

        # 验证结果
        self.assertEqual(len(filtered.analogs), 3)
        self.assertEqual(len(filtered.digitals), 0)
        self.assertEqual(filtered.sample.value_type, ValueType.RAW)
        for analog in filtered.analogs:
            self.assertEqual(analog.ps, PsType.P)
            self.assertEqual(analog.index, filtered.analogs.index(analog))  # 索引被重新设置


if __name__ == '__main__':
    unittest.main()
