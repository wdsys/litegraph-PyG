#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Unicode参数加载
"""

import json
import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.getcwd())

def test_unicode_json_loading():
    """测试JSON文件中Unicode字符的加载"""
    print("=== 测试Unicode JSON加载 ===")
    
    # 测试读取包含Unicode的JSON文件
    try:
        with open('pyingraph_export.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("✅ JSON文件加载成功")
        
        # 检查Unicode参数
        for node in data.get('nodes', []):
            params = node.get('parameters', {})
            print(f"节点 {node.get('name', 'Unknown')}: {params}")
            
            # 检查是否包含Unicode参数名
            for param_name, param_value in params.items():
                if any(ord(char) > 127 for char in param_name):
                    print(f"  ✅ 发现Unicode参数: {param_name} = {param_value}")
                    
    except Exception as e:
        print(f"❌ JSON加载失败: {e}")
        return False
    
    return True

def test_module_import():
    """测试模块导入"""
    print("\n=== 测试模块导入 ===")
    
    try:
        # 测试导入水流源模块
        from mod_water_source import WaterSource
        print("✅ WaterSource模块导入成功")
        
        # 创建实例并测试Unicode参数
        source = WaterSource()
        print(f"✅ WaterSource实例创建成功")
        print(f"attrNamesArr: {source.attrNamesArr}")
        
        # 测试设置Unicode参数
        if hasattr(source, 'set_parameter'):
            source.set_parameter('输出流量', 150)
            print("✅ Unicode参数设置成功")
        
        return True
        
    except Exception as e:
        print(f"❌ 模块导入失败: {e}")
        return False

def main():
    """主测试函数"""
    print("开始Unicode参数加载测试...\n")
    
    # 测试JSON加载
    json_ok = test_unicode_json_loading()
    
    # 测试模块导入
    import_ok = test_module_import()
    
    print("\n=== 测试结果 ===")
    print(f"JSON加载: {'✅ 成功' if json_ok else '❌ 失败'}")
    print(f"模块导入: {'✅ 成功' if import_ok else '❌ 失败'}")
    
    if json_ok and import_ok:
        print("\n🎉 所有测试通过！Unicode参数支持正常。")
    else:
        print("\n⚠️ 部分测试失败，需要进一步检查。")

if __name__ == '__main__':
    main()