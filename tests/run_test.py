#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import unittest

# 将项目根目录添加到Python路径中
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from test_computation.test_calcius import TestCalcius
# 导入各个测试模块
from test_reader.test_analog_parser import TestAnalogParser
from test_reader.test_comtrade_reader import TestComtrade
from test_reader.test_config_reader import TestConfigReader
from test_reader.test_dat_reader import TestDataReader
from test_reader.test_digital_parser import TestDigitalParser
from test_reader.test_header_parser import TestHeaderParser
from utils.test_channel_dispose import TestChannelDispose


def create_test_suite():
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()

    # 添加测试用例
    suite.addTest(loader.loadTestsFromTestCase(TestAnalogParser))
    suite.addTest(loader.loadTestsFromTestCase(TestDigitalParser))
    suite.addTest(loader.loadTestsFromTestCase(TestHeaderParser))
    suite.addTest(loader.loadTestsFromTestCase(TestConfigReader))
    suite.addTest(loader.loadTestsFromTestCase(TestDataReader))
    suite.addTest(loader.loadTestsFromTestCase(TestComtrade))
    suite.addTest(loader.loadTestsFromTestCase(TestChannelDispose))
    suite.addTest(loader.loadTestsFromTestCase(TestCalcius))

    return suite


def run_test_suite():
    suite = create_test_suite()
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    # 输出详细测试报告
    print("\n" + "=" * 60)
    print("详细测试报告")
    print("=" * 60)
    print(f"总测试数: {result.testsRun}")
    print(f"失败数: {len(result.failures)}")
    print(f"错误数: {len(result.errors)}")
    print(
        f"成功率: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.2f}%" if result.testsRun > 0 else "0%")
    print(f"测试时间: {result.testsRun} 个测试已运行")

    # 输出失败详情
    if result.failures:
        print("\n失败的测试:")
        print("-" * 40)
        for i, (test, traceback) in enumerate(result.failures, 1):
            print(f"{i}. {test}")
            print(f"   Traceback:\n{traceback}")
            print()

    # 输出错误详情
    if result.errors:
        print("错误的测试:")
        print("-" * 40)
        for i, (test, traceback) in enumerate(result.errors, 1):
            print(f"{i}. {test}")
            print(f"   Traceback:\n{traceback}")
            print()

    # 输出成功信息
    successful_tests = result.testsRun - len(result.failures) - len(result.errors)
    print(f"成功执行: {successful_tests}/{result.testsRun} 个测试")
    print("=" * 60)
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_test_suite()
    exit(0 if success else 1)
