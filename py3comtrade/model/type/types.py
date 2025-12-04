from pathlib import Path

import numpy as np
from numpy.typing import NDArray
from typing_extensions import TypedDict

from py3comtrade.model.type.base_enum import BaseEnum

Array = NDArray
FloatArray64 = NDArray[np.float64]
FloatArray32 = NDArray[np.float32]
IntArray64 = NDArray[np.int64]
IntArray32 = NDArray[np.int32]


class SampleMode(BaseEnum):
    CENTERED = ("CENTERED", "以当前点为中心，前后各取数据。")  # 表示以当前点为中心，前后各取数据。
    FORWARD = ("FORWARD", "表示从起点向后取数据。")
    BACKWARD = ("BACKWARD", "表示从终点向前取数据。")


class IdxType(BaseEnum):
    INDEX = ("INDEX", "index索引")
    CFGAN = ("CFGAN", "cfg_idx索引")


class ChannelType(BaseEnum):
    ANALOG = ("ANALOG", "模拟通道")
    DIGITAL = ("DIGITAL", "开关量通道")
    ALL = ("ALL", "全部通道")


class ValueType(BaseEnum):
    INSTANT = ("INSTANT", "瞬时值")
    RAW = ("RAW", "原始采样值")
    RMS = ("RMS", "有效值值")
