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
from pathlib import Path

from pydantic_settings import BaseSettings


# !/usr/bin/env python
# -*- coding: utf-8 -*-


class Settings(BaseSettings):
    VERSION: str = "4.2.2"
    APP_TITLE: str = "波形解析器"
    PROJECT_NAME: str = "py3comtrade"
    APP_DESCRIPTION: str = "解析comtrade中的cfg、dat、dmf等文件，提供配置文件中通道数量，的解析、数值计算和文件合并功能。"

    DEBUG: bool = False

    PROJECT_ROOT: Path = Path(__file__).parent.parent.resolve()
    BASE_DIR: Path = PROJECT_ROOT.parent.resolve()
    LOGS: Path = BASE_DIR / "logs"


settings = Settings()
