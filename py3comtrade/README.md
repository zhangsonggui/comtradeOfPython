# 一、 py3comtrade项目介绍

本项目是采用python解析comtrade文件，可实现CFG、DAT、DMF文件的解析和数值计算功能。暂未对2017版本中的CFF格式文件进行解析，后续会进行补充。

本项目采用uv进行管理，也可以根据pyproject.toml中配置的依赖进行安装。

# 二、py3comtrade模块介绍

| 序号 |         模块名         | 描述                                                        |
|:--:|:-------------------:|-----------------------------------------------------------|
| 1  |     model(模型类)      | 配置文件类：配置文件头、通道数量、模拟量通道、开关量通道、采样点信息、采样段信息、故障时间和变比因子        | 
| 2  |   reader(文件读取模块)    | comtrade文件读取模块，可读取cfg、dat、dmf文件，返回Comtrade对象              |
| 3  | computation(数值计算模块) | 计算模块：可进行傅里叶变换、向量值计算、有效值计算、角度计算、序分量计算、相量转序分量、阻抗计算、故障零时刻计算等 | 
| 4  |     utils(工具模块)     | 工具模块，提供文件工具、角度计算、数据保存等工具                                  |                 

### 1. Comtrade对象

comtrade对象，继承自Configure
> **属性**

- file_path：文件路径
- sample_point：采样点号
- sample_time："采样时间"
- digital_change：变位通道

> **方法**
 
- **get_channel_raw_data_range**：获取指定通道、指定采样点范围的原始采样值数据
  - channel_idx(int,list[int]) 通道索引值或通道索引值列表
  - idx_type:(IdxType)通道标识类型，默认使用INDEX，支持按照通道数组索引值和cfg通道标识an两种方式
  - channel_type(ChannelTyep)通道类型，默认模拟量ANALOG，支持模拟量和开关量两种类型
  - start_point(int) 开始采样点，默认值0，包含该点。
  - end_point(int) 结束采样点，默认值为None，为录波文件最大采样点，不包含该点。
- **get_channel_instant_data_range**：获取指定通道、指定采样点范围的瞬时值数据
  - channel_idx(int,list[int]) 通道索引值或通道索引值列表
  - idx_type:(IdxType)通道标识类型，默认使用INDEX，支持按照通道数组索引值和cfg通道标识an两种方式
  - channel_type(ChannelTyep)通道类型，默认模拟量ANALOG，支持模拟量和开关量两种类型
  - start_point(int) 开始采样点，默认值0，包含该点。
  - end_point(int) 结束采样点，默认值为None，为录波文件最大采样点，不包含该点。
  - output_primary(bool)输出值是否是一次值
- **get_digital_change**：获取所有发生变位的开关量
- **analyze_digital_change_status**：根据开关量采样值计算变化点号及幅值
- _update_configure：更新配置文件对象
  - nrates(List[Nrate]) 采样段
  - data_file_type(DataFileType) 文件格式
- **save_json**：保存json文件
  - file_path(str):保存文件路径
- **save_csv**：保存csv文件
  - file_path(str):保存文件路径
  - samp_point_num_title(bool):是否添加采样点序号行,默认为添加
  - sample_time_title(bool):是否添加采样时间行,默认为添加
  - value_type(str):数值格式instant保存为瞬时值,raw保存为原始采样值,默认为瞬时值
- **save_comtrade**：保存comtrade文件
  - file_path(str) 保存路径,后缀名可选
  - data_file_type(DataFileType) 保存格式,默认保存为二进制文件
- _write_ascii_file：创建ascii文件
- _write_binary_file：创建二进制文件
## 2. 配置文件对象

> **属性**

- header：配置文件头
- channel_num：通道数量
- analogs：模拟通道列表
- digitals：开关量通道列表
- sample：采样信息
- file_start_time：文件起始时间
- fault_time：故障时间
- timemult：数据因子

> **方法**

