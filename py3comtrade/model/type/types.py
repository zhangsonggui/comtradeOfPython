from enum import Enum
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


class FilePath(TypedDict):
    # 配置文件路径
    cfg_path: Path
    # 数据文件路径
    dat_path: Path
    # 模型文件路径
    dmf_path: Path


class IdxType(Enum):
    INDEX = (0, "index索引")
    CFGAN = (1, "cfg_idx索引")


class ChannelType(Enum):
    ANALOG = (0, "模拟通道")
    DIGITAL = (1, "开关量通道")
    ALL = (2, "全部通道")


class ValueType(BaseEnum):
    INSTANT = ("INSTANT", "瞬时值")
    RAW = ("RAW", "原始采样值")
    RMS = ("RMS", "有效值值")
