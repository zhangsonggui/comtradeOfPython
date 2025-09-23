#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  Copyright (c) [2019] [name of copyright holder]
#  [py3comtrade] is licensed under Mulan PSL v2.
#  You can use this software according to the terms and conditions of the Mulan
#  PSL v2.
#  You may obtain a copy of Mulan PSL v2 at:
#           http://license.coscl.org.cn/MulanPSL2
#  THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY
#  KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
#  NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
#  See the Mulan PSL v2 for more details.
from datetime import datetime
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field

from py3comtrade.utils.file_tools import verify_file_validity


class ComtradeFilePath(BaseModel):
    cfg_path: Path = Field(default=None, description="Comtrade配置文件路径")
    dat_path: Path = Field(default=None, description="Comtrade数据文件路径")
    dmf_path: Path = Field(default=None, description="Comtrade模型文件路径")


def generate_comtrade_path(_file_path: str = None) -> ComtradeFilePath:
    """
    生成Comtrade文件路径对象

    参数：
        _file_path: comtrade任一格式文件名，可不含后缀名
    返回值:
        ComtradeFilePath对象
    """
    _cfp = Path(_file_path) if _file_path else Path.cwd()

    # 检查是否为目录路径或以分隔符结尾的路径
    if (_cfp.exists() and _cfp.is_dir()) or str(_file_path).endswith(('/', '\\')):
        # 如果是目录，则在目录下生成基于时间戳的文件名
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        _cfp = _cfp / timestamp
    # 如果没有提供文件名，则使用当前时间生成默认文件名
    elif not _cfp.name or _cfp.name == '.':
        timestamp = datetime.now().strftime("%Y%m%d%H%M")
        _cfp = _cfp / timestamp

    cfg_path = _cfp.with_suffix(".cfg")
    dat_path = _cfp.with_suffix(".dat")
    dmf_path = _cfp.with_suffix(".dmf")
    return ComtradeFilePath(cfg_path=cfg_path, dat_path=dat_path, dmf_path=dmf_path)


def get_comtrade_path(_file_path: str) -> Optional[ComtradeFilePath]:
    """
    根据传入的文件路径获取不同后缀名的一组文件,兼容后缀名大小写和无后缀名。

    参数：
        _file_path: 指定文件路径,可不包含文件后缀名
    返回值:
        ComtradeFilePath对象，文件不存在返回空
    """
    file_path = Path(_file_path)
    # 定义后缀名组合，优先检查小写，再检查大写
    suffix_combinations = [(".cfg", ".dat", ".dmf"),
                           (".CFG", ".DAT", ".DMF")]
    for cfg_suffix, dat_suffix, dmf_suffix in suffix_combinations:
        cfg_path = file_path.with_suffix(cfg_suffix)
        dat_path = file_path.with_suffix(dat_suffix)
        dmf_path = file_path.with_suffix(dmf_suffix)

        if verify_file_validity(str(cfg_path)) and verify_file_validity(str(dat_path)):
            if verify_file_validity(str(dmf_path)):
                return ComtradeFilePath(cfg_path=cfg_path, dat_path=dat_path, dmf_path=dmf_path)
            else:
                return ComtradeFilePath(cfg_path=cfg_path, dat_path=dat_path)
    return None


if __name__ == '__main__':
    file_path = r'D:\codeArea\gitee\comtradeOfPython\tests\data\xtz.CFG'
    f1 = r'D:\codeArea\gitee\comtradeOfPython\tests'
    cfp = generate_comtrade_path("test")
    print(cfp.model_dump_json(indent=4))
    # file_path = get_comtrade_path(file_path)
    # print(file_path.model_dump_json(indent=4))
