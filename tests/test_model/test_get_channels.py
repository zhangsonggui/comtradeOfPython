#!/usr/bin/env python
# -*- coding: utf-8 -*-

from py3comtrade.model.channel.analog import Analog
from py3comtrade.model.channel.digital import Digital
from py3comtrade.reader.comtrade_reader import comtrade_reader


def test_get_channels():
    """
    测试get_channels方法的多态查询功能
    """

    # 测试读取不同的配置文件
    test_files = [
        "d:\\codeArea\\gitee\\comtradeOfPython\\tests\\data\\hjz.cfg",
        "d:\\codeArea\\gitee\\comtradeOfPython\\tests\\data\\xtz.cfg"
    ]

    for file_path in test_files:
        print(f"\n测试文件: {file_path}")
        try:
            comtrade = comtrade_reader(file_path)
            print(f"成功读取文件，包含 {len(comtrade.analogs)} 个模拟通道，{len(comtrade.digitals)} 个开关量通道")

            # 测试1: 获取所有通道
            all_channels = comtrade.get_channels()
            print(f"\n测试1 - 获取所有通道:")
            print(f"  总通道数: {len(all_channels)}")
            # 检查返回的是否都是Channel类型
            for i, channel in enumerate(all_channels[:5]):  # 只显示前5个
                print(f"  通道{i + 1}: 类型={channel.__class__.__name__}, 名称={channel.name}, 索引={channel.idx_cfg}")

            # 测试2: 只获取模拟通道
            analog_channels = comtrade.get_channels(channel_type='analog')
            print(f"\n测试2 - 获取模拟通道:")
            print(f"  模拟通道数: {len(analog_channels)}")
            for i, channel in enumerate(analog_channels[:3]):  # 只显示前3个
                if isinstance(channel, Analog):
                    print(f"  模拟通道{i + 1}: 名称={channel.name}, 单位={channel.unit.code}")

            # 测试3: 只获取开关量通道
            digital_channels = comtrade.get_channels(channel_type='digital')
            print(f"\n测试3 - 获取开关量通道:")
            print(f"  开关量通道数: {len(digital_channels)}")
            for i, channel in enumerate(digital_channels[:3]):  # 只显示前3个
                if isinstance(channel, Digital):
                    print(f"  开关量通道{i + 1}: 名称={channel.name}, 状态={channel.contact}")

            # 测试4: 根据索引获取通道 (使用idx_type=INDEX)
            if analog_channels:
                # 假设获取前2个模拟通道
                selected_indices = [0, 1]
                indexed_channels = comtrade.get_channels(channel_type='analog', index=selected_indices,
                                                         idx_type="INDEX")
                print(f"\n测试4 - 根据索引获取通道 (索引: {selected_indices}):")
                print(f"  返回通道数: {len(indexed_channels)}")
                for channel in indexed_channels:
                    print(f"  通道: 索引={channel.idx_cfg}, 名称={channel.name}")

            # 测试5: 测试使用idx_type非INDEX的情况（如果有ccbm值）
            if all_channels:
                # 尝试获取第一个通道的ccbm值进行测试
                test_ccbm = all_channels[0].ccbm
                if test_ccbm:
                    ccbm_channels = comtrade.get_channels(index=test_ccbm, idx_type="CFG")
                    print(f"\n测试5 - 根据ccbm获取通道 (ccbm: {test_ccbm}):")
                    print(f"  返回通道数: {len(ccbm_channels)}")
                    for channel in ccbm_channels:
                        print(f"  通道: ccbm={channel.ccbm}, 名称={channel.name}")

            # 测试6: 测试多态特性 - 统一处理不同类型的通道
            print(f"\n测试6 - 多态特性演示:")
            mixed_channels = comtrade.get_channels()[:5]  # 获取前5个任意类型的通道
            for channel in mixed_channels:
                # 所有通道都有Channel基类的属性和方法
                common_info = f"名称={channel.name}, 索引={channel.idx_cfg}, 是否选中={channel.selected}"

                # 根据实际类型获取特有属性
                if isinstance(channel, Analog):
                    print(f"  模拟通道 - {common_info}, 单位={channel.unit.code}")
                elif isinstance(channel, Digital):
                    print(f"  开关量通道 - {common_info}, 触点类型={channel.contact}")

        except Exception as e:
            print(f"读取或测试出错: {e}")


if __name__ == "__main__":
    test_get_channels()
