import os
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field, field_validator, model_validator

from py3comtrade.model.exceptions import (
    ComtradeFileNotFoundException,
    ComtradeFileNumException,
    ComtradeFileSizeException,
    ComtradeFileSuffixException
)
from py3comtrade.utils.log import logger


class ComtradeFile(BaseModel):
    """
    读取comtrade文件

    属性:
        file_path(str): 原始文件路径
    返回:
        ComtradeFile对象,包含file_path同名的所有comtrade后缀文件
    异常:
        ComtradeFileNotFoundException: 文件找不到
        ComtradeFileNumException: 缺少必要的文件
        ComtradeFileSizeException: 文件大小不能小于等于0
        ComtradeFileSuffixException: 文件后缀不符合要求
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
        # 输入验证
        if not v or not isinstance(v, str):
            error_msg = "文件路径不能为空"
            logger.error(error_msg)
            raise ValueError(error_msg)

        # 去除首尾空白字符
        v = v.strip()
        if not v:
            error_msg = "文件路径不能为空白字符"
            logger.error(error_msg)
            raise ValueError(error_msg)

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

        # 检查文件是否存在，并处理符号链接和权限
        try:
            # 解析符号链接，获取真实路径
            real_path = convert_path.resolve()

            # 检查是否为文件且可读
            if not real_path.is_file():
                error_msg = f"文件{v}不存在或不可访问"
                logger.error(error_msg)
                raise ComtradeFileNotFoundException(file_path=v, message=error_msg)

            # 检查文件权限
            if not os.access(real_path, os.R_OK):
                error_msg = f"文件{v}不可读"
                logger.error(error_msg)
                raise ComtradeFileNotFoundException(file_path=v, message=error_msg)

        except (OSError, PermissionError) as e:
            error_msg = f"访问文件{v}时发生错误: {str(e)}"
            logger.error(error_msg)
            raise ComtradeFileNotFoundException(file_path=v, message=error_msg)

        # 检查文件大小（只有在文件存在时才检查）
        try:
            size_bytes = real_path.stat().st_size
            if size_bytes <= 0:
                error_msg = f"文件{v}大小应大于0"
                logger.error(error_msg)
                raise ComtradeFileSizeException(file_path=v, message=error_msg)
        except OSError as e:
            error_msg = f"无法获取文件{v}的大小信息: {str(e)}"
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

        # 遍历父目录中的所有文件，优化文件系统操作
        try:
            for item in parent.iterdir():
                # 先检查基本条件，避免不必要的文件系统调用
                if item.stem != stem or item.suffix.lower() not in suffix_mapping:
                    continue

                # 只有必要时才检查文件属性
                try:
                    if item.is_file() and item.stat().st_size > 0:
                        attr_name = suffix_mapping[item.suffix.lower()]
                        setattr(self, attr_name, item)
                except (OSError, PermissionError):
                    # 忽略无法访问的文件
                    continue
        except (OSError, PermissionError) as e:
            error_msg = f"无法访问目录{parent}: {str(e)}"
            logger.warning(error_msg)
            # 不抛出异常，继续处理

        # 检查cfg_path是否为空（cfg文件是必需的）
        if self.cfg_path is None:
            error_msg = f"{self.file_path}文件最少要包含cfg文件"
            logger.error(error_msg)
            raise ComtradeFileNumException(
                file_path=self.file_path, message=error_msg)

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
