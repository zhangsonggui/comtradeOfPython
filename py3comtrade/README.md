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

## 1.模型（model）

提供解析后的comtrade对象、配置文件对象、数据对象

### 1.1 Comtrade对象

> 属性

- **配置信息对象（Configure）**：故障头、通道数量、模拟量通道、开关量通道、采样信息、故障时间和变比因子
- **数据数组对象（DataReader）**：采样时间数组、模拟量数据列表、开关量数据列表
- **变位开关量通道记录**：发生变位的开关量对象列表及变位采样点号和状态

> 方法

- **get_raw_by_analog_index**：根据模拟量索引位置获取原始采样值，返回numpy数组。
- **get_raws_by_analog_index**:根据模拟量所以你位置数组获取原始采样值，返回numpy数组。
- **get_instant_by_analog**：获取指定单个通道、指定采样点或周波数的瞬时值，返回numpy数组。
- **get_instants_by_analog**：获取指定多个通道、指定采样点或周波数的瞬时值，返回numpy数组。
- **get_instant_samples_by_segment**：获取指定通道、指定采样段的瞬时值，返回numpy数组。

## 2. 读取模块（reader）

根据文件名读取comtrade文件，返回Comtrade对象，具体子模块如下：

| 序号 |       文件名       |                 方法名                 |                 描述                  |
|:--:|:---------------:|:-----------------------------------:|:-----------------------------------:|
| 1  | comtrade_reader |           comtrade_reader           | 根据文件名和读取方式读取comtrade文件，返回Comtrade对象 |
| 2  | comtrade_reader | get_files_with_different_extensions |        根据文件名获取同名所有文件，返回文件列表。        |
| 3  |  config_reader  |            config_reader            |       根据文件名获取configuration对象        |
| 4  |   dat_reader    |             DataReader              |   根据文件名和读取方式读取dat文件，返回Comtrade对象    |

## 3.数值计算模块（computation）

### 3.1 单通道计算类（calcius）

通过传入一个或一个半周波的瞬时值数据，可进行快速傅里叶计算，提供向量值（复数形式）、有效值、角度等数值，同时提供消除直流分量的向量值复数（实部、虚部）。

### 3.2 序分量计算模块（sequence）

通过传入一组通道向量值，计算正序、负序、零序分量

### 3.3 impedance阻抗计算

计算线路阻抗

### 3.4 功率计算模块（power）

待完成



## 4. 故障分析模块

提供故障时刻分析、保护动作行为分析等。

## 5.工具模块

### 5.1cfg_to_file

- generate_cfg_str：根据对象生成文本字符串

- cfg_to_file：cfg对象保存为cfg文件

### 5.2dat_to_file

- write_dat_ascii：生成ASCII格式dat文件
- write_dat_binary：生成binary格式dat文件
- write_dat_binary32：生成binary32格式dat文件

### 5.3file_tools

- file_finder：扫描指定目录、指定后缀的所有文件，是否递归查找
- split_path：分割文件路径为目录、文件名和后缀名
- verify_file_validity：验证文件是否存在且非空
- read_file_adaptive_encoding：尝试以GBK和UTF-8两种编码读取文件，以适应不确定的编码情况。

## 三、使用教程
- python版本要求3.9以上，推荐使用3.11
- 本项目采用uv进行项目管理，也可以使用其他工具进行管理，具体的依赖包见pyproject.toml

> 获取源代码
 - github仓库  https://github.com/zhangsonggui/comtradeOfPython.git
 - gitee仓库  https://gitee.com/zhangsonggui/comtradeOfPython.git
> 获取安装包

```shell
    pip install py3comtrade
```


> 使用示例

```python
from py3comtrade.reader.comtrade_reader import comtrade_reader

# 获取comtrade对象
comtrade_file_path = 'comtrade_file_path'
# 默认读取comtrade所有类型的文件，如果只读取cfg文件，可以使用read_mode参数ReadMode.CFG
record = comtrade_reader(comtrade_file_path)

# 获取变电站名称
station_name = record.cfg.header.station_name
# cfg为Configura对象，具体的方法可以查看帮助文档
# 获取通道对象，可以通过模拟量通道的an标识或索引顺序号获取模拟量通道对象
analog = record.cfg.get_analog_by_an(1)
# 根据模拟量通道获取瞬时值，默认获取改通道全部采样点的数据
record.get_instant_by_analog(analog)
```

## 五、参与贡献

1. Fork 本仓库
2. 新建 Feat_xxx 分支
3. 提交代码
4. 新建 Pull Request
