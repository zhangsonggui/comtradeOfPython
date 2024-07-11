[toc]

# 一、 py3comtrade项目介绍

本项目是采用python解析comtrade文件，可实现CFG、DAT、DMF文件的解析和数值计算功能。暂未对2017版本中的CFF格式文件进行解析，后续会进行补充。

本项目采用poetry进行管理，也可以根据pyproject.toml中配置的依赖进行安装。

# 二、py3comtrade模块介绍

| 序号 |     模块名     | 描述                                                     | 备注                                 |
|:--:|:-----------:|--------------------------------------------------------|------------------------------------|
| 1  |   parser    | 解析模块：可解析配置文件（cfg）、数据文件（dat）、模型文件（dmf）等                 |                                    |
| 2  |   entity    | 实体类：配置文件类（含故障头类、模拟量通道类、开关量通道类、故障时间类、采样信息类）、数据文件类、模型文件类 | 模型文件解析还未按照类文件进行解析                  |
| 3  | computation | 计算模块：可进行傅里叶变换、序分量计算、相量转序分量、阻抗计算、故障零时刻计算等               | 故障零时刻未实现                           |
| 4  |    utils    | 工具模块，提供文件工具、角度计算、数据保存等工具                               | 数据保存目前仅实现保存为ASCII格式                |
| 5  |    merge    | 合并comtrade文件                                           | 仅实现相同采样频率的多个文件合并，后续增加频率归一化和采样点裁剪功能 |

## 1.comtrade模块（parser、entity）

提供解析后的comtrade对象

> 属性

- 故障头对象（fault_header）：包含变电站名称、设备名称、录波文件版本、采样通道总数、模拟量通道数、开关量通道数、模拟量通道开始索引号、开关量通道开始索引号

-

采样信息对象（sample_info）：包含采样频率、采样段数量、各采样段信息（该段采样频率、该采样段结束位置、该采样段每周波采样点数、该采样段采样点数、该采样段开始位置、该采样段用时、该采样段结束时间）、采样点数、采样格式、采样时间因子、故障时间、模拟量每通道每采样点所占字节、开关量每通道每采样点所占字节、模拟量每通道每采样点所占用字节、每采样点总采样字节数

-

模拟量通道对象列表（analog_channels）：模拟量通道对象AnalogChannel组成，每个对象包含通道索引号、通道标识、通道相别、被监视元件、通道单位、通道增益系数、通道偏移系数、通道时滞、最大值、最小值、一次系数、二次系数、一二次标识、通道变比

- 开关量通道对象列表（digital_channels）：开关量量通道对象DigitalChannel组成，每个对象包含通道索引号、通道标识、通道相别、被监视元件、状态通道正常状态

- 模型对象（dmf）

- 模拟量数值列表（analog_values）：numpy数组，一维为通道、二维为各采样点原始采样值

- 开关量数值列表（digital_values）：numpy数组，一维为通道、二维为各采样点原始采样值

- 采样点及相对时间列表（sample_time_lists）numpy数组，一维0代表采样点号，1为相对时间、二维为各采样点原始采样值

- 发生变位的开关量列表（changed_digital_channels）：所有发生变位的开关量通道索引号dn

-

开关量初始位置和变位详情列表（digital_channels_state）：每个开关量为一个字典类型，channel代表开关量通道索引号dn、first_state初始值、change_positions为发生变化值在digital_values数组中的索引值，changes和change_positions对应的值

> 方法

- git_analog_ysz：获取指定通道、指定采样点或周波数的原始采样值。

- git_analog_ssz：获取指定通道、指定采样点或周波数的瞬时值。

- get_analog_phasor：获取指定数组或通道的的向量值。

- git_analog_yxz：获取指定通道、指定采样点或周波数的有效值。

- get_analog_angle：获取指定数组或通道的的角度。

- get_analog_xfl_phasor：获取指定数组或通道的的序分量相量值。目前仅支持三个通道的计算，待后续dmf解析完可以支持多组。

