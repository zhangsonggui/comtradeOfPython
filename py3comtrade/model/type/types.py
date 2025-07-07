import numpy as np
from numpy.typing import NDArray
from typing_extensions import TypedDict

Array = NDArray
FloatArray64 = NDArray[np.float64]
FloatArray32 = NDArray[np.float32]
IntArray64 = NDArray[np.int64]
IntArray32 = NDArray[np.int32]


class FilePath(TypedDict):
    # 配置文件路径
    cfg_path: str
    # 数据文件路径
    dat_path: str
    # 模型文件路径
    dmf_path: str
