[toc]

# ComtradeParser

# 一、Comtrade格式介绍

COMTRADE是IEEE标准电力系统暂态数据交换通用格式，于1991年提出，并于1999年、2008、2017年进行了修订和完善。标准为电力系统或电力系统模型采集到的暂态波形和事故数据的文件定义了一种格式。该格式意欲提供一种易于说明的数据交换通用格式。

每个COMTRADE记录有四个相关联的文件。四个文件的每一个承载着不同等级的信息。这四个文件是头文件、配置文件、数据文件和信息文件。每一组中的所有文件必须有相同有文件名，其区别只在于说明文件类型的扩展。

文件名的格式式是 **名称.扩展名** 。

- 名称部分是用以标志记录的名称（比如 FAULTI 或 TEST-2）。
- 扩展部分用以标志文件类型和作为扩展： .HDR 用于头标文件， .CFG 用于配置文件， .DAT 用于数据文件， INF
  用于信息文件。其中CFG和DAT文件必须有，而INF和HDR文件是可选的。

# 二、 py3comtrade项目介绍

本项目是采用python3解析comtrade文件，可实现CFG、DAT、DMF文件的解析和数值计算功能。暂未对2017版本中的CFF格式文件进行解析，后续会进行补充。

- 获取单个通道或指定通道的**模拟量原始采样值**：
- 获取单个通道或指定通道的**模拟量瞬时值**
- 获取单个通道或指定通道游标位置的**模拟量有效值**
- 获取单个通道或指定通道游标位置的**角度**
- 获取通道分组的**序分量**
- 获取通道分组**相量**
- 获取单个通道或指定通道的**开关量瞬时值**
- 获取单个通道或指定通道的**开关量变位**
- 获取发生**变位的开关量列表**

# 三、安装教程

## 3.1 Python版本要求

3.9以上推荐3.11

## 3.2 whl包安装

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

## 3.3 源码安装

> 本项目为独立模块，如不对源代码进行修改，建议使用3.2whl包安装方式

1. 克隆代码到本地
2. 安装依赖
3. 在comtradeOfPython目录下创建数据文件和main.py文件，直接实例化ComtradeParser类

```shell
git clone https://github.com/zhangyongjian/comtradeOfPython.git
cd comtradeOfPython
pip install -r requirements.txt
```

## 3.4 pip仓库安装

```shell
pip install py3comtrade
```

# 四、使用说明

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

# 五、参与贡献

1. Fork 本仓库
2. 新建 Feat_xxx 分支
3. 提交代码
4. 新建 Pull Request


