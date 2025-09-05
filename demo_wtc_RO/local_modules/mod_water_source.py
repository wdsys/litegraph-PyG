#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
水流源节点 (Water Source Node)
用于生成指定流量的水流
"""

from pyingraph import BlockBase

class WaterSource(BlockBase):
    """
    水流源节点
    
    功能：
    - 生成用户指定流量的水流
    - 可配置输出流量参数
    - 作为水处理系统的起始节点
    
    输出：
    - 水流量 (m³/h)
    """
    
    def __init__(self):
        super().__init__()
        # 定义用户可配置的参数
        self.attrNamesArr = ['输出流量']  # output_flow_rate
        
        # 默认参数值
        self.output_flow_rate = 100.0  # 默认输出流量 100 m³/h
        
        # 输出数量
        self.numOutputs = 1
        self.numInputs = 0  # 源节点没有输入
        
        # 节点描述
        self.title = "水流源"
        self.desc = "生成指定流量的水流"
    
    def read_inputs(self, inputs: list) -> None:
        """
        读取输入（源节点通常没有输入）
        """
        # 源节点不需要处理输入
        pass
    
    def read_parameters(self, params: dict) -> None:
        """
        读取参数配置
        :param params: 参数字典，使用中文参数名
        """
        # 从参数字典中读取配置参数
        self.output_flow_rate = params.get('输出流量', 100.0)  # 默认输出流量100 m³/h
    
    def compute_outputs(self, time: float) -> list:
        """
        计算输出
        :param time: 当前时间
        :return: 输出列表 [流量]
        """
        # 水流源直接输出设定的流量
        return [self.output_flow_rate]
    
    def get_water_info(self) -> dict:
        """
        获取水流信息
        :return: 水流信息字典
        """
        return {
            '流量': self.output_flow_rate,
            '单位': 'm³/h'
        }
    
    def reset(self) -> None:
        """
        重置节点状态
        """
        # 源节点通常不需要重置特殊状态
        pass
    
    def __str__(self):
        return f"WaterSource(流量={self.output_flow_rate} m³/h)"

# 测试代码
if __name__ == "__main__":
    print("=== 水流源节点测试 ===")
    
    # 创建水流源实例
    water_source = WaterSource()
    
    # 设置参数 (使用中文参数名)
    params = {
        '输出流量': 150.0       # 输出流量150 m³/h
    }
    water_source.read_parameters(params)
    
    print(f"\n节点信息: {water_source}")
    
    # 计算输出
    outputs = water_source.compute_outputs(time=0)
    print(f"\n输出流量: {outputs[0]} m³/h")
    
    # 获取水流信息
    water_info = water_source.get_water_info()
    print("\n=== 水流信息 ===")
    for key, value in water_info.items():
        print(f"{key}: {value}")
    
    print("\n=== 测试不同参数设置 ===")
    
    # 测试不同流量设置
    test_flows = [50, 100, 200, 300]
    for flow in test_flows:
        test_params = {
            '输出流量': flow
        }
        water_source.read_parameters(test_params)
        outputs = water_source.compute_outputs(time=0)
        print(f"设置流量: {flow} m³/h -> 输出流量: {outputs[0]} m³/h")
    
    print("\n=== 水流源节点测试完成 ===")