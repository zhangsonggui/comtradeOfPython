#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

from py3comtrade.computation.calcium import Calcium
from py3comtrade.reader.comtrade_reader import comtrade_reader

if __name__ == "__main__":
    file_path = r'D:\codeArea\gitee\comtradeOfPython\tests\data\xtz.cfg'
    start_time = time.time()
    cr = comtrade_reader(file_path)
    # for analog in cr.analogs:
    #     if analog.is_enable():
    #         print(f"{analog.name}:\t是否启用:{analog.is_enable()},是否电流:{analog.channel_flag()}")
    # for digital in cr.digitals:
    #     if digital.is_change():
    #         print(f"{digital.name}:\t是否启用:{digital.is_enable()},是否变位:{digital.is_change()}")
    end_time = time.time()
    zrt = cr.get_zero_point()
    print(f"文件解析耗时{(end_time - start_time) * 1000}毫秒")
    wave = cr.save_comtrade("test.cfg",compress=True)
    # cr.save_json("test.json")
    # cr.save_comtrade("test.cfg", data_file_type=DataFileType.BINARY)
    # raw_all = cr.get_channel_raw_data_range()
    # digital_change = cr.get_digital_change()
    # start_point, end_point, _ = cr.get_cursor_sample_range(0, cycle_num=1)
    # sszs = cr.get_channel_instant_data_range(start_point=start_point, end_point=end_point)
    # print(
    #     f"通道名称\t\t向量值\t\t有效值\t\t角度\t\t直流分量\t\t二次谐波\t\t三次谐波\t\t五次谐波\t\t七次谐波\t\t九次谐波\t\t用时")
    wave_start_time = time.time()
    # for ssz in sszs:
    #     if ssz.is_enable():
    #         calc_start_time = time.time()
    #         cal = Calcium(instant=ssz.values)
    #         cal.calc_harmonics()
    #         calc_end_time = time.time()
    #         print(
    #             f"{ssz.name}\t\t{cal.vector}\t\t{cal.effective}\t\t{cal.angle}\t\t{cal.dc_component}\t\t{cal.harmonics.get(2).amplitude}\t\t{cal.harmonics.get(3).amplitude}\t\t{cal.harmonics.get(5).amplitude}\t\t{cal.harmonics.get(7).amplitude}\t\t{cal.harmonics.get(9).amplitude}\t\t{(calc_end_time - calc_start_time) * 1000}ms")
    wave_end_time = time.time()
    print(f"数值计算用时{(wave_end_time - wave_start_time) * 1000}毫秒")
