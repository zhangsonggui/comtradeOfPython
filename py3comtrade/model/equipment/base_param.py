#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Optional

from pydantic import BaseModel, Field


class BaseParam(BaseModel):
    idx: int = Field(default=None, description="内部索引号")
    name: str = Field(default=None, description="名称，站内唯一")
    reference: Optional[str] = Field(default=None, description="IEC61850参引")
