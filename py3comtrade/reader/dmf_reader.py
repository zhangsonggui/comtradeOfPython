#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  Copyright (c) [2019] [name of copyright holder]
#  [py3comtrade] is licensed under Mulan PSL v2.
#  You can use this software according to the terms and conditions of the Mulan
#  PSL v2.
#  You may obtain a copy of Mulan PSL v2 at:
#           http://license.coscl.org.cn/MulanPSL2
#  THIS SOFTWARE IS PROVIDED ON CFGAN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY
#  KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
#  NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
#  See the Mulan PSL v2 for more details.
import os
import xml.etree.ElementTree as ET

from py3comtrade.model.channel.analog_channel import AnalogChannel, ChannelIdx
from py3comtrade.model.channel.status_channel import StatusChannel
from py3comtrade.model.dmf import DMF
from py3comtrade.model.equipment.branch import ACCBranch, ACVBranch
from py3comtrade.model.equipment.bus import Bus
from py3comtrade.model.equipment.line import Line
from py3comtrade.model.equipment.line_param import CG, MR, RX
from py3comtrade.model.equipment.transformer import Transformer, TransformerWinding, WG
from py3comtrade.model.exceptions import ComtradeDataFormatException, ComtradeFileEncodingException, \
    ComtradeFileParseException
from py3comtrade.model.type.analog_enum import (BranNum, CtDirection, Multiplier, PsType, TransWindLocation,
                                                TvInstallation, WGFlag)
from py3comtrade.model.type.digital_enum import BreakerFlag, ChannelFlag, Contact, RelayFlag, SignalType, WarningFlag


def analog_channel_parser(channel_xml) -> AnalogChannel:
    """
    解析模拟量通道
    :param channel_xml: 模拟量通道字符串
    :return 模拟量通道对象
    """
    idx_cfg = channel_xml.get('idx_cfg', None)
    idx_org = channel_xml.get('idx_org', "")
    type = channel_xml.get('type', None)
    flag = channel_xml.get('flag', None)
    freq = channel_xml.get('freq', 50)
    au = channel_xml.get('au', 1)
    bu = channel_xml.get('bu', 0)
    sIUnit = channel_xml.get('sIUnit', None)
    multiplier = channel_xml.get('multiplier', "")
    primary = channel_xml.get('primary', 1)
    secondary = channel_xml.get('secondary', 1)
    ps = channel_xml.get('ps', "")
    ph = channel_xml.get('ph', "")
    p_min = channel_xml.get('p_min', None)
    p_max = channel_xml.get('p_max', None)
    s_min = channel_xml.get('s_min', None)
    s_max = channel_xml.get('s_max', None)
    return AnalogChannel(idx_cfg=idx_cfg,
                         idx_org=idx_org,
                         type=type,
                         flag=flag,
                         freq=freq,
                         au=au,
                         bu=bu,
                         s_i_unit=sIUnit,
                         multiplier=Multiplier.from_string(multiplier, default=Multiplier.N),
                         primary=primary,
                         secondary=secondary,
                         ps=PsType.from_string(ps, default=PsType.S),
                         phase=ph,
                         p_max=p_max,
                         p_min=p_min,
                         s_max=s_max,
                         s_min=s_min)


def status_channel_parser(channel_xml) -> StatusChannel:
    """解析开关量通道"""
    idx_cfg = channel_xml.get('idx_cfg', None)
    idx_org = channel_xml.get('idx_org', "")
    signal_type_str = channel_xml.get('type', None)
    signal_type = SignalType.from_string(signal_type_str, default=SignalType.RELAY)
    flag = channel_xml.get('flag', ChannelFlag.GENERAL)
    if signal_type is SignalType.RELAY:
        flag = RelayFlag.from_string(flag, default=RelayFlag.TR)
    elif signal_type is SignalType.BREAKER:
        flag = BreakerFlag.from_string(flag, default=BreakerFlag.HWJ)
    elif signal_type is SignalType.WARNING:
        flag = WarningFlag.from_string(flag, default=WarningFlag.WARN_COMM)
    else:
        flag = ChannelFlag.GENERAL
    contact = channel_xml.get('contact', None)
    srcRef = channel_xml.get('srcRef', "")

    return StatusChannel(idx_cfg=idx_cfg, idx_org=idx_org, type=signal_type, flag=flag, reference=srcRef,
                         contact=Contact.from_string(contact, default=Contact.NORMALLY_OPEN))


