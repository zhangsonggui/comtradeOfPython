#!/usr/bin/env python
# -*- coding: utf-8 -*-


class ComtradeException(Exception):
    """Comtrade模块所有异常的基类"""

    def __init__(self, message=None, error_code=None, original_error=None):
        self.message = message or "Comtrade操作异常"
        self.error_code = error_code
        self.original_error = original_error
        super().__init__(self.message)

    def __str__(self):
        if self.error_code:
            return f"[{self.error_code}] {self.message}"
        return self.message


class ComtradeFileNotFoundException(ComtradeException):
    """文件不存在异常"""
    ERROR_CODE = "FILE_NOT_FOUND"

    def __init__(self, file_path, message=None, original_error=None):
        self.file_path = file_path
        default_message = f"文件不存在: {file_path}"
        super().__init__(message or default_message, self.ERROR_CODE, original_error)


class ComtradeFileEncodingException(ComtradeException):
    """文件编码错误异常"""
    ERROR_CODE = "FILE_ENCODING_ERROR"

    def __init__(self, file_path, message=None, encoding=None, original_error=None):
        self.file_path = file_path
        self.encoding = encoding
        default_message = f"文件编码错误: {file_path}"
        if encoding:
            default_message += f" (尝试的编码: {encoding})"
        super().__init__(message or default_message, self.ERROR_CODE, original_error)


class ComtradeFileParseException(ComtradeException):
    """文件解析失败异常"""
    ERROR_CODE = "FILE_PARSE_ERROR"

    def __init__(self, file_path, message=None, original_error=None):
        self.file_path = file_path
        default_message = f"文件解析失败: {file_path}"
        super().__init__(message or default_message, self.ERROR_CODE, original_error)


class ComtradeDataNullException(ComtradeException):
    """数据内容为空"""
    ERROR_CODE = "DATA_NULL_ERROR"

    def __init__(self, message=None, original_error=None):
        default_message = "数据内容为空"
        super().__init__(message or default_message, self.ERROR_CODE, original_error)


class ComtradeDataFormatException(ComtradeException):
    """数据格式不正确异常"""
    ERROR_CODE = "DATA_FORMAT_ERROR"

    def __init__(self, message=None, data_type=None, original_error=None):
        self.data_type = data_type
        default_message = "数据格式不正确"
        if data_type:
            default_message += f" (数据类型: {data_type})"
        super().__init__(message or default_message, self.ERROR_CODE, original_error)


class ComtradeFileWriteException(ComtradeException):
    """文件写入失败异常"""
    ERROR_CODE = "FILE_WRITE_ERROR"

    def __init__(self, file_path, message=None, original_error=None):
        self.file_path = file_path
        default_message = f"文件写入失败: {file_path}"
        super().__init__(message or default_message, self.ERROR_CODE, original_error)


class ChannelNotFoundException(ComtradeException):
    """通道未找到异常"""
    ERROR_CODE = "CHANNEL_NOT_FOUND"

    def __init__(self, channel_id, channel_type=None, message=None, original_error=None):
        self.channel_id = channel_id
        self.channel_type = channel_type
        default_message = f"通道未找到: {channel_id}"
        if channel_type:
            default_message += f" (通道类型: {channel_type})"
        super().__init__(message or default_message, self.ERROR_CODE, original_error)


class InvalidIndexException(ComtradeException):
    """索引无效异常"""
    ERROR_CODE = "INVALID_INDEX"

    def __init__(self, index, valid_range=None, message=None, original_error=None):
        self.index = index
        self.valid_range = valid_range
        default_message = f"索引无效: {index}"
        if valid_range:
            default_message += f" (有效范围: {valid_range})"
        super().__init__(message or default_message, self.ERROR_CODE, original_error)


class InvalidOperationException(ComtradeException):
    """无效操作异常"""
    ERROR_CODE = "INVALID_OPERATION"

    def __init__(self, operation, message=None, original_error=None):
        self.operation = operation
        default_message = f"无效操作: {operation}"
        super().__init__(message or default_message, self.ERROR_CODE, original_error)
