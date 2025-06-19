#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  Copyright (c) [2019] [name of copyright holder]
#  [py3comtrade] is licensed under Mulan PSL v2.
#  You can use this software according to the terms and conditions of the Mulan
#  PSL v2.
#  You may obtain a copy of Mulan PSL v2 at:
#           http://license.coscl.org.cn/MulanPSL2
#  THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY
#  KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
#  NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
#  See the Mulan PSL v2 for more details.
from py3comtrade.model import AnalogChannel, ChannelIdx
from py3comtrade.model import StatusChannel
from py3comtrade.model import DMF
import xml.etree.ElementTree as ET

from py3comtrade.model.bus import Bus
from py3comtrade.model.line import Line
from py3comtrade.model.primary_equipments import ACCBranch, ACVBranch, CG, MR, RX
from py3comtrade.model.type import BreakerFlag, ChannelFlag, Contact, PsType, RelayFlag, SignalType, WarningFlag
from py3comtrade.model.type.analog_enum import CtDirection, Multiplier


def dmf_parser(file_path) -> DMF:
    dmf = DMF()
    tree = ET.parse(file_path)
    root = tree.getroot()
    ns = {
        'scl': 'http://www.iec.ch/61850/2003/SCL'
    }
    for channel in root.findall('scl:AnalogChannel', ns):
        idx_cfg = channel.get('idx_cfg', None)
        idx_org = channel.get('idx_org', "")
        type = channel.get('type', None)
        flag = channel.get('flag', None)
        freq = channel.get('freq', 50)
        au = channel.get('au', 1)
        bu = channel.get('bu', 0)
        sIUnit = channel.get('sIUnit', None)
        multiplier = channel.get('multiplier', "")
        primary = channel.get('primary', 1)
        secondary = channel.get('secondary', 1)
        ps = channel.get('ps', "")
        ph = channel.get('ph', "")
        p_min = channel.get('p_min', None)
        p_max = channel.get('p_max', None)
        s_min = channel.get('s_min', None)
        s_max = channel.get('s_max', None)
        ac = AnalogChannel(idx_cfg=idx_cfg,
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

        dmf.analog_channels.append(ac)

    for channel in root.findall('scl:StatusChannel', ns):
        idx_cfg = channel.get('idx_cfg', None)
        idx_org = channel.get('idx_org', "")
        signal_type_str = channel.get('type', None)
        signal_type = SignalType.from_string(signal_type_str, default=SignalType.RELAY)
        flag = channel.get('flag', ChannelFlag.GENERAL)
        if signal_type is SignalType.RELAY:
            flag = RelayFlag.from_string(flag, default=RelayFlag.TR)
        elif signal_type is SignalType.BREAKER:
            flag = BreakerFlag.from_string(flag, default=BreakerFlag.HWJ)
        elif signal_type is SignalType.WARNING:
            flag = WarningFlag.from_string(flag, default=WarningFlag.WARN_COMM)
        else:
            flag = ChannelFlag.GENERAL
        contact = channel.get('contact', None)
        srcRef = channel.get('srcRef', "")

        sc = StatusChannel(idx_cfg=idx_cfg,
                           idx_org=idx_org,
                           type=signal_type,
                           flag=flag,
                           contact=Contact.from_string(contact, default=Contact.NORMALLY_OPEN),
                           reference=srcRef)
        dmf.status_channels.append(sc)

    for bus in root.findall('scl:Bus', ns):
        idx = bus.get('idx', 1)
        bus_name = bus.get('bus_name', "")
        src_ref = bus.get('srcRef', "")
        v_rtg = bus.get('VRtg', None)
        v_rtg_snd = bus.get('VRtgSnd', None)
        v_rtg_snd_pos = bus.get('VRtgSnd_Pos', "")
        bus_uuid = bus.get('bus_uuid', "")
        b = Bus(idx=idx, name=bus_name, reference=src_ref, v_rtg=v_rtg, v_rtg_snd=v_rtg_snd,
                v_rtg_snd_pos=v_rtg_snd_pos, bus_uuid=bus_uuid)
        acv_chn = bus.find('scl:ACVChn', ns)
        b.acv_chn = ACVBranch(ua_idx=acv_chn.get('ua_idx', ""),
                              ub_idx=acv_chn.get('ub_idx', ""),
                              uc_idx=acv_chn.get('uc_idx', ""),
                              un_idx=acv_chn.get('un_idx', ""),
                              ul_idx=acv_chn.get('ul_idx', ""))
        for chn in bus.findall('scl:AnaChn', ns):
            b.analog_chn.append(ChannelIdx(idx_cfg=chn.get('idx_cfg', "")))
        for chn in bus.findall('scl:StaChn', ns):
            chn_idx = chn.get('idx', "")
            b.digital_chn.append(ChannelIdx(idx_cfg=chn_idx))

        dmf.buses.append(b)
    for line in root.findall('scl:Line', ns):
        idx = line.get('idx', 1)
        line_name = line.get('line_name', "")
        bus_id = line.get('bus_id', "")
        src_ref = line.get('srcRef', "")
        v_rtg = line.get('VRtg', "")
        a_rtg = line.get('ARtg', "")
        a_rtg_snd = line.get('ARtgSnd', "")
        line_len = line.get('LinLen', 0.0)
        bran_num = line.get('bran_num', 1)
        line_uuid = line.get('line_uuid', "")
        l = Line(idx=idx, name=line_name, bus_idx=bus_id, reference=src_ref, v_rtg=v_rtg, a_rtg=a_rtg,
                 a_rtg_snd=a_rtg_snd, lin_len=line_len, bran_num=bran_num, line_uuid=line_uuid)
        rx = line.find('scl:RX', ns)
        l.rx = RX(r1=rx.get('r1', 0.0),
                  x1=rx.get('x1', 0.0),
                  r0=rx.get('r0', 0.0),
                  x0=rx.get('x0', 0.0))
        cg = line.find('scl:CG', ns)
        l.cg = CG(c0=cg.get('c0', 0.0),
                  c1=cg.get('c1', 0.0),
                  g0=cg.get('g0', 0.0),
                  g1=cg.get('g1', 0.0))
        mr = line.find('scl:MR', ns)
        l.mr = MR(idx=mr.get('idx', 1),
                  mr0=mr.get('mr0', 0.0),
                  mx0=mr.get('mx0', 0.0))
        # for acc in line.findall('scl:ACC_Bran', ns):
        #     l.acc_bran.append(ACCBranch(idx=acc.get('idx', 1),
        #                                 ia_idx=acc.get('ia_idx', ""),
        #                                 ib_idx=acc.get('ib_idx', ""),
        #                                 ic_idx=acc.get('ic_idx', ""),
        #                                 in_idx=acc.get('in_idx', ""),
        #                                 dir=CtDirection.from_string(acc.get('dir', ""), default=CtDirection.POS)))
        # for chn in line.findall('scl:AnaChn', ns):
        #     l.ana_chn.append(ChannelIdx(idx_cfg=chn.get('idx_cfg', "")))
        # for chn in line.findall('scl:StaChn', ns):
        #     l.sta_chn.append(ChannelIdx(idx_cfg=chn.get('idx_cfg', "")))
        # dmf.lines.append(l)
    return dmf


if __name__ == '__main__':
    file_path = r'D:\codeArea\gitee\comtradeOfPython\tests\data\xtz.dmf'
    dmf = dmf_parser(file_path)