def acv_branch_parser(branch_xml) -> ACVBranch:
    """解析电压分支"""
    ua_idx = branch_xml.get('ua_idx', "")
    ub_idx = branch_xml.get('ub_idx', "")
    uc_idx = branch_xml.get('uc_idx', "")
    ul_idx = branch_xml.get('ul_idx', "")
    un_idx = branch_xml.get('un_idx', "")
    return ACVBranch(ua_idx=0 if ua_idx == "" else int(ua_idx),
                     ub_idx=0 if ub_idx == "" else int(ub_idx),
                     uc_idx=0 if ub_idx == "" else int(uc_idx),
                     ul_idx=0 if ul_idx == "" else int(ul_idx),
                     un_idx=0 if un_idx == "" else int(un_idx))


def bus_parser(bus_xml, ns) -> Bus:
    """解析母线"""
    idx = bus_xml.get('idx', 1)
    bus_name = bus_xml.get('bus_name', "")
    src_ref = bus_xml.get('srcRef', "")
    v_rtg = bus_xml.get('VRtg', None)
    v_rtg_snd = bus_xml.get('VRtgSnd', None)
    v_rtg_snd_pos_str = bus_xml.get('VRtgSnd_Pos', "")
    v_rtg_snd_pos = TvInstallation.from_string(v_rtg_snd_pos_str, default=TvInstallation.BUS)
    bus_uuid = bus_xml.get('bus_uuid', "")
    bus = Bus(idx=idx, name=bus_name, reference=src_ref, v_rtg=v_rtg, v_rtg_snd=v_rtg_snd,
              v_rtg_snd_pos=v_rtg_snd_pos, bus_uuid=bus_uuid)
    bus.acv_chn = acv_branch_parser(bus_xml.find('scl:ACVChn', ns))
    for chn in bus_xml.findall('scl:AnaChn', ns):
        bus.analog_chn.append(ChannelIdx(idx_cfg=chn.get('idx_cfg', "")))
    for chn in bus_xml.findall('scl:StaChn', ns):
        bus.digital_chn.append(ChannelIdx(idx_cfg=chn.get('idx_cfg', "")))
    return bus


def acc_branch_parser(branch_xml) -> ACCBranch:
    """解析电流分支"""
    return ACCBranch(idx=branch_xml.get('bran_idx', ""),
                     ia_idx=branch_xml.get('ia_idx', ""),
                     ib_idx=branch_xml.get('ib_idx', ""),
                     ic_idx=branch_xml.get('ic_idx', ""),
                     in_idx=branch_xml.get('in_idx', ""),
                     dir=CtDirection.from_string(branch_xml.get('dir', ""), default=CtDirection.POS))


def line_parser(line_xml, ns) -> Line:
    """解析线路"""
    idx = line_xml.get('idx', 1)
    line_name = line_xml.get('line_name', "")
    bus_id = line_xml.get('bus_ID', "")
    bus_id = 0 if bus_id == "" else bus_id
    src_ref = line_xml.get('srcRef', "")
    v_rtg = line_xml.get('VRtg', "")
    v_rtg = 0.0 if v_rtg == "" else v_rtg
    a_rtg = line_xml.get('ARtg', "")
    a_rtg_snd = line_xml.get('ARtgSnd', "")
    line_len = line_xml.get('LinLen', 0.0)
    bran_num = BranNum.from_string(line_xml.get('bran_num', 1), default=BranNum.B1)
    line_uuid = line_xml.get('line_uuid', "")
    line = Line(idx=idx, name=line_name, bus_idx=bus_id, reference=src_ref, v_rtg=v_rtg, a_rtg=a_rtg,
                a_rtg_snd=a_rtg_snd, lin_len=line_len, bran_num=bran_num, line_uuid=line_uuid)
    rx = line_xml.find('scl:RX', ns)
    line.rx = RX(r1=rx.get('r1', 0.0), x1=rx.get('x1', 0.0), r0=rx.get('r0', 0.0), x0=rx.get('x0', 0.0))
    cg = line_xml.find('scl:CG', ns)
    line.cg = CG(c0=cg.get('c0', 0.0), c1=cg.get('c1', 0.0), g0=cg.get('g0', 0.0), g1=cg.get('g1', 0.0))
    mr = line_xml.find('scl:MR', ns)
    if mr:
        line.mr = MR(idx=mr.get('idx', 1), mr0=mr.get('mr0', 0.0), mx0=mr.get('mx0', 0.0))
    for acc in line_xml.findall('scl:ACC_Bran', ns):
        line.acc_bran.append(acc_branch_parser(acc))
    for chn in line_xml.findall('scl:AnaChn', ns):
        line.ana_chn.append(ChannelIdx(idx_cfg=chn.get('idx_cfg', "")))
    for chn in line_xml.findall('scl:StaChn', ns):
        line.sta_chn.append(ChannelIdx(idx_cfg=chn.get('idx_cfg', "")))
    return line


