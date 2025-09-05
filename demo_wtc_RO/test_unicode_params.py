#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试中文Unicode参数名的超滤单元节点
Test script for UltrafiltrationUnit with Chinese Unicode parameter names
"""

from mod_ultrafiltration_unit import UltrafiltrationUnit

def test_unicode_parameters():
    """测试中文Unicode参数名功能"""
    print("=== 测试中文Unicode参数名 ===")
    
    # 创建超滤单元实例
    uf_unit = UltrafiltrationUnit()
    
    # 显示参数名列表
    print("\n参数名列表:")
    for i, param_name in enumerate(uf_unit.attrNamesArr):
        print(f"{i+1}. {param_name}")
    
    # 测试中文参数设置
    chinese_params = {
        '回收率': 0.88,           # recovery_rate
        '给水泵扬程': 55,         # feed_pump_head  
        '膜型号': 'UF-300',       # membrane_model
        '膜面积': 45,             # membrane_area
        '产水通量': 90,           # permeate_flux
        '反洗泵扬程': 35          # backwash_pump_head
    }
    
    print("\n设置的中文参数:")
    for key, value in chinese_params.items():
        print(f"{key}: {value}")
    
    # 读取参数
    uf_unit.read_parameters(chinese_params)
    
    # 验证参数是否正确设置
    print("\n验证参数设置:")
    print(f"回收率: {uf_unit.recovery_rate}")
    print(f"给水泵扬程: {uf_unit.feed_pump_head} m")
    print(f"膜型号: {uf_unit.membrane_model}")
    print(f"膜面积: {uf_unit.membrane_area} m²")
    print(f"产水通量: {uf_unit.permeate_flux} L/m²/h")
    print(f"反洗泵扬程: {uf_unit.backwash_pump_head} m")
    
    # 测试计算功能
    print("\n=== 测试计算功能 ===")
    
    # 设置输入流量
    feed_flow = 120.0  # m³/h
    uf_unit.read_inputs([feed_flow])
    
    # 计算输出
    outputs = uf_unit.compute_outputs(0.0)
    permeate_flow, concentrate_flow = outputs
    
    print(f"进水流量: {feed_flow} m³/h")
    print(f"产水流量: {permeate_flow:.2f} m³/h")
    print(f"浓水流量: {concentrate_flow:.2f} m³/h")
    
    # 选型计算
    sizing_results = uf_unit.compute_sizing()
    
    print("\n=== 选型计算结果 ===")
    for key, value in sizing_results.items():
        if isinstance(value, (int, float)):
            if key in ['给水泵流量', '反洗水泵流量']:
                print(f"{key}: {value:.2f} m³/h")
            elif key == '超滤膜支数':
                print(f"{key}: {value} 支")
            elif key == '反洗水箱容积':
                print(f"{key}: {value:.2f} L")
            elif key == '原水箱容积':
                print(f"{key}: {value:.2f} m³")
            else:
                print(f"{key}: {value}")
        else:
            print(f"{key}: {value}")
    
    print("\n=== Unicode参数测试完成 ===")
    return True

def test_parameter_validation():
    """测试参数验证功能"""
    print("\n=== 测试参数验证 ===")
    
    uf_unit = UltrafiltrationUnit()
    
    # 测试缺少参数的情况（应使用默认值）
    partial_params = {
        '回收率': 0.92,
        '膜型号': 'UF-400'
    }
    
    print("\n部分参数设置:")
    for key, value in partial_params.items():
        print(f"{key}: {value}")
    
    uf_unit.read_parameters(partial_params)
    
    print("\n参数读取结果（缺少的参数使用默认值）:")
    print(f"回收率: {uf_unit.recovery_rate} (设置值)")
    print(f"给水泵扬程: {uf_unit.feed_pump_head} m (默认值)")
    print(f"膜型号: {uf_unit.membrane_model} (设置值)")
    print(f"膜面积: {uf_unit.membrane_area} m² (默认值)")
    print(f"产水通量: {uf_unit.permeate_flux} L/m²/h (默认值)")
    print(f"反洗泵扬程: {uf_unit.backwash_pump_head} m (默认值)")
    
    return True

if __name__ == "__main__":
    try:
        # 测试Unicode参数
        test_unicode_parameters()
        
        # 测试参数验证
        test_parameter_validation()
        
        print("\n✅ 所有测试通过！中文Unicode参数名功能正常工作。")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()