from comtradeParser.fault_record import FaultRecord

if __name__ == '__main__':
    # path =r'D:\Nextcloud\个人工作文档\项目管理\智能录波器实训基地建设\3-模型搭建\电网故障模型\A相瞬时接地故障(15km).gf42\Rank_00001\Run_00001'
    # fileName = '\BRK3._cfg'
    file = r'tests/data/xtz.cfg'
    # file = path+fileName
    ch_numbers = [1, 2, 3, 4]
    record = FaultRecord(file)
    ssz = record.get_analog_ssz(ch_numbers, primary=True)
    print('采样点数：', len(ssz[0]))
    print(ssz)
    # channel = record._cfg.get_channel_info(cfg_an=1)
    # print(channel)
    # ssz = record.get_analog_ssz(cfg_an)
    # print(ssz)
    # cursor_point = 0
    # cycle = 1
    # sample_rate = record._cfg.get_cursor_cycle_sample_num(cursor_point)
    # start_point, end_point, samp_num = record._cfg.get_cursor_sample_range(cursor_point, cycle_num=cycle)
    # ssz = ssz[:, start_point:end_point + 1]
    # yxz = record.get_analog_yxz(ssz)
    # print(f'有效值：{yxz}')
    # phasor = record.get_analog_phasor(ssz)
    # print(f'相量值：{phasor}')
    # anagle = record.get_analog_angle(ssz)
    # print(f'角度：{anagle}')
    # xfl = record.get_channel_xfl_phasor(ssz)
    # print(f'序分量：{xfl}')
    #
    # yxzk = record.get_analog_yxz(cfg_an=cfg_an, start_point=cursor_point, cycle_num=cycle)
    # print(f'可变参数有效值：{yxzk}')
    # xflm = record.get_channel_xfl_magnitude(cfg_an=cfg_an, start_point=cursor_point, cycle_num=cycle)
    # print(f'可变参数模值：{xflm}')
