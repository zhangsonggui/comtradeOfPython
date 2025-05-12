from numpy.typing import NDArray
from typing import TypedDict
import numpy as np

Array = NDArray
FloatArray64 = NDArray[np.float64]
FloatArray32 = NDArray[np.float32]
IntArray64 = NDArray[np.int64]
IntArray32 = NDArray[np.int32]

class FilePath(TypedDict):
    cfg_path: str
    dat_path: str
    dmf_path: str
