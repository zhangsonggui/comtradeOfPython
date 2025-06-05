import time

from py3comtrade.reader.comtrade_reader import comtrade_reader

if __name__ == '__main__':
    file_path = r'D:\codeArea\gitee\comtradeOfPython\tests\data\hjz.cfg'
    start_time = time.time()
    comtrade = comtrade_reader(file_path)
    comtrade.analyze_digital_change_status()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Execution time: {elapsed_time:.2f} seconds,{elapsed_time / 60:.2f}")
    dc = comtrade.digital_change
    print(dc)
    # sszs = comtrade.get_instant_by_multi_analog()

    # cfg_content = generate_cfg_str(comtrade.configure)
    # configure_to_file(comtrade.configure, "./test1.cfg")
    # sample_time = comtrade.data.sample_time.T
    # analog_values = comtrade.data.analog_value.T
    # digital_values = comtrade.data.digital_value.T
    # ssz = comtrade.get_instant_by_multi_analog()
    # data = np_concatenate(comtrade.configure,comtrade.data.sample_time,comtrade.data.analog_value,comtrade.data.digital_value)
    # data_to_ascii(comtrade.configure,data, "./test1.dat")
    # data_to_ascii_file(comtrade.configure, sample_time, analog_values,digital_values, "./test.dat")
    # for ssz in sszs:
    #     print(ssz)
    # fig,axes = plt.subplots(nrows=sszs.shape[0],ncols=1,figsize=(8,6),sharex=True)
    # for i,ax in enumerate(axes):
    #     ax.plot(sszs[i, :])
    #     ax.set_ylabel(comtrade.configure.analogs[i].name)
    #
    # plt.tight_layout()
    # plt.show()
