#!/usr/bin/env python
# -*- coding: utf-8 -*-
from py3comtrade.model.configure import Configure


def generate_cfg_str(cfg_obj: Configure):
    """
    生成cfg文件字符串
    @param cfg_obj: cfg对象
    @return: cfg文件字符串
    """
    cfg_content = ''
    cfg_content += str(cfg_obj.header) + "\n"
    cfg_content += str(cfg_obj.channel_num) + "\n"
    for ac in cfg_obj.analogs:
        cfg_content += str(ac) + '\n'
    for dc in cfg_obj.digitals:
        cfg_content += str(dc) + '\n'
    cfg_content += str(cfg_obj.sample) + "\n"
    cfg_content += str(cfg_obj.file_start_time) + "\n"
    cfg_content += str(cfg_obj.fault_time) + "\n"
    cfg_content += str(cfg_obj.timemult)

    return cfg_content


def configure_to_file(cfg: Configure, filename: str):
    """
    将cfg对象写入文件
    :param cfg: cfg文件对象
    :param filename: 文件名
    """
    with open(filename, 'w', encoding='gbk') as f:
        f.write(generate_cfg_str(cfg))
    return f'{filename}文件生成成功！'
