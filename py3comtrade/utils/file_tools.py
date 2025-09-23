#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@File    :   file_tools.py
@Time    :   2024/06/17
@Version :   1.0
@Desc    :   文件操作工具
"""
import os
import zipfile
from pathlib import Path

# 定义读取字节数的常量
READ_BYTES_FOR_ENCODING = 10 * 1024  # 10KB


def generate_filename_with_timestamp(prefix="", suffix="", _format="%Y%m%d%H%M%S"):
    """
    以当前时间生成文件名

    :param prefix: 文件名前缀
    :param suffix: 文件名后缀（如 .txt, .log 等）
    :param _format: 时间格式，默认为 "%Y%m%d%H%M%S"
    :return: 基于当前时间生成的文件名
    """
    from datetime import datetime
    timestamp = datetime.now().strftime(_format)
    return f"{prefix}{timestamp}{suffix}"


def file_finder(directory: str, extension: str, recursive: bool = False):
    """
    查找指定目录下所有指定后缀名的文件
    :param directory: 指定目录
    :param extension: 指定后缀名,应以点号开头，如.cfg
    :param recursive: 是否递归查找
    :return: 符合条件的文件列表
    """
    # 确保后缀名以点号开头
    if not extension.startswith('.'):
        extension = '.' + extension

    # 使用pathlib处理路径
    directory_path = Path(directory)

    # 检查目录是否存在
    if not directory_path.exists():
        raise FileNotFoundError(f"目录不存在: {directory}")

    if not directory_path.is_dir():
        raise NotADirectoryError(f"路径不是目录: {directory}")

    # 根据是否递归查找来获取文件
    if recursive:
        # 递归查找所有匹配后缀的文件
        pattern = f"**/*{extension}"
        matching_files = list(directory_path.glob(pattern))
    else:
        # 只在当前目录查找匹配后缀的文件
        pattern = f"*{extension}"
        matching_files = list(directory_path.glob(pattern))
        # 过滤出文件（排除目录）
        matching_files = [f for f in matching_files if f.is_file()]

        # 只返回文件路径的字符串形式
    return [str(f) for f in matching_files]


def split_path(path):
    """
    分割文件路径为目录、文件名和后缀名
    :param path: 文件全路径
    :return: 目录、文件名和后缀名元祖
    """
    # 分离目录和文件名（含后缀）
    dir_name, file_name_with_extension = os.path.split(path)
    # 分离文件名和后缀
    file_name, extension = os.path.splitext(file_name_with_extension)
    return dir_name, file_name, extension


def verify_file_validity(_file_path: str) -> bool:
    """
    验证文件是否存在且非空。
    :param _file_path: 文件的路径
    :return: 文件名路径或错误信息
    """
    _file_path = Path(_file_path)
    if not _file_path.exists():
        return False
    if not _file_path.is_file():
        return False
    return _file_path.stat().st_size != 0


def read_file_adaptive_encoding(filename):
    """
    尝试以GBK和UTF-8两种编码读取文件，以适应不确定的编码情况。
    :param filename: 要读取的文件名
    :return: 文件内容字符串，如果两种编码都失败，则返回None
    """
    try:
        # 首先尝试以UTF-8编码读取
        with open(filename, 'r', encoding='utf-8') as file:
            return file.readlines()
    except UnicodeDecodeError:
        # 如果UTF-8解码失败，再尝试GBK编码
        try:
            with open(filename, 'r', encoding='gbk') as file:
                return file.readlines()
        except UnicodeDecodeError:
            # 如果GBK也失败，打印错误信息并返回None
            print(f"读取文件'{filename}'时，UTF-8和GBK编码均失败。")
            return None
    except IOError as e:
        print(f"读取文件'{filename}'时发生错误：{e}")
        return None


def zip_files(_files: list[str], output: str):
    """压缩多个文件
    参数:
        _files:文件列表
        output:输出目录
    返回值:
        压缩包
    """
    if output is None:
        output = generate_filename_with_timestamp(suffix=".zip")
    try:
        with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as zip:
            for file in _files:
                zip.write(file)
    except Exception as e:
        raise Exception(f"创建ZIP文件时发生错误: {e}")


def zip_dir(path, output=None):
    """压缩指定目录"""
    output = output or os.path.basename(path) + '.zip'  # 压缩文件的名字
    zip = zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(path):
        relative_root = '' if root == path else root.replace(path, '') + os.sep  # 计算文件相对路径
        for filename in files:
            zip.write(str(os.path.join(root, filename)), relative_root + filename)  # 文件路径 压缩文件路径（相对路径）
    zip.close()


def extract_files_with_suffixes(zip_file, output=None, suffixes=None):
    """
    从压缩文件中解压指定后缀名称到指定目录
    :param zip_file :压缩文件路径
    :param output:解压目标文件夹路径,当为None时，解压到压缩文件所在目录
    :param suffixes:要解压的文件后缀列表
    """
    zip_path, zip_name, _ = split_path(zip_file)
    # 指定解压的目标文件夹路径
    output = output or os.path.join(zip_path, zip_name)  # 默认解压到当前目录同名文件夹中
    # 使用zipfile模块打开ZIP文件并解压
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        for entry in zip_ref.namelist():
            if any(entry.endswith(suffix) for suffix in suffixes):
                zip_ref.extract(entry, output)


if __name__ == '__main__':
    fd = r"Y:\2013"
    files = file_finder(fd, ".cfg", True)
    print(files)
