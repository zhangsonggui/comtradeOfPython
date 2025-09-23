#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@File    :   file_encoding.py
@Time    :   2025/05/15
@Version :   1.0
@Desc    :   文件编码工具
"""
import argparse
import codecs
import logging
import os
from typing import List

import chardet

from py3comtrade.model.exceptions import FileNotFoundException, FileEncodingException

# 配置日志系统
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # 输出到控制台
        logging.FileHandler('log.txt', mode='w', encoding='utf-8')  # 输出到文件,取消注释
    ]
)
# 定义读取字节数的常量
READ_BYTES_FOR_ENCODING = 10 * 1024  # 10KB


def is_valid_encoding(encoding: str) -> bool:
    """
    检查编码是否合法
    """
    try:
        if encoding:
            codecs.lookup(encoding)
            return True
    except LookupError:
        pass
    return False


def detect_file_encoding(file_path: str):
    """
    读取文件前10KB数据用于检测编码格式
    :param file_path: 文件路径
    :return: 检测到的编码格式，若无法识别则返回 None
    """
    if not isinstance(file_path, str):
        raise logging.error(f"必须是一个字符串,{file_path}")

    try:
        if not os.path.exists(file_path):
            raise FileNotFoundException(file_path)
        
        with open(file_path, "rb") as file:
            raw_data = file.read(READ_BYTES_FOR_ENCODING)
            result = chardet.detect(raw_data)

            # 可选：根据置信度过滤结果
            if result["confidence"] < 0.5:
                return None

            return result["encoding"] if is_valid_encoding(result["encoding"]) else None
    except FileNotFoundException:
        raise
    except (IOError, OSError) as e:
        logging.error(f"无法读取文件 {file_path}: {e}")
        raise FileEncodingException(file_path, f"无法读取文件: {str(e)}", original_error=e)


def detect_os_encoding():
    """
    检查操作系统的编码设置
    :return: 系统的编码设置
    """
    import locale
    return locale.getpreferredencoding()


def convert_file_encoding(_file_path: str, target_encoding: str):
    """
    将文件转换为目标编码
    :param _file_path:文件路径
    :param target_encoding:目标编码
    """
    if not os.path.isfile(_file_path):
        logging.error(f"不是一个文件，或文件不存在：{_file_path}")
        return

    original_encoding = detect_file_encoding(_file_path)
    if original_encoding is None:
        logging.warning(f"无法识别文件编码，跳过转换：{_file_path}")
        return

    if is_valid_encoding(target_encoding) is False:
        logging.error(f"目标编码格式错误：{_file_path}")
        return

    if original_encoding == target_encoding:
        return

    try:
        # 使用临时文件避免数据丢失
        temp_file_path = _file_path + ".tmp"
        with open(_file_path, "r", encoding=original_encoding) as src_file, open(temp_file_path, "w",
                                                                                 encoding=target_encoding) as dst_file:
            while True:
                chunk = src_file.read(1024 * 1024)  # 每次读取1MB
                if not chunk:
                    break
                dst_file.write(chunk)
        # 替换原文件
        os.replace(temp_file_path, _file_path)
    except Exception:
        logging.warning(f"转换文件编码失败: {_file_path}")
    logging.info(f"转换文件编码成功: {_file_path}")


def list_files(directory: str, _recursive: bool = False, suffixes: List[str] = None) -> List[str]:
    """
    获取指定目录下的所有文件路径
    :param directory: 目录路径
    :param _recursive: 是否递归搜索子目录
    :param suffixes: 仅查找文件后缀
    :return: 文件路径列表
    """
    file_paths = []
    for root, dirs, files in os.walk(directory):
        if not _recursive:
            dirs[:] = []
        for file in files:
            if suffixes is None or any(file.endswith(suffix) for suffix in suffixes):
                file_paths.append(os.path.join(root, file))
    return file_paths


def parse_arguments():
    parser = argparse.ArgumentParser(description='文件编码转换工具。')
    parser.add_argument('file_path', type=str, nargs='?', default=None,
                        help='待转换编码文件或目录(可选，默认为当前目录的所有文件)')
    parser.add_argument('recursive', type=bool, nargs='?', default=False,
                        help='是否递归处理子目录中的文件(可选，默认不递归)')
    parser.add_argument('target_encoding', type=str, nargs='?', default=None,
                        help='目标编码（可选，默认为操作系统编码）')

    return parser.parse_args()


def convert_encoding(_file_path: str, _recursive: bool = False, _target_encoding: str = None):
    """
    编码转换程序
    :param _file_path:待转换的文件路径或目录，如为空为当前目录中中的文件
    :param _recursive:是否递归处理子目录中的文件
    :param _target_encoding:待处理的编码
    """
    _target_encoding = detect_os_encoding() if _target_encoding is None else _target_encoding

    if os.path.isdir(_file_path):
        logging.info(f"待处理的目录：{_file_path}")
        _files = list_files(_file_path, _recursive=_recursive)
        for _file in _files:
            convert_file_encoding(_file, _target_encoding)
        logging.info(f"编码转换完成:{_file_path}")
    else:
        convert_file_encoding(_file_path, _target_encoding)


if __name__ == '__main__':
    args = parse_arguments()
    file_path = args.file_path
    recursive = args.recursive
    target_encoding = args.target_encoding
    convert_encoding(file_path, recursive, target_encoding)