- get_analog_xfl_magnitude：获取指定数组或通道的的序分量模值。目前仅支持三个通道的计算，待后续dmf解析完可以支持多组。

> 入口

```python
from py3comtrade.comtrade import read_comtrade

# 获取comtrade对象
record = read_comtrade('cfg_path', 'dat_path', 'dmf_path')

```

可以通过 py3comtrade.comtrade或直接使用 py3comtrade.parser.comtrade_parser都可以。

## 2.计算模块（computation）

### 2.1fourier傅里叶计算

提供单个通道或多个通道的傅里叶计算，计算工频下的实部、虚部，同时提供消除直流分量的实部、虚部。

### 2.2impedance阻抗计算

计算线路阻抗

### 2.3 sequence相分量转换为序分量

提供旋转角度和矩阵计算两种方式

## 3.工具模块

### 3.1cfg_to_file

- generate_cfg_str：根据对象生成文本字符串

- cfg_to_file：cfg对象保存为cfg文件

### 3.2dat_to_file

- write_dat_ascii：生成ASCII格式dat文件
- write_dat_binary：生成binary格式dat文件
- write_dat_binary32：生成binary32格式dat文件

### 3.3file_tools

- file_finder：扫描指定目录、指定后缀的所有文件，是否递归查找
- split_path：分割文件路径为目录、文件名和后缀名
- verify_file_validity：验证文件是否存在且非空
- read_file_adaptive_encoding：尝试以GBK和UTF-8两种编码读取文件，以适应不确定的编码情况。

### 3.4math_polar_rect

## 4.merge模块

可以进行多个comtrade文件的合并，目前仅支持采样频率一致的全通道文件合并。

> TODO

- 增加采样频率归一化
- 采样点裁剪对齐
- 选择通道合并
- 修改故障头、故障时间、格式互转
- 幅值变换。。。

> 属性

- cfgs：扫描指定磁盘目录下的cfg文件，形成字典列表，每个字典包含file_name和cfg对象

> 方法

- merge_cfg_data：遍历cfgs，合并cfg文件，并输出到文件
- merge_dat_data：遍历cfgs，合并dat文件，并输出到文件

## 三、安装教程

### 3.1 Python版本要求

3.8以上推荐3.11

### 3.2 whl包安装

> 本项目采用poetry管理，建议拉取项目后先生成whl二进制安装包,在安装新建项目的python环境中

1. 克隆代码到本地
2. 进入comtradeOfPython目录
3. 安装poetry，打包项目whl包，目录为comtradeOfPython目录下dist
4. 新建项目并创建虚拟环境，在虚拟环境中安装comtradeParser包
5. 在新建项目下创建数据文件和main.py文件，直接实例化ComtradeParser类

```shell
   git clone https://github.com/zhangyongjian/comtradeOfPython.git
   cd comtradeOfPython
   pip install poetry  # 安装poetry
   python -m build  # 打包为whl包，或poetry build
   
```

### 3.3 源码安装

> 本项目为独立模块，如不对源代码进行修改，建议使用3.2whl包安装方式

1. 克隆代码到本地
2. 安装依赖
3. 在comtradeOfPython目录下创建数据文件和main.py文件，直接实例化ComtradeParser类

```shell
git clone https://github.com/zhangsonggui/comtradeOfPython.git
cd comtradeOfPython
pip install -r requirements.txt
```

### 3.4 pip仓库安装

```shell
pip install py3comtrade
```

## 四、使用说明

```python
from py3comtrade.comtrade import read_comtrade

comtrade_file_path = 'comtrade_file_path'
record = read_comtrade(comtrade_file_path)
station_name = record.fault_header.station_name
ch_numbers = [1, 2, 3, 4]
# 先获取模拟量通道对象
analog_channels = [record.cfg.get_analog_obj(i) for i in ch_numbers]
# 获取指定通道对象的二次瞬时值，可根据需要增加参数获取
ssz = record.get_analog_ssz(analog_channels)
```

## 五、参与贡献

1. Fork 本仓库
2. 新建 Feat_xxx 分支
3. 提交代码
4. 新建 Pull Request


