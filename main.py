#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

from py3comtrade.reader.comtrade_reader import comtrade_reader

if __name__ == "__main__":
    # file_path = r'D:\codeArea\gitee\comtradeOfPython\tests\data\xtz.cfg'
    file_path = r"C:\Users\sddl\Desktop\7次电铁线录波文件\20200803_220kV仁铁Ⅰ线(仁和站-高密牵引站)动作报告\仁和站\本侧故障录波器\32353_65318_comtrade.cfg"

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
    print(f"文件解析耗时{end_time - start_time}")
    json = cr.model_dump()
    # cr.save_json("test.json")
    # cr.save_comtrade("test.cfg", data_file_type=DataFileType.BINARY)
    # raw_all = cr.get_channel_raw_data_range()
    # digital_change = cr.get_digital_change()
    print(cr.header.station_name)
