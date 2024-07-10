# ComtradeParser

# 一、Comtrade格式介绍

COMTRADE是IEEE标准电力系统暂态数据交换通用格式，于1991年提出，并于1999年、2008、2017年进行了修订和完善。标准为电力系统或电力系统模型采集到的暂态波形和事故数据的文件定义了一种格式。该格式意欲提供一种易于说明的数据交换通用格式。

每个COMTRADE记录有四个相关联的文件。四个文件的每一个承载着不同等级的信息。这四个文件是头文件、配置文件、数据文件和信息文件。每一组中的所有文件必须有相同有文件名，其区别只在于说明文件类型的扩展。

文件名的格式式是 **名称.扩展名** 。

- 名称部分是用以标志记录的名称（比如 FAULTI 或 TEST-2）。
- 扩展部分用以标志文件类型和作为扩展： .HDR 用于头标文件， .CFG 用于配置文件， .DAT 用于数据文件， INF
  用于信息文件。其中CFG和DAT文件必须有，而INF和HDR文件是可选的。

# 二、 ComtradeParser项目介绍

本项目是采用python解析comtrade文件，可实现CFG、DAT、DMF文件的解析和数值计算功能。暂未对2017版本中的CFF格式文件进行解析，后续会进行补充。

## 1.FaultRecord

主逻辑程序，加载文件实例化子模块，提供数据的解析和计算工作，主要有以下功能：

- 获取单个通道或指定通道的**模拟量原始采样值**：
- 获取单个通道或指定通道的**模拟量瞬时值**
- 获取单个通道或指定通道游标位置的**模拟量有效值**
- 获取单个通道或指定通道游标位置的**角度**
- 获取通道分组的**序分量**
- 获取通道分组**相量**
- 获取单个通道或指定通道的**开关量瞬时值**
- 获取单个通道或指定通道的**开关量变位**
- 获取发生**变位的开关量列表**

## 2.cfg模块

### 2.1 解析模块

解析cfg文件，包含头部信息、通道信息、开关量信息、采样信息四个部分

- **FaultHeader类**提供cfg前两行的信息，包含厂站名称、设备标识、文件版本、通道总数、模拟量通道数量和开关量通道数量
- **AnalogChannel类**提供模拟量通道信息，包含通道标识、通道名称等信息。
- **DigitalChannel类**提供开关量通道信息，包含通道标识、通道名称等信息。
- **SampleInfo类**提供采样频率、采样段数、采样点数、故障时间、采样格式等信息

### 2.2 模型模块

**CfgParser类**提供cfg文件中各项属性和方法的调用，获取游标位置的采样范围、所在采样段、通道属性等

- **get_channel_info**获取通道属性
- **get_cursor_sample_rage**以游标所在采样点获取采样点范围
- **get_cursor_sample_segment**获取游标所在采样点所在采样段
- **get_cursor_cycle_sample_range**获取游标位置指定周波的采样点范围

### 2.3 文件保存

- **cfg_to_file**提供根据cfg模型写入文件的操作
- **generate_cfg_str**提供根据cfg模型生成文本

## 3.dat模块

### 3.1 解析模块

解析不同格式的dat文件，需要配套cfg使用，可指定通道、指定采样点获取原始采样值、瞬时值
对于开关量不同数据格式的模拟量原始采样值、瞬时值数据，可以获取指定通道的开关量瞬时值和发生变位的开关量列表。

### 3.2 数据模块

- 获取单个**模拟量通道原始值**
- 获取单个**模拟量通道瞬时值**
- 获取单个**开关量通道瞬时值**
- 获取发生**变位开关量列表**

### 3.3 文件保存

- 保存为ASCII码格式文件
- 保存为二进制格式文件（未实现）
- 保存为Excel文件（未实现）

## 4 dmf模块

### 4.1 解析模块

- DmfParser类解析dmf文件，可独立使用提供与CFG文件配套的模型数据解析，获取母线、线路、主变模型
- CfgToDmf类根据cfg文件创建dmf文件，提供与cfg文件配套的模型数据解析，获取母线、线路、主变模型
- ChannelGroupParser类将通道转换成线路、主变、母线分组模型

### 4.2 模型模块

- 获取线路模型
- 获取主变模型
- 获取母线模型
-

### 4.3 文件保存

将模型保存为DMF文件

## 5.计算模块

计算模块，对comtrade各类数值提供计算方法

### 5.1 fourier

提供傅里叶变换

### 5.3 sequence

序分量计算，相量转序分量

### 5.4 impedance

通过两侧电压电流计算线路阻抗阻抗

### 5.5 zerolocation 故障时刻计算，规划中，暂未开发

计算故障点零时刻

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
git clone https://github.com/zhangyongjian/comtradeOfPython.git
cd comtradeOfPython
pip install -r requirements.txt
```

### 3.4 pip仓库安装

pypi仓库暂时禁止新建包，暂时无法使用pip安装

## 四、使用说明

```python
from py3comtrade.comtrade import Comtrade

comtrade_file_path = 'comtrade_file_path'
fr = Comtrade(comtrade_file_path)
station = fr.cfg.station_name
ssz = fr.get_analog_ssz(1, False, 0, -1)  # 获取通道标识an为1的全部二次瞬时值
```

## 五、参与贡献

1. Fork 本仓库
2. 新建 Feat_xxx 分支
3. 提交代码
4. 新建 Pull Request