def transformer_parser(transformer_xml, ns) -> Transformer:
    idx = transformer_xml.get('idx', 1)
    tran_name = transformer_xml.get('trm_name', "")
    src_ref = transformer_xml.get('srcRef', "")
    pwr_rtg = transformer_xml.get('pwrRtg', "")
    tranformer_uuid = transformer_xml.get('transformer_uuid', "")
    tran = Transformer(idx=idx, name=tran_name, reference=src_ref, pwr_rtg=pwr_rtg, transformer_uuid=tranformer_uuid)
    for tw in transformer_xml.findall('scl:TransformerWinding', ns):
        location = TransWindLocation.from_string(tw.get('location', ""), default=TransWindLocation.HIGH)
        src_ref = tw.get('srcRef', "")
        v_rtg = tw.get('VRtg', "")
        a_rtg = tw.get('ARtg', "")
        bran_num = tw.get('bran_num', 1)
        wg = WG(angle=tw.get('angle', 0), wgroup=WGFlag.from_string(tw.get('wgroup', ""), default=WGFlag.Y))
        bus_id = tw.get('bus_ID', "")
        tfw = TransformerWinding(location=location, reference=src_ref, v_rtg=v_rtg, a_rtg=a_rtg,
                                 bran_num=bran_num, wg=wg, bus_id=bus_id)
        acv_chn = tw.find('scl:ACVChn', ns)
        tfw.acv_chn = acv_branch_parser(acv_chn)
        for chn in tw.findall('scl:ACC_Bran', ns):
            tfw.acc_bran.append(acc_branch_parser(chn))
        tran.transWinds.append(tfw)
    return tran


def dmf_parser(_file_path: str) -> DMF:
    if not os.path.exists(_file_path):
        raise ComtradeFileEncodingException(_file_path, "DMF文件找不到")
    try:
        _dmf = DMF()
        try:
            tree = ET.parse(_file_path)
        except ET.ParseError as e:
            error_msg = f"XML解析错误: {e}\n错误位置: 行 {e.lineno}, 列 {e.offset}"
            raise ComtradeFileParseException(_file_path, error_msg, e)

        root = tree.getroot()
        ns = {
            'scl': 'http://www.iec.ch/61850/2003/SCL'
        }

        try:
            _dmf.station_name = root.get('station_name', "变电站")
            _dmf.version = root.get('version', 1.0)
            _dmf.reference = root.get('reference', 0)
            _dmf.rec_dev_name = root.get('rec_dev_name', "录波器")

            for channel in root.findall('scl:AnalogChannel', ns):
                _dmf.analog_channels.append(analog_channel_parser(channel))

            for channel in root.findall('scl:StatusChannel', ns):
                _dmf.status_channels.append(status_channel_parser(channel))

            for bus in root.findall('scl:Bus', ns):
                _dmf.buses.append(bus_parser(bus, ns))

            for line in root.findall('scl:Line', ns):
                _dmf.lines.append(line_parser(line, ns))

            for tran in root.findall('scl:Transformer', ns):
                _dmf.transformers.append(transformer_parser(tran, ns))
            return _dmf
        except ComtradeDataFormatException as e:
            raise ComtradeDataFormatException(_file_path, f"解析DMF文件内容时发生错误: ", original_error=e)
    except ComtradeFileParseException as e:
        raise ComtradeFileParseException(_file_path, f"处理DMF文件时发生未知错误:", original_error=e)


if __name__ == '__main__':
    file_path = r'D:\codeArea\gitee\comtradeOfPython\tests\data\xtz.dmf'
    dmf = dmf_parser(file_path)
    bus = dmf.find_bus_by_name("220kV母线U")
    for line in dmf.lines:
        print(line.name)
