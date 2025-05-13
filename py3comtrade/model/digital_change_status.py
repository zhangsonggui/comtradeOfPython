from pydantic import BaseModel, Field


class DigitalChangeStatus(BaseModel):
    timestamp:list[int] = Field(default_factory=list, description="时间戳")
    status:list[int] = Field(default_factory=list, description="状态")
