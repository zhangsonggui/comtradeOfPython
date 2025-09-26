#!/usr/bin/env python
# -*- coding: utf-8 -*-
from py3comtrade.model.type.base_enum import BaseEnum


class Ret(BaseEnum):
    OK = (200, "成功")
    CONTINUE = (100, "继续")
    CREATED = (201, "已创建")
    ACCEPTED = (202, "已接受,未处理完")
    NO_CONTENT = (204, "无内容")
    NOT_ACCEPTABLE = (404, "请求内容不存在")
    ERROR = (500, "错误")
    NOT_IMPLEMENTED = (501, "不支持的方法")
