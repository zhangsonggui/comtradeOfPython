from comtradeParser.ComtradeParser import ComtradeParser as cp

if __name__ == '__main__':
    file = r'data/xtz.cfg'
    ch_number = [1, 2, 3]
    record = cp(file)
    ssz = record.get_analog_ssz(ch_number, False)
    cursor_point = 0
    cycle = 1
    sample_rate = record.cfg.get_cursor_cycle_sample_num(cursor_point)
    start_point, end_point, samp_num = record.cfg.get_cursor_sample_range(cursor_point, cycle_num=cycle)
    ssz = ssz[:, start_point:end_point + 1]
    yxz = record.get_analog_yxz(ssz)
    print(f'有效值：{yxz}')
    phasor = record.get_analog_phasor(ssz)
    print(f'相量值：{phasor}')
    anagle = record.get_analog_angle(ssz)
    print(f'角度：{anagle}')
    xfl = record.get_channel_xfl_phasor(ssz)
    print(f'序分量：{xfl}')

    yxzk = record.get_analog_yxz(ch_number=ch_number, start_point=cursor_point, cycle_num=cycle)
    print(f'可变参数有效值：{yxzk}')
    xflm = record.get_channel_xfl_magnitude(ch_number=ch_number, start_point=cursor_point, cycle_num=cycle)
    print(f'可变参数模值：{xflm}')