- 重写__str__方法：返回cfg格式字符串
- **write_cfg_file**：将cfg字符串保存为cfg文件
- **get_cursor_in_segment**：获取游标位置所在的采样段
- **get_two_point_between_segment**：获取两个点之间的采样段
- **equal_two_point_samp_rate**：判断两个点是否处于同一段
- **get_cursor_cycle_point**：获取游标位置所在的采样段
- **get_cursor_sample_range**：获取游标采样点位置开始、结束采样取值范围、采样点个数
- **get_cursor_cycle_sample_range**：获取游标采样点所在周波获取采样取值范围
- **get_zero_point**：获取零时刻采样值采样点位置
- **get_channel**：根据通道索引获取通道类型
- **add_analog**：添加模拟量通道
- **add_digital**：添加开关量通道

## 3. 模型（model）

提供解析后的comtrade对象、配置文件对象、数据对象

### 3.1 配置文件类

#### 3.1.1 ConfigHeader头部信息

> **属性**

- station_name：变电站名称
- recorder_name：录波设备名称
- version：录波格式版本号

> **方法**

- 重写__str__方法：使用“,”连接属性返回字符串

#### 3.1.2 ChannelNum通道数量

采样通道数量

> **属性**

- total_num：采样通道总数
- analog_num：模拟量通道数
- digital_num：开关量通道数

> **方法**

- 重写__str__方法：使用“,”连接属性，在模拟量通道数后拼接A，在开关量通道数后拼写D，返回字符串
- 重写__setattr__方法：当设置模拟量通道数或开关量通道数时，更新采样通道总数
- validate_and_update_totals，实例初始化后调用，用于更新通道数量属性

#### 3.1.3ConfigSample采样信息

> **属性**

- freg：采样频率
- nrate_num：采样段数
- nrates：采样段数组
- count：采样点数
- data_file_type：数据文件类型
- analog_word：模拟量占用字节数
- digital_word：开关量占用字节数
- analog_sampe_word：每采样点模拟量占用字节数
- digital_sampe_word：每采样点开关量占用字节数
- total_sample_word：每采样点占用字节数
- channel_num：通道数量对象

> **方法**

- 重写__iter__方法：返回采样段通道属性的迭代器
- 重写__getitem__方法：根据索引获取通道对象
- 重写__len__方法：返回采样段数量
- 重写__str__方法：按照cfg文件格式返回电网频率、采样段数，调用Nrates方法返回采样段字符串合并为采样信息字符串
- 重写__setitem__方法：设置采样段信息
- **calc_sampling**：计算采样段信息，更新采样段每周波采样点数、该段采样点数、开始采样点号、结束采样点号、该段用时
- **calc_sample_words**：根据文件格式计算每采样点占用字节数
- **add_nrate**：添加采样段信息
- **delete_sampling_nrate**：删除采样段信息

#### 3.1.5 Nrate对象：

采样段对象
> **属性**

- index：索引
- samp：采样频率
- end_point：结束采样点号
- start_point：开始采样点号
- cycle_point：每周波采样点数
- count：该段采样点数
- duration：该段用时
- end_time：该段结束时间

> **方法**

- 重写__str__方法：使用“,”连接属性返回字符串
- validate_count校验通道采样点数

#### 3.1.6 PrecisionTime对象：

时间对象
> **属性**

- time：datetime时间


> **方法**

- 重写__init__方法：初始化时间对象
- 重写__str__方法：使用"%d/%m/%Y,%H:%M:%S.%f"返回字符串
- format_time格式化字符串为时间对象，兼容四位年份、月份和日期位置乱序、日期和时间位置乱序


### 4. 录波通道类

#### 4.1 ChannelIdx对象：

通道对象索引类
> **属性**

- idx_cfg：cfg文件中的通道索引

> **方法**

-重写__str__方法：返回字符串

#### 4.2 Channel对象：

通道对象基类，继承自ChannelIdx类
> **属性**

- name：通道名称
- phase：通道相别
- cdbm：被监视的通道
- index：通道索引
- raw：原始采样值

> **方法**

- 重写__str__方法：使用“,”连接属性返回字符串
- is_enable方法：判断通道是否启用
- channel_flag方法：根据通道名称判断通道类型

