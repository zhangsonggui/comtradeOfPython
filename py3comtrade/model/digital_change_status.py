from typing import List

from pydantic import BaseModel, Field


class StatusRecord(BaseModel):
    """表示一个变为记录的模型类，包含时间戳和状态"""
    timestamp: int = Field(description="时间戳")
    status: int = Field(description="状态")

class DigitalChangeStatus(BaseModel):
    records: List[StatusRecord] = Field(default_factory=list, description="变位记录列表")
