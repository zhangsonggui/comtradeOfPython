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
    # 验证或清理路径（简化示例）
    directory = os.path.abspath(directory)
    # 添加递归查找逻辑
    matching_files = []
    if recursive:
        for root, dirs, files in os.walk(directory):
            matching_files.extend([os.path.join(root, file) for file in files if file.endswith(extension)])
    else:
        files_and_dirs = os.listdir(directory)
        matching_files = [os.path.join(directory, file) for file in files_and_dirs if
                          os.path.isfile(os.path.join(directory, file)) and file.endswith(extension)]

    return matching_files


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


def verify_file_validity(file_path: str):
    """
    验证文件是否存在且非空。
    :param file_path: 文件的路径
    :return: 文件名路径或错误信息
    """
    try:
        # 检查文件是否存在
        if not os.path.exists(file_path):
            return f"错误：文件 {file_path} 不存在。"

        # 检查文件是否为空
        if os.path.getsize(file_path) == 0:
            return f"错误：文件 {file_path} 为空。"

        # 如果通过以上检查，说明文件存在且非空
        return file_path
    except Exception as e:
        # 捕获其他可能的异常，如权限问题等
        return f"发生错误：{str(e)}"


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


def zip_files(files, output):
    """压缩多个文件"""
    zip = zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED)
    for file in files:
        zip.write(file)
    zip.close()


def zip_dir(path, output=None):
    """压缩指定目录"""
    output = output or os.path.basename(path) + '.zip'  # 压缩文件的名字
    zip = zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(path):
        relative_root = '' if root == path else root.replace(path, '') + os.sep  # 计算文件相对路径
        for filename in files:
            zip.write(os.path.join(root, filename), relative_root + filename)  # 文件路径 压缩文件路径（相对路径）
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