#### 4.3 Analog对象：

通道对象基类，继承自Channel类
> **属性**

- unit：通道名称
- a：通道增益系数
- b：通道偏移系数
- skew：通道时滞
- min_val：通道最小值
- max_val：通道最大值
- primary：通道一次系数
- secondary：通道二次系数
- ps：一次二次标识
- ratio：变比
- y：通道有效值，默认为None

> **方法**

- 重写__str__方法：使用“,”连接属性返回字符串
- 重写is_enable方法：判断通道是否启用
- 重写channel_flag方法：根据通道名称判断通道类型

#### 4.4 Analog对象：

通道对象基类，继承自Channel类
> **属性**

- contact：状态通道正常状态
- change_status：变位记录

> **方法**

- 重写__str__方法：使用“,”连接属性返回字符串
- 重写is_enable方法：判断通道是否启用
- 重写channel_flag方法：根据通道名称判断通道类型
- is_change方法：返回是否变位


#### 4.5 DigitalChangeStatus开关量变位状态

> **属性**

- sample_point：采样点
- timestamp：时间戳
- status：状态

### 5. computation计算类

#### 5.1 basic_calc原始值转换瞬时值

> **参数**

- raw(list[int])原始采样值数组
- a(folat)通道增益系数
- b(folat)通道偏移系数
- primary(folat)通道互感器变比一次系数
- secondary(folat)通道互感器变比二次系数
- input_primary(bool)输入数值类型是一次值或二次值
- outpu_primary(bool)输出数值类型是一次值或二次值

#### 5.2 math_polar_rect角度、弧度、向量值互转
#### 5.3 fourier傅里叶计算
- compute_dft_component：实现离散傅里叶变换（DFT）的核心计算逻辑
- fft_component：使用numpy中fft实现离散傅里叶变换的核心计算逻辑
- dft_exp_decay：消除直流分量后返回对应通道的实部和虚部，需要1.5个周波的数据。
#### 5.4 calcium 数值计算
> **属性**

- instant：瞬时值数组
- effective：有效值
- vector：相量值
- angle：角度
- dc_component：直流分量
- harmonics：各次谐波

> **方法**

- model_post_init：在模型初始化完成后根据瞬时值数组自动计算属性值
- calc_vector：返回相量值
- calc_angle：返回角度
- calc_dc_component：返回直流分量
- calc_harmonics：返回各次谐波
- calc_effective：返回有效值
- 
#### 5.5 Sequence 向量转序分量
- phasor_to_sequence_by_rotate：将相分量转化为序分量,使用旋转B、C角度进行计算
- phasor_to_sequence_by_matrix：将相量值转化为序分量，使用numpy矩阵
#### 5.6 impedance阻抗计算
- compute_line_impedance：通过本侧故障前后电压、电流通道和对侧故障前后电压，计算线路正序阻抗

### DMF故障模型类

#### AnalogChannel模拟量通道模型

#### StatusChannel开关量通道模型

#### Transformer变压器模型

#### TransformerWinding变压器绕组模型

### 1.1 Comtrade对象

> 属性

- **配置信息对象（Configure）**：故障头、通道数量、模拟量通道、开关量通道、采样信息、故障时间和变比因子
- **数据数组对象（DataReader）**：采样时间数组、模拟量数据列表、开关量数据列表
- **变位开关量通道记录**：发生变位的开关量对象列表及变位采样点号和状态

> 方法

- **get_raw_by_analog_index**：根据模拟量索引位置获取原始采样值，返回numpy数组。
- **get_raws_by_analog_index**：根据模拟量所以你位置数组获取原始采样值，返回numpy数组。
- **get_instant_by_analog**：获取指定单个通道、指定采样点或周波数的瞬时值，返回numpy数组。
- **get_instants_by_analog**：获取指定多个通道、指定采样点或周波数的瞬时值，返回numpy数组。
- **get_instant_samples_by_segment**：获取指定通道、指定采样段的瞬时值，返回numpy数组。
