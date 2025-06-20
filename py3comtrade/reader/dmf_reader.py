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
import xml.etree.ElementTree as ET

from py3comtrade.model import AnalogChannel, ChannelIdx
from py3comtrade.model import DMF
from py3comtrade.model import StatusChannel
from py3comtrade.model.bus import Bus
from py3comtrade.model.line import Line
from py3comtrade.model.primary_equipments import ACVBranch, CG, MR, RX, ACCBranch
from py3comtrade.model.transformer import Transformer, WG, TransformerWinding
from py3comtrade.model.type import BreakerFlag, ChannelFlag, Contact, PsType, RelayFlag, SignalType, WarningFlag
from py3comtrade.model.type.analog_enum import Multiplier, TvInstallation, BranNum, CtDirection, TransWindLocation, \
    WGFlag


def channel_parser(channel_xml):
    pass


def dmf_parser(file_path) -> DMF:
    dmf = DMF()
    tree = ET.parse(file_path)
    root = tree.getroot()
    ns = {
        'scl': 'http://www.iec.ch/61850/2003/SCL'
    }
    dmf.station_name = root.get('station_name', "变电站")
    dmf.version = root.get('version', 1.0)
    dmf.reference = root.get('reference', 0)
    dmf.rec_dev_name = root.get('rec_dev_name', "录波器")

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
        v_rtg_snd_pos_str = bus.get('VRtgSnd_Pos', "")
        v_rtg_snd_pos = TvInstallation.from_string(v_rtg_snd_pos_str, default=TvInstallation.BUS)
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
            b.digital_chn.append(ChannelIdx(idx_cfg=chn.get('idx_cfg', "")))
        dmf.buses.append(b)

    for line in root.findall('scl:Line', ns):
        idx = line.get('idx', 1)
        line_name = line.get('line_name', "")
        bus_id = line.get('bus_ID', "")
        src_ref = line.get('srcRef', "")
        v_rtg = line.get('VRtg', "")
        a_rtg = line.get('ARtg', "")
        a_rtg_snd = line.get('ARtgSnd', "")
        line_len = line.get('LinLen', 0.0)
        bran_num = BranNum.from_string(line.get('bran_num', 1), default=BranNum.B1)
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
        for acc in line.findall('scl:ACC_Bran', ns):
            l.acc_bran.append(ACCBranch(idx=acc.get('idx', 1),
                                        ia_idx=acc.get('ia_idx', ""),
                                        ib_idx=acc.get('ib_idx', ""),
                                        ic_idx=acc.get('ic_idx', ""),
                                        in_idx=acc.get('in_idx', ""),
                                        dir=CtDirection.from_string(acc.get('dir', ""), default=CtDirection.POS)))
        for chn in line.findall('scl:AnaChn', ns):
            l.ana_chn.append(ChannelIdx(idx_cfg=chn.get('idx_cfg', "")))
        for chn in line.findall('scl:StaChn', ns):
            l.sta_chn.append(ChannelIdx(idx_cfg=chn.get('idx_cfg', "")))
        dmf.lines.append(l)

    for tran in root.findall('scl:Transformer', ns):
        idx = tran.get('idx', 1)
        tran_name = tran.get('trm_name', "")
        src_ref = tran.get('srcRef', "")
        pwr_rtg = tran.get('pwrRtg', "")
        tranformer_uuid = tran.get('transformer_uuid', "")
        t = Transformer(idx=idx, name=tran_name, reference=src_ref, pwr_rtg=pwr_rtg,
                        transformer_uuid=tranformer_uuid)
        for tw in tran.findall('scl:TransformerWinding', ns):
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
            tfw.acv_chn = ACVBranch(ua_idx=acv_chn.get('ua_idx', ""),
                                    ub_idx=acv_chn.get('ub_idx', ""),
                                    uc_idx=acv_chn.get('uc_idx', ""),
                                    un_idx=acv_chn.get('un_idx', ""),
                                    ul_idx=acv_chn.get('ul_idx', ""))
            for chn in tw.findall('scl:ACC_Bran', ns):
                tfw.acc_bran.append(ACCBranch(idx=chn.get('idx', 1),
                                              ia_idx=chn.get('ia_idx', ""),
                                              ib_idx=chn.get('ib_idx', ""),
                                              ic_idx=chn.get('ic_idx', ""),
                                              in_idx=chn.get('in_idx', ""),
                                              dir=CtDirection.from_string(chn.get('dir', ""), default=CtDirection.POS)))
            t.transWinds.append(tfw)
        dmf.transformers.append(t)
    return dmf


if __name__ == '__main__':
    file_path = r'D:\codeArea\gitee\comtradeOfPython\tests\data\hjz.dmf'
    dmf = dmf_parser(file_path)
    for line in dmf.lines:
        print(line.name)
