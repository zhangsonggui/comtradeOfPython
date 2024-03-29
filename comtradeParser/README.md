# ComtradeParser

# 一、Comtrade格式介绍

COMTRADE是IEEE标准电力系统暂态数据交换通用格式，于1991年提出，并于1999年、2008、2017年进行了修订和完善。标准为电力系统或电力系统模型采集到的暂态波形和事故数据的文件定义了一种格式。该格式意欲提供一种易于说明的数据交换通用格式。

每个COMTRADE记录有四个相关联的文件。四个文件的每一个承载着不同等级的信息。这四个文件是头文件、配置文件、数据文件和信息文件。每一组中的所有文件必须有相同有文件名，其区别只在于说明文件类型的扩展。

文件名的格式式是 **名称.扩展名** 。
- 名称部分是用以标志记录的名称（比如 FAULTI 或 TEST-2）。
- 扩展部分用以标志文件类型和作为扩展： .HDR 用于头标文件， .CFG 用于配置文件， .DAT 用于数据文件， INF 用于信息文件。其中CFG和DAT文件必须有，而INF和HDR文件是可选的。

# 二、 ComtradeParser项目介绍

本项目是采用python解析comtrade文件，可实现CFG、DAT、DMF文件的解析和数值计算功能。暂未对2017版本中的CFF格式文件进行解析，后续会进行补充。

## 1.ComtradeParser

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

## 2.cfg.CFGParser参数文件解析

解析CFG文件，可单独使用，提供厂站名称、通道数量、采样点数量、模拟量和开关量通道参数，采样类型、时间获取方法。
- 获取采样范围：根据游标位置采样点、结束采样点、采样周波数和取值模式，提供采样范围对应的开始、结束采样点和对应的采样点总数，默认获取到全部采样点，当采样周波数不为空时，根据游标采样点对应的采样频率计算结束采样点
- 获取采样段信息：根据游标位置采样点判断所在的采样段及该段对应的采样频率，并可以计算两个采样点之间的采样段及每段采样点数。
- 可根据采样通道列表、通道属性和通道类型获取指定的通信息，如可以获取全部的模拟量通道信息，可以获取全部的模拟量通道名称或指定通道的模拟量通道名称。
- 提供采样点频率是否一致的判断


## 3.dat.DATParser数据文件解析

解析dat文件，需要配套cfg使用，可以获取指定通道、指定采样点获取不同数据格式的模拟量原始采样值、瞬时值数据，可以获取指定通道的开关量瞬时值和发生变位的开关量列表。
- 获取单个**模拟量通道原始值**
- 获取单个**模拟量通道瞬时值**
- 获取单个**开关量通道瞬时值**
- 获取发生**变位开关量列表**

## 4 dmf 模型文件解析和生成
### 4.1 dmf.DMFParser

解析dmf文件，可独立使用提供与CFG文件配套的模型数据解析，获取母线、线路、主变模型

### 4.2. dmf.CFG2DMF

根据cfg文件创建dmf文件，提供与cfg文件配套的模型数据解析，获取母线、线路、主变模型

### 4.3 dmf.ChannelGroupParser

提供线路、主变、母线分组模型信息

## 5.computation计算类

计算模块，对comtrade各类数值提供计算方法

### 5.1 fourier

提供傅里叶变换

### 5.3 sequence

序分量计算，相量转序分量

### 5.4 impedance

通过两侧电压电流计算线路阻抗阻抗

### 5.5 zerolocation 故障时刻计算，规划中，暂未开发

计算故障点零时刻

## 6.export 数据导出模块，规划中，暂未开发

导出文件模块

### 6.1 tocsv

导出CSV文件，行是采样点，列是通道标识

### 6.2 toexcel

导出Excel文件，行是采样点，列是通道标识

## 三、安装教程
### 3.1 Python版本要求
3.8以上推荐3.11
### 3.2 whl包安装
>本项目采用poetry管理，建议拉取项目后先生成whl二进制安装包,在安装新建项目的python环境中
1. 克隆代码到本地
2. 进入comtradeOfPython目录
3. 安装poetry，打包项目whl包,目录为comtradeOfPython目录下dist
4. 新建项目并创建虚拟环境，在虚拟环境中安装comtradeParser包
5. 在新建项目下创建数据文件和main.py文件，直接实例化ComtradeParser类
```shell
   git clone https://github.com/zhangyongjian/comtradeOfPython.git
   cd comtradeOfPython
   pip install poetry  # 安装poetry
   python -m build  # 打包为whl包
   ```
### 3.3 源码安装
>本项目为独立模块，如不对源代码进行修改，建议使用3.2whl包安装方式

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

1. from ComtradeParser import ComtradeParser as cp
2. cp = cp(comtrade_file_path)
3. cp.get_station_name()  # 获取变电站名称
4. cp.get_analog_ssz_from_channel(1,False,0,-1)获取通道标识an为1的全部瞬时值二次值

## 五、参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request


