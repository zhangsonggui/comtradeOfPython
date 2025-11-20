from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field, field_validator, model_validator

from py3comtrade.model.exceptions import ComtradeFileNotFoundException, \
    ComtradeFileNumException, ComtradeFileSizeException, ComtradeFileSuffixException
from py3comtrade.utils import logger


class ComtradeFile(BaseModel):
    """
    读取comtrade文件

    属性:
        file_path(str): 原始文件路径
    返回:
        ComtradeFile对象,包含file_path同名的所有comtrade后缀文件
    异常:
        ValueError:文件找不到
    """
    # 原始文件路径
    file_path: str = Field(..., description="原始文件路径", exclude=True)
    # 文件路径属性
    cfg_path: Optional[Path] = Field(default=None)
    dat_path: Optional[Path] = Field(default=None)
    dmf_path: Optional[Path] = Field(default=None)
    hdr_path: Optional[Path] = Field(default=None)
    inf_path: Optional[Path] = Field(default=None)

    class Config:
        arbitrary_types_allowed = True

    @field_validator('file_path')
    def validate_file_path(cls, v: str) -> str:
        """验证文件路径"""
        convert_path = Path(v)

        # 定义期望的后缀列表
        expected_suffixes = ('.cfg', '.dat', '.dmf', '.hdr', '.inf')

        # 如果没有后缀，尝试添加第一个期望的后缀
        if not convert_path.suffix:
            convert_path = convert_path.with_suffix(expected_suffixes[0])

        # 检查后缀是否在期望的后缀列表中
        if convert_path.suffix.lower() not in expected_suffixes:
            error_msg = f"文件后缀必须是{expected_suffixes}之一"
            logger.error(error_msg)
            raise ComtradeFileSuffixException(file_path=v, message=error_msg)

        # 检查文件是否存在
        if not convert_path.is_file():
            error_msg = f"文件{v}不存在"
            logger.error(error_msg)
            raise ComtradeFileNotFoundException(file_path=v, message=error_msg)

        # 检查文件大小
        size_bytes = convert_path.stat().st_size
        if size_bytes <= 0:
            error_msg = f"文件{v}大小应大于0"
            logger.error(error_msg)
            raise ComtradeFileSizeException(file_path=v, message=error_msg)

        return str(convert_path)

    @model_validator(mode='after')
    def find_sibling_files(self) -> 'ComtradeFile':
        """查找同目录下的相关文件"""
        _file_path = Path(self.file_path)
        parent = _file_path.parent
        stem = _file_path.stem

        # 创建后缀到属性的映射
        suffix_mapping = {
            '.cfg': 'cfg_path',
            '.dat': 'dat_path',
            '.dmf': 'dmf_path',
            '.hdr': 'hdr_path',
            '.inf': 'inf_path'
        }

        # 遍历父目录中的所有文件
        for item in parent.iterdir():
            if (item.is_file() and
                    item.stem == stem and
                    item.stat().st_size > 0 and
                    item.suffix.lower() in suffix_mapping):
                attr_name = suffix_mapping[item.suffix.lower()]
                setattr(self, attr_name, item)

        # 检查cfg_path和dat_path是否都为空
        if self.cfg_path is None or self.dat_path is None:
            error_msg = f"{self.file_path}文件最少要包含cfg和dat文件"
            logger.error(error_msg)
            raise ComtradeFileNumException(file_path=self.file_path, message=error_msg)

        return self

    def __repr__(self) -> str:
        return f"ComtradeFile(file_path='{self.file_path}', cfg={self.cfg_path is not None}, dat={self.dat_path is not None})"


# 示例用法
if __name__ == "__main__":
    file_path = r"D:\codeArea\gitee\comtradeOfPython\tests\data\hjz"
    cfr = ComtradeFile(file_path=file_path)
    print(f"CFG: {cfr.cfg_path}")
    print(f"DAT: {cfr.dat_path}")
    print(f"DMF: {cfr.dmf_path}")
    print(f"HDR: {cfr.hdr_path}")
    print(f"INF: {cfr.inf_path}")

    # 安全地获取文件大小
    if cfr.cfg_path:
        print(f"CFG size: {cfr.cfg_path.stat().st_size}")
    if cfr.dat_path:
        print(f"DAT size: {cfr.dat_path.stat().st_size}")
    if cfr.dmf_path:
        print(f"DMF size: {cfr.dmf_path.stat().st_size}")
    if cfr.hdr_path:
        print(f"HDR size: {cfr.hdr_path.stat().st_size}")
    if cfr.inf_path:
        print(f"INF size: {cfr.inf_path.stat().st_size}")
