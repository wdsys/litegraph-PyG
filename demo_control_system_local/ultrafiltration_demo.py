#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
超滤单元节点使用示例
演示如何在pyingraph图中使用超滤单元节点
"""

import sys
import os

# 添加local_modules到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'local_modules'))

from mod_ultrafiltration_unit import UltrafiltrationUnit

def demo_ultrafiltration_unit():
    """
    演示超滤单元节点的使用
    """
    print("=== 超滤单元节点演示 ===")
    
    # 创建超滤单元实例
    uf_unit = UltrafiltrationUnit()
    
    # 设置工艺参数
    print("\n1. 设置工艺参数")
    params = {
        'recovery_rate': 0.85,      # 回收率85%
        'feed_pump_head': 55,       # 给水泵扬程55m
        'membrane_model': "UF-150", # 膜型号UF-150
        'membrane_area': 45,        # 膜面积45m²
        'permeate_flux': 90,        # 产水通量90L/m²/h
        'backwash_pump_head': 35    # 反洗泵扬程35m
    }
    uf_unit.read_parameters(params)
    
    print(f"回收率: {uf_unit.recovery_rate}")
    print(f"膜型号: {uf_unit.membrane_model}")
    print(f"膜面积: {uf_unit.membrane_area} m²")
    print(f"产水通量: {uf_unit.permeate_flux} L/m²/h")
    
    # 模拟不同的运行工况
    print("\n2. 模拟不同运行工况")
    test_scenarios = [
        {"name": "低负荷运行", "flow": 80},
        {"name": "设计负荷运行", "flow": 120},
        {"name": "高负荷运行", "flow": 160}
    ]
    
    for scenario in test_scenarios:
        print(f"\n--- {scenario['name']} ---")
        feed_flow = scenario['flow']
        
        # 设置输入
        uf_unit.read_inputs([feed_flow])
        
        # 计算输出
        outputs = uf_unit.compute_outputs(time=0)
        permeate_flow = outputs[0]
        concentrate_flow = outputs[1]
        
        print(f"进水流量: {feed_flow} m³/h")
        print(f"产水流量: {permeate_flow:.2f} m³/h")
        print(f"浓水流量: {concentrate_flow:.2f} m³/h")
        print(f"实际回收率: {(permeate_flow/feed_flow)*100:.1f}%")
        
        # 计算选型参数
        sizing_results = uf_unit.compute_sizing()
        
        # 显示关键选型结果
        print(f"膜支数: {sizing_results['membrane_count']} 支")
        print(f"给水泵流量: {sizing_results['feed_pump_flow']:.1f} m³/h")
        
    # 演示参数变化对结果的影响
    print("\n3. 参数敏感性分析")
    print("\n--- 不同回收率的影响 ---")
    
    feed_flow = 100  # 固定进水流量
    recovery_rates = [0.75, 0.80, 0.85, 0.90, 0.95]
    
    for recovery_rate in recovery_rates:
        # 更新回收率参数（需要提供完整的参数字典）
        updated_params = params.copy()
        updated_params['recovery_rate'] = recovery_rate
        uf_unit.read_parameters(updated_params)
        uf_unit.read_inputs([feed_flow])
        
        outputs = uf_unit.compute_outputs(time=0)
        permeate_flow = outputs[0]
        concentrate_flow = outputs[1]
        
        print(f"回收率 {recovery_rate*100:2.0f}%: 产水 {permeate_flow:5.1f} m³/h, 浓水 {concentrate_flow:5.1f} m³/h")
    
    print("\n=== 演示完成 ===")

def demo_node_integration():
    """
    演示节点在图中的集成使用
    """
    print("\n=== 节点集成演示 ===")
    
    # 模拟一个简单的水处理流程
    # 原水 -> 超滤单元 -> 产水和浓水
    
    uf_unit = UltrafiltrationUnit()
    
    # 设置标准参数
    standard_params = {
        'recovery_rate': 0.88,
        'feed_pump_head': 50,
        'membrane_model': "UF-200",
        'membrane_area': 50,
        'permeate_flux': 100,
        'backwash_pump_head': 30
    }
    uf_unit.read_parameters(standard_params)
    
    print("\n模拟24小时运行数据:")
    print("时间(h)\t进水(m³/h)\t产水(m³/h)\t浓水(m³/h)\t膜支数")
    print("-" * 60)
    
    # 模拟一天中不同时段的流量变化
    hourly_flows = [
        60, 70, 80, 90, 100, 110, 120, 130,  # 0-7点，逐渐增加
        140, 150, 150, 140, 130, 120, 110, 100,  # 8-15点，高峰后下降
        90, 80, 70, 60, 50, 40, 50, 60  # 16-23点，夜间低负荷
    ]
    
    for hour, flow in enumerate(hourly_flows):
        uf_unit.read_inputs([flow])
        outputs = uf_unit.compute_outputs(time=hour)
        sizing = uf_unit.compute_sizing()
        
        print(f"{hour:2d}:00\t{flow:8.1f}\t{outputs[0]:8.1f}\t{outputs[1]:8.1f}\t{sizing['membrane_count']:4d}")
    
    print("\n注意: 在实际应用中，膜支数通常按最大流量设计，不会频繁变化")

if __name__ == "__main__":
    # 运行演示
    demo_ultrafiltration_unit()
    demo_node_integration()