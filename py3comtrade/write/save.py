#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

import pandas as pd

from py3comtrade.model.comtrade import Comtrade
from py3comtrade.model.type.base_enum import CustomEncoder
from py3comtrade.model.type.ret_enum import Ret
from py3comtrade.write.result import Result


def to_json(file_path: str, _wave: Comtrade) -> Result:
    """
    将comtrade对象保存为json文件
    参数:
        file_path(str):保存文件路径
        _wave(Comtrade):comtrade对象
    """
    comtrade_json = _wave.model_dump_json()
    try:
        with open(file_path, 'w', encoding='utf8') as f:
            json.dump(comtrade_json, f, ensure_ascii=False, indent=2, cls=CustomEncoder)
        return Result(message=f"{file_path}文件写入成功")
    except Exception as e:
        return Result(code=Ret.ERROR, message=f"{file_path}文件写入失败")


def to_csv(file_path: str,
           _wave: Comtrade,
           samp_point_num_title: bool = True,
           sample_time_title: bool = True) -> Result:
    """
    将comtrade对象保存为csv文件
    参数:
        file_path(str):保存文件路径
        _wave(Comtrade):comtrade对象
        samp_point_num_title(bool):是否添加采样点序号行,默认为添加
        sample_time_title(bool):是否添加采样时间行,默认为添加
    返回值:
    """
    try:
        with open(file_path, "w", encoding="gbk") as f:
            if samp_point_num_title:
                f.write(f'采样点号,{",".join(map(str, _wave.sample_point))}\n')
            if sample_time_title:
                f.write(f'采样时间,{",".join(map(str, _wave.sample_time))}\n')
            for analog in _wave.analogs:
                if analog.values is not None:
                    f.write(f'{analog.name},{",".join(map(str, analog.values))}\n')
            for digital in _wave.digitals:
                if digital.values is not None:
                    f.write(f'{digital.name},{",".join(map(str, digital.values))}\n')
        return Result(message=f"{file_path}文件写入成功")
    except Exception:
        return Result(code=Ret.ERROR, message=f"{file_path}文件写入失败")


def to_excel(file_path: str,
             _wave: Comtrade,
             samp_point_num_title: bool = True,
             sample_time_title: bool = True) -> Result:
    """
    将comtrade对象保存为Excel文件
    参数:
        file_path(str):保存文件路径
        _wave(Comtrade):comtrade对象
        samp_point_num_title(bool):是否添加采样点序号行,默认为添加
        sample_time_title(bool):是否添加采样时间行,默认为添加
    返回值:
        Result:操作结果
    """
    try:
        # 创建DataFrame
        data_dict = {}

        # 添加采样点号
        if samp_point_num_title:
            data_dict['采样点号'] = _wave.sample_point

        # 添加采样时间
        if sample_time_title:
            data_dict['采样时间'] = _wave.sample_time

        # 添加模拟量通道数据
        for analog in _wave.analogs:
            if analog.values is not None:
                data_dict[analog.name] = analog.values

        # 添加开关量通道数据
        for digital in _wave.digitals:
            if digital.values is not None:
                data_dict[digital.name] = digital.values

        # 创建DataFrame并保存为Excel
        df = pd.DataFrame(data_dict)
        df.to_excel(file_path, index=False)

        return Result(message=f"{file_path}文件写入成功")
    except Exception as e:
        return Result(code=Ret.ERROR, message=f"{file_path}文件写入失败: {str(e)}")
