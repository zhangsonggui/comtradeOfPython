#!/usr/bin/python3
# _*_ coding: utf-8 _*_
#
# Copyright (C) 2024 - 2024 张松贵, Inc. All Rights Reserved
#
# @Time    : 2024/3/23 11:27
# @Author  : 张松贵
# @File    : CFGParser.py
# @IDE     : PyCharm
import logging
from datetime import datetime
from typing import Union

from comtradeParser.utils import constants


class CFGParser:
    """
    这是用于读取IEEE Comtrade cfg文件的python类
    提供通道信息，开关量信息获取，采样段信息，游标位置和周波采样信息
    """
    # 1.基本信息
    _file_handler = ''  # 文件处理
    _station_name = ''  # 变电站名称
    _rec_dev_id = ''  # 设备名称
    _rev_year = 1991  # 版本年份，默认为1991
    _TT = 0  # 通道总数
    _A = 0  # 模拟量数量
    _D = 0  # 开关量数量
    # 2.模拟量通道信息:
    _ans = []
    # 3.开关量通道信息:
    _dns = []
    # 4.其他信息
    _lf = 0  # 频率
    _nrates_num: int = 0  # 采样段数量
    _nrates = []  # 采样段信息
    _start_time = ''  # 文件开始时间绝对时间
    _trigger_time = None  # 文件零时刻绝对时间
    _zero_time: int = 0  # 零时刻相对时间
    _zero_point: int = 0  # 零时刻采样点
    _ft = ''  # 数据文件格式
    _timemult = 0.0  # 倍增系数

    def __init__(self, cfg_name):
        """
        构造函数：初始化解析CFG文件的实例
        @param cfg_name:CFG文件的路径字符串。
        """
        logging.info("初始化解析{}文件实例!".format(cfg_name))
        self.clear()
        self._parse_cfg(cfg_name)

    def clear(self):
        """
        清除类内部的私有变量
        @return:
        """
        # 1.基本信息
        self._file_handler = ''  # 文件处理
        self._station_name = ''  # 变电站名称
        self._rec_dev_id = ''  # 设备名称
        self._rev_year = 1991  # 版本年份，默认为1991
        self._TT = 0  # 通道总数
        self._A = 0  # 模拟量数量
        self._D = 0  # 开关量数量
        # 2.模拟量通道信息:
        self._ans = []
        # 3.开关量通道信息:
        self._dns = []
        # 4.其他信息
        self._lf = 0  # 频率
        self._nrates_num: int = 0  # 采样段数量
        self._nrates = []  # 采样段数
        self._start_time = ''  # 文件开始时间绝对时间
        self._trigger_time = None  # 文件零时刻绝对时间
        self._zero_time = 0  # 零时刻相对时间,纳秒值
        self._zero_point: int = 0  # 零时刻采样点位置
        self._ft = ''  # 数据文件格式
        self._timemult = 0.0  # 倍增系数

    def _parse_cfg(self, file_name, cfg_content=None):
        """
        解析CFG文件
        :param: CFG文件路径字符串
        """
        if cfg_content is None:
            with open(file_name, 'r', encoding='GBK') as cfg_file:
                self._file_handler = cfg_file.readlines()
        else:
            self._file_handler = cfg_content.split('\n')
        self._parse_header()  # 解析CFG头部信息
        self._parse_channel_num()  # 解析CFG文件通道数量

        for i in range(2, self._A + 2):  # 解析模拟量通道信息，从第三行开始到模拟量通道总数+3
            self._parse_analog(i)

        for i in range(self._A + 2, self._TT + 2):  # 解析开关量通道信息
            self._parse_digital(i)

        # 读取频率信息
        self._lf = int(self._file_handler[self._TT + 2])

        # 处理采样信息
        self._nrates_num = int(self._file_handler[self._TT + 3])
        self._parse_nartes(self._TT + 4, self._TT + 4 + self._nrates_num)
        self._parse_segment()

        # 处理时间
        self._parse_time()

        # 读取数据文件类型
        self._ft = self._file_handler[2 + self._TT + 1 + self._nrates_num + 3].strip('\n')

        # 读取时间倍增系数
        self._timemult = self._parse_timemult()

    def _parse_header(self):
        """
        解析CFG文件的头部信息
        """
        cfg_header = self._file_handler[0]
        cfg_header = cfg_header.split(',')
        self._station_name = cfg_header[0]
        self._rec_dev_id = cfg_header[1]
        if len(cfg_header) > 2:
            self._rev_year = int(cfg_header[2])

    def _parse_channel_num(self):
        """
        解析CFG文件的量通道数量
        """
        channel_num = self._file_handler[1].rstrip()
        tls = channel_num.split(',')
        self._TT = int(tls[0])
        self._A = int(tls[1].strip('A'))
        self._D = int(tls[2].strip('D'))

    def _parse_analog(self, idx: int):
        """
        解析CFG文件的模拟量通道信息
        :@param chid: 模拟量通道行号
        """
        channel_info = self._file_handler[idx]
        channel_info = channel_info.split(',')
        an = {
            "index": idx - 2,
            "an": int(channel_info[0]),
            "chid": channel_info[1],
            "ph": channel_info[2],
            "ccbm": channel_info[3],
            "uu": channel_info[4],
            "a": float(channel_info[5]),
            "b": float(channel_info[6]),
            "skew": float(channel_info[7]),
            "min": int(channel_info[8]),
            "max": int(channel_info[9]),
            "primary": float(channel_info[10]) if len(channel_info) > 10 else 0.0,
            "secondary": float(channel_info[11]) if len(channel_info) > 11 else 0.0,
            "ps": channel_info[12].rstrip() if len(channel_info) > 12 else "S"
        }
        self._ans.append(an)

    def _parse_digital(self, idx):
        """
        解析CFG文件的开关量通道信息
        :@param chid: 开关量通道行号
        """
        channel_info = self._file_handler[idx]
        channel_info = channel_info.split(',')
        dn = {
            "index": idx - 2 - self._A,
            "an": int(channel_info[0]),
            "chid": channel_info[1],
            "ph": channel_info[2],
            "ccbm": channel_info[3] if len(channel_info) > 3 else None
        }
        self._dns.append(dn)

    def _parse_nartes(self, start_idx: int, end_idx: int):
        """
        解析采样频率、最终采样点和对应的没周波采样点数
        该段的开始采样点，结束采样点，采样总数，该段用时
        """
        for i in range(start_idx, end_idx):
            nartes_info = self._file_handler[i]
            nartes_info = nartes_info.split(',')
            # 采样频率
            sample_rate = int(float(nartes_info[0]))
            # 最终采样点
            end_point = int(float(nartes_info[1]))
            # 采样段每周波采样点数
            cycle_sample_num = int(float(sample_rate) / self._lf)
            narte = {
                "sample_rate": sample_rate,
                "end_point": end_point,
                "cycle_sample_num": cycle_sample_num
            }
            self._nrates.append(narte)

    def _parse_segment(self):
        """
        解析采样段信息
        """
        for i in range(self._nrates_num):
            narate = self._nrates[i]
            sample_num = narate['end_point'] if i == 0 else narate['end_point'] - self._nrates[i - 1]['end_point']
            self._nrates[i]['sample_num'] = sample_num
            start_point = 0 if i == 0 else self._nrates[i - 1].get('end_point')
            self._nrates[i]['start_point'] = start_point
            # 计算采样段一共用了多少时间
            waste_time = sample_num / narate["cycle_sample_num"] * 20
            self._nrates[i]['waste_time'] = waste_time
            end_time = waste_time if i == 0 else waste_time + self._nrates[i - 1]['waste_time']
            self._nrates[i]['end_time'] = end_time

    def _parse_time(self):
        """
        解析时间
        """
        strtime = self._file_handler[2 + self._TT + 1 + self._nrates_num + 1].strip('\n').strip()
        self._start_time = datetime.strptime(strtime, '%d/%m/%Y,%H:%M:%S.%f')
        strtime = self._file_handler[2 + self._TT + 1 + self._nrates_num + 2].strip('\n').strip()
        self._trigger_time = datetime.strptime(strtime, '%d/%m/%Y,%H:%M:%S.%f')
        self._zero_time = (self._trigger_time - self._start_time).microseconds
        self._zero_point = self.get_zero_point()

    def _parse_timemult(self):
        """
        解析时间倍增系数
        """
        try:
            timemult = float(self._file_handler[self._TT + self._nrates_num + 4])
        except IndexError:
            timemult = 1.0
        except ValueError:
            timemult = 1.0
        return timemult

    def get_station_name(self) -> str:
        """
        获取变电站名称
        @return: 字符串，变电站名称
        """
        return self._station_name

    def get_total_channel_num(self) -> int:
        """
        获取模拟量和开关量通道总数
        @return: 整数，通道总数
        """
        return self._TT

    def get_sample_num(self) -> int:
        """
        返回总采样点数
        @return: 返回总采样点数，类型为整形
        """
        return self._nrates[-1]['end_point']

    def get_cursor_sample_range(self, point1: int = 0, point2: int = None,
                                cycle_num: float = None, mode=1) -> tuple:
        """
        获取游标采样点位置开始、结束采样取值范围、采样点个数，当end_point不为空，以end_point采样点为准，
        当end_point和cycle_num同时为空时，获取全部采样点，
        当cycle_num不为空按整周波倍数默认向后取值。
        :param point1: 采样起始点，默认为0
        :param point2: 采样终止点，不含终止点，默认为None 代表全部采样点
        :param cycle_num: 采样周波数量，当end_point为空时生效
        :param mode: 取值模式，仅在按周波取值时生效，默认为1：代表向采样点后方取值，-1：代表向采样点前方取值，0：代表向采样点两边取值
        :return: 返回一个二维数组，一维是通道，二维是各采样点的瞬时值数组
        """
        start_point = point1
        # 当end_point不为空时，以end_point为最后采样点
        if point2 is not None:
            end_point = point2
        # 当end_point和cycle_num都为空时，获取全部采样点
        elif point2 is None and cycle_num is None:
            end_point = self.get_sample_num() - 1
        # 按周波计算采样点范围，当跨采样段取该段的最后一个值，如果向前取值开始采样点为该段的第一个值
        else:
            start_point, end_point = self.get_cursor_cycle_sample_range(point1, cycle_num, mode)
        samp_num = end_point - start_point
        return start_point, end_point, samp_num + 1

    def get_cursor_cycle_sample_range(self, point1: int = 0, cycle_num: float = 1, mode=1) -> tuple:
        """
        获取游标采样点所在周波获取采样取值范围
        @param point1:游标位置
        @param cycle_num:周波数量
        @param mode:取值模式，仅在按周波取值时生效，默认为1：代表向采样点后方取值，-1：代表向采样点前方取值，0：代表向采样点两边取值
        @return 返回起始点和终止点
        """
        point1_segment = self.get_cursor_point_in_segment(point1)
        point1_cycle_samp_num = self.get_cursor_cycle_sample_num(point1)
        # 根据采样点1的每周波采样数获取采样数量
        if point1_cycle_samp_num == 1:  # 当每周波采样数为1工频采样时，取两个点
            samp_num = 2
        elif point1_cycle_samp_num % 2 == 0:  # 当每周波采样数为偶数时，取周波数的倍数-1
            samp_num = int(cycle_num * point1_cycle_samp_num) - 1
        else:  # 当每周波采样数为奇数时，取周波数的倍数
            samp_num = int(cycle_num * point1_cycle_samp_num)
        # 根据取值模式，计算采样点
        if mode == -1:
            point1 = point1 - samp_num if point1 >= samp_num else 0
            point2 = point1 + samp_num
        elif mode == 0:
            offset_point = samp_num // 2
            point1 = point1 - offset_point if point1 >= offset_point else 0
            point2 = point1 + samp_num
        else:
            point2 = point1 + samp_num
        # 判断两点采样频率是否相等
        if not self.equal_samp_rate(point1, point2):
            if mode == 1:
                point2 = self._nrates[point1_segment]["end_point"] - 1
                point1 = point2 - samp_num
            else:
                point1 = 0 if point1_segment == 0 else self._nrates[point1_segment]["end_points"] - 1
                point2 = point1 + samp_num
        return point1, point2

    def get_segment_cycle_sample_num(self, nrate: int = 0) -> int:
        """
        获取当前采样段每周波采多少个点
        @param nrate: 采样信息段，类型为整形，从0开始，默认为0
        @return: 返回当前采样段每周波采多少个点，类型为整形
        """
        return self._nrates[nrate]["cycle_sample_num"]

    def get_cursor_cycle_sample_num(self, cursor_site: int) -> int:
        """
        获取游标位置的每周波采样点数
        @param cursor_site: 游标采样点位置
        @return: 游标位置采样点数
        """
        n = self.get_cursor_point_in_segment(cursor_site)  # 所在采样段
        return self.get_segment_cycle_sample_num(n)  # 每周波采样点数

    def get_point_between_segment(self, point1: int, point2: int) -> list:
        """
        获取两个采样点之间的采样段列表
        @param point1: 采样点1的位置
        @param point2: 采样点2的位置
        @return: 两个采样点所在的采样段列表
        """
        segment = []
        if not isinstance(point1, int) or (
                point2 is not None and not isinstance(point2, int)):
            raise ValueError("point1 和 point2 必须是整数")
        point1_segment = self.get_cursor_point_in_segment(point1)
        point2_segment = self.get_cursor_point_in_segment(point2)
        for i in range(point1_segment, point2_segment + 1):
            segment.append(i)
        return segment

    def get_point_between_segment_sample_num(self, point1: int, point2: int) -> list:
        """
        获取两个采样点之间每个采样段所涉及的采样点
        @param point1: 采样点1的位置
        @param point2: 采样点2的位置
        @return: 两个采样点之间每段采样段的采样点列表
        """
        if point1 is None:
            point1 = 0
        if point2 is None:
            point2 = self.get_sample_num()
        segment_sample_num = []
        if not isinstance(point1, int) or (
                point2 is not None and not isinstance(point2, int)):
            raise ValueError("point1 和 point2 必须是整数")
        segment = self.get_point_between_segment(point1, point2)
        # 如果两个点的采样频率相同，直接返回两点的差
        if self.equal_samp_rate(point1, point2):
            return [point2 - point1]
        # 循环除最后一个采样段以外的每个采样段的采样点数
        for i, val in enumerate(segment):
            nrate = self._nrates[val]
            if i == 0:  # 第一个采样段考虑开始采样点不是该段的第一个值
                first_segment_sample = nrate.get('sample_num') - point1 + nrate.get('start_point')
                segment_sample_num.append(first_segment_sample)
            else:
                segment_sample_num.append(nrate.get('sample_num'))
        # 判断最后一个采样段的采样点和该段的最终采样点不一致时，以point2点减去开始的点
        end_segment = self._nrates[segment[-1]]
        if point2 != end_segment.get('end_point'):
            segment_sample_num[-1] = point2 - end_segment.get('start_point')
        return segment_sample_num

    def get_cursor_point_in_segment(self, cursor_site: int) -> int:
        """
        获取游标采样点所在的采样段
        @param cursor_site: 采样点位置
        @return: 采样点所在的采样段
        """
        for i in range(self._nrates_num):
            nrate = self._nrates[i]
            if nrate["start_point"] <= cursor_site < nrate["end_point"]:
                return i

    def equal_samp_rate(self, point1: int, point2: int) -> bool:
        """
        比较两个采样点所在的采样点是否一致
        :param point1: 采样点1的位置
        :param point2: 采样点2的位置
        :return: True or False
        """
        segment_num = []
        point1_segment = self.get_cursor_point_in_segment(point1)
        point2_segment = self.get_cursor_point_in_segment(point2)
        for i in range(point1_segment, point2_segment + 1):
            segment_num.append(self.get_segment_cycle_sample_num(i))
        return True if len(set(segment_num)) == 1 else False

    def get_zero_time_from_cfg(self) -> int:
        """
        返回cfg文件中零时刻的相对时间，单位：纳秒
        @return: 返回整型的纳秒值
        """
        return self._zero_time

    def get_trigger_time_from_cfg(self) -> datetime:
        """
        返回故障时刻的绝对时间
        @return: 返回故障时刻的绝对时间
        """
        return self._trigger_time

    def get_zero_in_cycle(self) -> int:
        """
        根据零时刻相对时间和每一段采样值的最后时间相比较，确定在那个采样段内
        @return: 返回零时刻所在采样段
        """
        for i in range(self._nrates_num):
            if self.get_zero_time_from_cfg() < self._nrates[i]["end_time"] * 1000:
                return i

    def get_zero_point(self) -> int:
        """
        获取零时刻采样值采样点位置。
        使用零时刻相对时间除以每周波的时间，在乘以零时刻所在采样段每个周波的采样点
        @return: 零时刻采样点位置
        """
        n = self.get_zero_in_cycle()
        return round(self.get_zero_time_from_cfg() / 20000 * self.get_segment_cycle_sample_num(n))

    def get_analog_channel_num(self):
        """
        获取模拟通道数
        :return: 模拟量通道数
        """
        return self._A

    def get_channel_info(self, cfg_id: int = None, key: str = None, _type: str = 'ana'):
        """
        获取通道信息，
        :param cfg_id: cfg文件中的通道索引号，模拟量和开关量都统一为an，默认为空，当key不为空时返回该属性所有值的列表
        :param key: 模拟量通道属性，默认为空当cfg_id为空获取所有通道的所有属性，如chid、ccbm
        :param _type: 通道类型，默认为ana表示模拟量，dig表示开关量
        :return: 当key存在时返回指定属性，当key不存在时返回通道所有属性
        """
        if cfg_id is None and key is not None:
            return self._get_key_values(key, _type)
        if cfg_id is None:
            return self._get_all_info(_type)
        if cfg_id is not None and key is not None:
            try:
                cfg_id = int(cfg_id)
            except ValueError:
                raise ValueError("cfg_an通道号必须是整数或能转换为整数的字符串")
            return self._get_specific_info(cfg_id, key, _type)

    def _get_key_values(self, key: str, _type: str = 'ana'):
        """
        根据key返回所有匹配的值
        """
        channels = self._dns if _type == 'dig' else self._ans
        if not channels:
            return []  # 明确处理self._ans为空的情况
        return [d[key] for d in channels if key in d]

    def _get_all_info(self, _type: str = 'ana'):
        """
        返回所有通道的信息
        """
        return self._dns if _type == 'dig' else self._ans

    def _get_specific_info(self, cfg_an: int, key: str, _type: str = 'ana'):
        """
        根据cfg_an和key返回特定通道的信息
        """
        channels = self._dns if _type == 'dig' else self._ans
        idx = next((i for i, d in enumerate(channels) if d.get("an") == cfg_an), None)
        if idx is None:
            raise ValueError("通道号不存在")
        specific_info = channels[idx]
        return specific_info if key is None else specific_info.get(key, None)

    def is_analog_usage(self, cfg_an: Union[int, str]) -> bool:
        """
        获取对应模拟通道是否使用
        @param cfg_an: cfg文件中的通道索引号an
        @return: 布尔值True代表使用，False代表未使用
        """
        ratio = self.get_analog_ratio(cfg_an)
        return False if ratio == 1 else True

    def get_analog_ratio(self, cfg_an: int) -> float:
        """
        获取对应模拟量通道的变比
        @param cfg_an: cfg_id: cfg文件中的通道号an
        @return: 通道变比
        """
        primary = self.get_channel_info(cfg_an, key="primary")
        secondary = self.get_channel_info(cfg_an, key="secondary")
        ratio = primary / secondary
        return 0 if cfg_an is None else ratio

    def is_primary_analog(self, cfg_an: Union[int, str]) -> bool:
        """
        判断通道数值是否是一次值
        @param cfg_an: cfg文件中的通道号an
        @return: 布尔值True代表一次值，False代表二次值
        """
        ps = self.get_channel_info(cfg_an, key="ps")
        return ps in constants.PAIMARY_SIGN

    def get_digital_channel_num(self):
        """
        获取开关量通道数
        :return: 开关量量通道数
        """
        return self._D

    def get_data_format_type(self):
        """
        获取数据格式类型和字节宽度
        :return: 数据格式类型，如：binary,ascii
        """
        ft = self._ft.upper()  # 将ft转换为大写
        if ft == "BINARY":
            return "binary", 2
        if ft == "BINARY32" or ft == "FLOAT32":
            return "binary32", 4
        if ft == "ASCII":
            return "ascii", 0
