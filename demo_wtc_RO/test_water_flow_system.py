#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
水流系统综合测试
演示水流源和水流终点节点的协同工作
"""

from mod_water_source import WaterSource
from mod_water_sink import WaterSink
import time

def test_basic_flow_system():
    """
    测试基本的水流系统
    """
    print("=== 基本水流系统测试 ===")
    
    # 创建水流源和水流终点
    water_source = WaterSource()
    water_sink = WaterSink()
    
    # 配置水流源参数
    source_params = {
        '输出流量': 120.0
    }
    water_source.read_parameters(source_params)
    
    print(f"\n水流源配置: {water_source}")
    print(f"水流终点初始状态: {water_sink}")
    
    # 模拟水流传输
    print("\n=== 开始水流传输 ===")
    
    # 获取源的输出
    source_output = water_source.compute_outputs(time=0)
    flow_rate = source_output[0]
    
    print(f"水流源输出: {flow_rate} m³/h")
    
    # 将源的输出传递给终点
    water_sink.read_inputs([flow_rate])
    
    # 显示水流信息
    water_info = water_source.get_water_info()
    print("\n=== 水流源信息 ===")
    for key, value in water_info.items():
        print(f"{key}: {value}")
    
    # 显示终点统计
    water_sink.print_statistics()
    
    return water_source, water_sink

def test_dynamic_flow_system():
    """
    测试动态水流系统（流量变化）
    """
    print("\n\n=== 动态水流系统测试 ===")
    
    # 创建水流源和水流终点
    water_source = WaterSource()
    water_sink = WaterSink()
    
    # 模拟不同时间段的流量变化
    flow_scenarios = [
        {'time': 0, 'flow': 100.0},
        {'time': 1, 'flow': 150.0},
        {'time': 2, 'flow': 80.0},
        {'time': 3, 'flow': 200.0},
        {'time': 4, 'flow': 0.0},  # 停水
        {'time': 5, 'flow': 120.0},  # 恢复供水
    ]
    
    print("\n模拟6个时间段的流量变化:")
    
    for scenario in flow_scenarios:
        print(f"\n--- 时间段 {scenario['time']} ---")
        
        # 更新水流源参数
        source_params = {
            '输出流量': scenario['flow']
        }
        water_source.read_parameters(source_params)
        
        # 计算输出并传递给终点
        source_output = water_source.compute_outputs(time=scenario['time'])
        water_sink.read_inputs(source_output)
        
        print(f"设置: 流量={scenario['flow']} m³/h")
        
        # 短暂延时模拟时间流逝
        time.sleep(0.1)
    
    # 显示最终统计
    print("\n=== 动态测试最终统计 ===")
    water_sink.print_statistics()
    
    # 显示流量历史
    print("\n=== 流量变化历史 ===")
    history = water_sink.get_recent_history(10)
    for i, record in enumerate(history):
        print(f"{i+1}. [{record['timestamp']}] 流量: {record['flow_rate']:.1f} m³/h")
    
    return water_source, water_sink

def test_multiple_sources_single_sink():
    """
    测试多个水流源汇聚到一个终点
    """
    print("\n\n=== 多源单汇测试 ===")
    
    # 创建多个水流源
    source1 = WaterSource()
    source2 = WaterSource()
    source3 = WaterSource()
    sink = WaterSink()
    
    # 配置不同的水流源
    source1.read_parameters({'输出流量': 50.0})
    source2.read_parameters({'输出流量': 80.0})
    source3.read_parameters({'输出流量': 30.0})
    
    print("\n水流源配置:")
    print(f"源1: {source1}")
    print(f"源2: {source2}")
    print(f"源3: {source3}")
    
    # 计算各源的输出
    output1 = source1.compute_outputs(time=0)[0]
    output2 = source2.compute_outputs(time=0)[0]
    output3 = source3.compute_outputs(time=0)[0]
    
    # 汇聚流量（简单相加）
    total_flow = output1 + output2 + output3
    
    print(f"\n流量汇聚:")
    print(f"源1输出: {output1} m³/h")
    print(f"源2输出: {output2} m³/h")
    print(f"源3输出: {output3} m³/h")
    print(f"总流量: {total_flow} m³/h")
    
    # 将总流量输入到终点
    sink.read_inputs([total_flow])
    
    # 显示终点统计
    sink.print_statistics()
    
    return [source1, source2, source3], sink

def test_parameter_validation():
    """
    测试参数验证和边界情况
    """
    print("\n\n=== 参数验证测试 ===")
    
    source = WaterSource()
    sink = WaterSink()
    
    # 测试极端参数
    extreme_params = [
        {'输出流量': 0.0},
        {'输出流量': 1000.0},
        {'输出流量': -10.0},  # 负值测试
    ]
    
    for i, params in enumerate(extreme_params):
        print(f"\n--- 极端参数测试 {i+1} ---")
        print(f"参数: {params}")
        
        source.read_parameters(params)
        output = source.compute_outputs(time=0)
        sink.read_inputs(output)
        
        print(f"源输出: {output[0]} m³/h")
        print(f"当前终点流量: {sink.get_current_flow()} m³/h")
    
    # 测试空输入
    print("\n--- 空输入测试 ---")
    sink.read_inputs(None)
    sink.read_inputs([])
    
    sink.print_statistics()

def main():
    """
    主测试函数
    """
    print("🌊 水流系统综合测试开始 🌊\n")
    
    try:
        # 基本功能测试
        test_basic_flow_system()
        
        # 动态流量测试
        test_dynamic_flow_system()
        
        # 多源单汇测试
        test_multiple_sources_single_sink()
        
        # 参数验证测试
        test_parameter_validation()
        
        print("\n\n✅ 所有测试完成！水流源和水流终点节点功能正常。")
        
    except Exception as e:
        print(f"\n❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()