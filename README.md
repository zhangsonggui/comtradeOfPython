# 一、 py3comtrade项目介绍

本项目是采用python解析comtrade文件，可实现CFG、DAT、DMF文件的解析、数值计算和格式另存功能。暂未对2017版本中的CFF格式文件进行解析，后续会进行补充。

本项目采用uv进行管理，也可以根据pyproject.toml中配置的依赖进行安装。

# 二、py3comtrade模块介绍

| 序号 |     模块名     | 描述                                                        |
|:--:|:-----------:|-----------------------------------------------------------|
| 1  |    model    | 配置文件类：配置文件头、通道数量、模拟量通道、开关量通道、采样点信息、采样段信息、故障时间和变比因子        | 
| 2  |   reader    | comtrade文件读取模块，可读取cfg、dat、dmf文件，返回Comtrade对象              |
| 3  | computation | 计算模块：可进行傅里叶变换、向量值计算、有效值计算、角度计算、序分量计算、相量转序分量、阻抗计算、故障零时刻计算等 | 
| 4  |    utils    | 工具模块：提供文件工具、角度计算、数据保存等工具                                  |                 

## 三、环境配置

- python版本要求3.10以上，推荐使用3.12
- 本项目采用uv进行项目管理，也可以使用其他工具进行管理，具体的依赖包见pyproject.toml

> 源代码仓库

- github仓库  https://github.com/zhangsonggui/comtradeOfPython.git
- gitee仓库  https://gitee.com/zhangsonggui/comtradeOfPython.git

### 3.1 配置模块开发环境

```shell
# 安装uv项目管理，如已安装，则跳过模块
pip install uv
# 拉取项目代码
git clone https://github.com/zhangsonggui/comtradeOfPython.git
# 进入项目目录
cd comtradeOfPython
#根据pyproject.toml创建虚拟环境，安装依赖包
uv venv

# 打包whl
uv build
```

### 3.2 模块使用

> 使用uv新建项目

```shell
    # 新建目录
    mkdir project_name
    # 指定项目使用的python版本，如果不指定，默认使用当前操作系统版本最高的python版本
    uv python pin 3.10
    # 初始化项目
    uv init
    # 安装模块，不在加版本号，默认安装最新版本
    uv add py3comtrade
    
    # 安装本地whl包
    uv pip install 本地目录\py3comtrade-4.0.5.1-py3-none-any.whl
```

> 原有系统安装依赖包

```shell
    # 使用pip安装
    pip install py3comtrade
    # 使用uv安装
    uv add py3comtrade
    # 安装本地whl包
    uv pip install 本地目录\py3comtrade-4.0.5.1-py3-none-any.whl
```

> 使用示例

```python
from py3comtrade.reader.comtrade_reader import comtrade_reader
from py3comtrade.model.type.types import ChannelType, IdxType

# comtrade路径，包含后缀名
comtrade_file_path = 'comtrade_file_path'
# 默认读取comtrade所有类型的文件，如果只读取cfg文件，可以使用read_mode参数ReadMode.CFG
record = comtrade_reader(comtrade_file_path)

# 获取变电站名称
station_name = record.header.station_name
# 获取通道对象，可以通过模拟量通道的an标识或索引顺序号获取模拟量通道对象
analog = record.get_channel_obj(1, ChannelType.ANALOG, IdxType.CFGAN)
# 根据模拟量通道获取瞬时值，默认获取改通道全部采样点的数据
record.get_analog_instant_data_range()
```

## 五、参与贡献

1. Fork 本仓库
2. 新建 Feat_xxx 分支
3. 提交代码
4. 新建 Pull Request
