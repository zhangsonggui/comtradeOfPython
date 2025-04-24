[toc]

# 零、更新情况

这是本项目的第三个版本，在学习过程中发现之前数据读取冗余，且面向对象处理较差，通过这段时间的学习，对模块进行重新设计，版本向前不兼容，给您造成的不便之处，敬请谅解。

# 一、 py3comtrade项目介绍

本项目是采用python解析comtrade文件，可实现CFG、DAT、DMF文件的解析和数值计算功能。暂未对2017版本中的CFF格式文件进行解析，后续会进行补充。

本项目采用poetry进行管理，也可以根据pyproject.toml中配置的依赖进行安装。

# 二、py3comtrade模块介绍

| 序号 |     模块名     | 描述                                                        |
|:--:|:-----------:|-----------------------------------------------------------|
| 1  |    model    | 配置文件类：配置文件头、通道数量、模拟量通道、开关量通道、采样点信息、采样段信息、故障时间和变比因子        | 
| 2  |   reader    | comtrade文件读取模块，可读取cfg、dat、dmf文件，返回Comtrade对象              |
| 3  | computation | 计算模块：可进行傅里叶变换、向量值计算、有效值计算、角度计算、序分量计算、相量转序分量、阻抗计算、故障零时刻计算等 | 
| 4  |    utils    | 工具模块，提供文件工具、角度计算、数据保存等工具                                  |                 
| 5  |    merge    | 合并comtrade文件，仅实现相同采样频率的多个文件合并，后续增加频率归一化和采样点裁剪功            |  

## 1.comtrade读取模块（comtrade_reader）

提供解析后的comtrade对象

> 属性

- **配置信息对象（Configure）**：故障头、通道数量、模拟量通道、开关量通道、采样信息、故障时间和变比因子

- **数据数组对象（DataReader）**：采样时间数组、模拟量数据列表、开关量数据列表

> 方法

- **read**：初始化comtrade对象，根据读取文件参数解析解析cfg、dat、dmf文件，返回Comtrade对象

- **get_raw_samples_by_index**：获取指定通道、指定采样点的原始采样值，返回numpy数组。

- **get_instant_samples_by_analog**：获取指定单个通道、指定采样点或周波数的瞬时值，返回numpy数组。

- **get_instant_samples_by_analogs**：获取指定多个通道、指定采样点或周波数的瞬时值，返回numpy数组。

- **get_instant_samples_by_segment**：获取指定通道、指定采样段的瞬时值，返回numpy数组。

- **save**：将comtrade数据保存为二进制、文本、CSV、Excel等格式文件

## 2.数值计算模块（computation）

### 2.1 单通道计算类（calcius）

通过传入一个或一个半周波的瞬时值数据，可进行快速傅里叶计算，提供向量值（复数形式）、有效值、角度等数值，同时提供消除直流分量的向量值复数（实部、虚部）。

### 2.2 序分量计算模块（sequence）

通过传入一组通道向量值，计算正序、负序、零序分量

### 2.3 impedance阻抗计算

计算线路阻抗

### 2.4 功率计算模块（power）

待完成

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

## 4. 故障分析模块

提供故障时刻分析、保护动作行为分析等。

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

> 使用示例

```python
from py3comtrade.model.comtrade import Comtrade
from py3comtrade.model.comtrade import ReadMode

# 获取comtrade对象
comtrade_file_path = 'comtrade_file_path'
record = Comtrade(comtrade_file_path)
# 读取数据
record.read(read_mode=ReadMode.FULL)
# 获取变电站名称
station_name = record.cfg.header.station_name
# cfg为Configura对象，具体的方法可以查看帮助文档
# 获取通道对象，可以通过模拟量通道的an标识或索引顺序号获取模拟量通道对象
analog = record.cfg.get_analog_by_an(1)
# 根据模拟量通道获取瞬时值，默认获取改通道全部采样点的数据
record.get_instant_samples_by_analog(analog)
```

## 五、参与贡献

1. Fork 本仓库
2. 新建 Feat_xxx 分支
3. 提交代码
4. 新建 Pull Request


