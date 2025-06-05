import numpy as np
import pandas as pd

from py3comtrade.reader.config_reader import config_reader

if __name__ == "__main__":
    # file_path = r'D:\codeArea\gitee\comtradeOfPython\tests\data\xtz.cfg'
    # comtrade = comtrade_reader(file_path)
    # comtrade.analyze_digital_change_status()
    #
    # cfg_content = generate_cfg_str(comtrade.configure)
    # configure_to_file(comtrade.configure, "./test1.cfg")
    # instant_analog = comtrade.get_instant_by_multi_analog()
    # instant_digital = comtrade.get_instant_by_multi_digital()
    # data = np_concatenate(comtrade.data.sample_time.T,instant_analog,instant_digital)
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
    cfg_file = r"D:\codeArea\gitee\comtradeOfPython\tests\data\D51_RCD_2346_20150917_105253_065_F.cfg"
    dat_file = r"D:\codeArea\gitee\comtradeOfPython\tests\data\D51_RCD_2346_20150917_105253_065_F.dat"
    cfg = config_reader(cfg_file)
    count = cfg.sample.count
    data = {
        "index": np.zeros(count, dtype=np.int32),
        "time": np.zeros(count, dtype=np.int32),
    }

    for analog in cfg.analogs:
        data[analog.name] = np.zeros(count, dtype=np.float32)

    for digital in cfg.digitals:
        data[digital.name] = np.zeros(count, dtype=np.int32)
    df = pd.DataFrame(data)
    with open(dat_file, 'r') as f:
        content = pd.read_csv(f, header=None)
        df = content
    print(df)
