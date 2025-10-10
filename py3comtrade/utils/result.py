#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field
from typing import Any, Optional



class Result(BaseModel):
    code: int = Field(default=200, description="结果码")
    msg: Optional[str] = Field(default="OK", description="消息")
    data: Optional[Any] = Field(default=None, description="数据")

    class Config:
        extra = 'allow'

    def __str__(self) -> str:
        return f"code:{self.code}msg:{self.msg}内容:{self.data}"
