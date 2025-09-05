#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的Unicode参数图测试
"""

import json
import sys
import os
from pathlib import Path

# 添加当前目录到Python路径
sys.path.insert(0, os.getcwd())

def create_simple_graph():
    """创建一个简单的图文件用于测试"""
    graph_data = {
        "nodes": [
            {
                "id": "node1",
                "name": "WaterSource",
                "folder_url": "",
                "folder_path": "local_modules",
                "class_file": "mod_water_source",
                "class_name": "WaterSource",
                "parameters": {
                    "输出流量": 100
                }
            }
        ],
        "edges": []
    }
    
    with open('simple_graph.json', 'w', encoding='utf-8') as f:
        json.dump(graph_data, f, ensure_ascii=False, indent=2)
    
    print("✅ 创建了简单图文件: simple_graph.json")

def test_pyingraph_loading():
    """测试pyingraph加载"""
    try:
        from pyingraph import GraphLoader
        
        # 创建简单图
        create_simple_graph()
        
        # 加载图
        loader = GraphLoader('simple_graph.json', flag_remote=False)
        loader.load()
        
        print("✅ PyInGraph加载成功！")
        
        # 获取图
        nx_graph = loader.get_nx_graph()
        print(f"✅ 图包含 {len(nx_graph.nodes)} 个节点")
        
        # 检查节点实例
        for node_id, node_data in nx_graph.nodes(data=True):
            instance = node_data.get('instance')
            if instance:
                print(f"✅ 节点 {node_id} 实例创建成功")
                if hasattr(instance, 'attrNamesArr'):
                    print(f"  参数列表: {instance.attrNamesArr}")
                if hasattr(instance, '输出流量'):
                    print(f"  输出流量: {getattr(instance, '输出流量')}")
        
        return True
        
    except Exception as e:
        print(f"❌ PyInGraph加载失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("开始简单Unicode图测试...\n")
    
    success = test_pyingraph_loading()
    
    if success:
        print("\n🎉 测试成功！Unicode参数在PyInGraph中工作正常。")
    else:
        print("\n❌ 测试失败，需要进一步调试。")

if __name__ == '__main__':
    main()