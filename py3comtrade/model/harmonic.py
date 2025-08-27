#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pydantic import Field, BaseModel


class Harmonic(BaseModel):
    """谐波计算结果"""
    frequency: float = Field(description="频率值")
    amplitude: float = Field(description="幅值")
    # 可以根据需要添加其他字段
    phase: float = Field(default=0.0, description="相位角")
