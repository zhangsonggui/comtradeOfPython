# ComtradeParser

# 一、Comtrade格式介绍

COMTRADE是IEEE标准电力系统暂态数据交换通用格式，于1991年提出，并于1999年、2008、2017年进行了修订和完善。标准为电力系统或电力系统模型采集到的暂态波形和事故数据的文件定义了一种格式。该格式意欲提供一种易于说明的数据交换通用格式。

每个COMTRADE记录有四个相关联的文件。四个文件的每一个承载着不同等级的信息。这四个文件是头文件、配置文件、数据文件和信息文件。每一组中的所有文件必须有相同有文件名，其区别只在于说明文件类型的扩展。

文件名的格式式是 **名称.扩展名** 。
- 名称部分是用以标志记录的名称（比如 FAULTI 或 TEST-2）。
- 扩展部分用以标志文件类型和作为扩展： .HDR 用于头标文件， .CFG 用于配置文件， .DAT 用于数据文件， INF 用于信息文件。其中CFG和DAT文件必须有，而INF和HDR文件是可选的。

# 二、 ComtradeParser项目介绍

本项目是采用python解析comtrade文件，可实现CFG、DAT、DMF文件的解析和数值计算功能。暂未对207版本中的CFF格式文件进行解析，后续会进行补充。
- 1.ComtradeParser主逻辑程序，加载文件实例化子模块，提供数据的解析和计算工作
- 2.cfg.CFGParser参数文件解析解析CFG文件，可单独使用，提供厂站名称、通道数量、采样点数量、模拟量和开关量通道参数，采样类型、时间获取方法。
- 3.dat.DATParser数据文件解析，解析dat文件，需要配套cfg使用，可以获取指定通道、指定采样点获取不同数据格式的模拟量原始采样值、瞬时值数据，可以获取指定通道的开关量瞬时值和发生变位的开关量列表。
- 4 dmf 模型文件解析和生成，解析dmf文件，可独立使用提供与CFG文件配套的模型数据解析，获取母线、线路、主变模型。根据cfg文件创建dmf文件，提供与cfg文件配套的模型数据解析，获取母线、线路、主变模型
- 5.computation计算类，对comtrade各类数值提供计算方法，如傅里叶变换、相量转序分量、线路阻抗等
- 6.export 数据导出模块，规划中，暂未开发

## 三、安装教程
### 3.1 Python版本要求
3.8以上推荐3.11
### 3.2 源码安装
1. 克隆代码到本地
2. 进入安装包目录找到setup.py文件
3. 执行python setup.py install进行安装
4. 安装依赖 pip install -r requirements.txt
```shell
   git clone https://github.com/zhangyongjian/comtradeOfPython.git
   cd comtradeOfPython/comtradeParser
   python setup.py install
   pip install -r requirements.txt
   ```

### 3.3 pip仓库安装

### 3.4 whl包安装

## 四、使用说明
在comtradeOfPython目录下新建一个py文件，导入ComtradeParser模块，并实例化ComtradeParser类，调用相关方法，如
```python
from ComtradeParser.ComtradeParser import ComtradeParser
cp = ComtradeParser(comtrade_file_path)  # 实例化ComtradeParser类
cp.get_station_name()  # 获取变电站名称
cp.get_analog_ssz_from_channel(1,False)  # 获取通道标识an为1的全部瞬时值二次值
```

## 五、参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request


