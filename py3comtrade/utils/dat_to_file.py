#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd


class DatToFile(object):
    dat = None

    def __init__(self, dat: np.ndarray):
        self.dat = dat


def write_dat_ascii(dat: np.ndarray, filename: str):
    """
    使用pandas保存文本文件的能力直接将numpy数组保存成csv格式
    :param dat: 数组对象
    :param filename: 保存的文件名，含目录、文件名和后缀
    :return:
    """
    df = pd.DataFrame(dat)
    df[[0, 1]] = df[[0, 1]].astype(int)
    df.to_csv(filename, index=False, header=False)
    return f'{filename}文件生成成功！'


def write_dat_binary(dat: np.ndarray, filename: str):
    pass


def write_dat_binary32(dat: np.ndarray, filename: str):
    pass
