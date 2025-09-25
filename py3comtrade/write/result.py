#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field

from py3comtrade.model.type.ret_enum import Ret


class Result(BaseModel):
    code: Ret = Field(default=Ret.OK, description="返回结果码")
    message: str = Field(default="", description="返回消息")
