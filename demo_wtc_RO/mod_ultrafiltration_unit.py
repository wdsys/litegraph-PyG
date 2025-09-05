#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
超滤单元模块
用于水处理系统中的超滤工艺计算
"""

from pyingraph import BlockBase

class UltrafiltrationUnit(BlockBase):
    """
    超滤单元节点
    
    输入：进水水流量
    输出：输出0为产水水流量，输出1为浓水水流量
    用户指定参数：回收率、给水泵扬程、膜型号、膜面积、产水通量、反洗泵扬程
    """
    
    def __init__(self):
        super().__init__()
        # 定义用户可配置的参数
        # Original English parameter names (commented out for Unicode testing)
        # self.attrNamesArr = [
        #     'recovery_rate',        # 回收率
        #     'feed_pump_head',       # 给水泵扬程
        #     'membrane_model',       # 膜型号
        #     'membrane_area',        # 膜面积
        #     'permeate_flux',        # 产水通量
        #     'backwash_pump_head'    # 反洗泵扬程
        # ]
        
        # New Chinese Unicode parameter names for testing
        self.attrNamesArr = ['回收率', '给水泵扬程', '膜型号', '膜面积', '产水通量', '反洗泵扬程']
        
        # 初始化参数默认值
        self.recovery_rate = 0.85       # 默认回收率85%
        self.feed_pump_head = 50        # 默认给水泵扬程50m
        self.membrane_model = "UF-100"  # 默认膜型号
        self.membrane_area = 40         # 默认膜面积40m²
        self.permeate_flux = 80         # 默认产水通量80L/m²/h
        self.backwash_pump_head = 30    # 默认反洗泵扬程30m
        
        # 内部状态变量，用于存储计算的中间结果
        self._inputs = []
        self._feed_flow = 0.0           # 进水水流量
        self._permeate_flow = 0.0       # 产水水流量
        self._concentrate_flow = 0.0    # 浓水水流量
        
    def read_inputs(self, inputs: list) -> None:
        """
        读取输入信号
        :param inputs: 输入信号列表，包含进水水流量
        """
        if inputs is None:
            self._inputs = [0.0]
        else:
            self._inputs = inputs if inputs else [0.0]
            
    def read_parameters(self, params: dict) -> None:
        """
        读取参数配置
        :param params: 参数字典，使用中文参数名
        """
        # 从参数字典中读取配置参数 (使用中文参数名)
        self.recovery_rate = params.get('回收率', 0.85)  # 默认回收率85%
        self.feed_pump_head = params.get('给水泵扬程', 50)  # 默认给水泵扬程50m
        self.membrane_model = params.get('膜型号', 'UF-100')  # 默认膜型号
        self.membrane_area = params.get('膜面积', 40)  # 默认膜面积40m²
        self.permeate_flux = params.get('产水通量', 80)  # 默认产水通量80L/m²/h
        self.backwash_pump_head = params.get('反洗泵扬程', 30)  # 默认反洗泵扬程30m
            
    def compute_outputs(self, time: float) -> list:
        """
        计算超滤单元的输出
        :param time: 当前时间
        :return: [产水水流量, 浓水水流量]
        """
        # 获取进水水流量
        if not self._inputs:
            self._feed_flow = 0.0
        else:
            self._feed_flow = self._inputs[0] if self._inputs[0] is not None else 0.0
            
        # 计算产水水流量和浓水水流量
        self._permeate_flow = self._feed_flow * self.recovery_rate
        self._concentrate_flow = self._feed_flow - self._permeate_flow
        
        return [self._permeate_flow, self._concentrate_flow]
    
    def compute_sizing(self) -> dict:
        """
        计算选型参数
        注意：此函数应在compute_outputs之后调用，以使用计算得到的流量数据
        :return: 包含选型计算结果的字典
        """
        # 计算选型参数
        feed_pump_flow = self._feed_flow  # 给水泵流量 = 进水水流量
        
        # 超滤膜支数计算
        if self.membrane_area > 0 and self.permeate_flux > 0:
            membrane_count = round(self._permeate_flow * 1000 / self.permeate_flux / self.membrane_area)
        else:
            membrane_count = 0
            
        # 反洗水泵流量
        backwash_pump_flow = membrane_count * 1.8
        
        # 反洗水箱容积
        backwash_tank_volume = 35 * 2 * membrane_count
        
        # 原水箱容积
        raw_water_tank_volume = self._feed_flow * 2
        
        # 构建结果字典
        sizing_results = {
            'feed_pump_flow': feed_pump_flow,                    # 给水泵流量
            'membrane_count': membrane_count,                    # 超滤膜支数
            'backwash_pump_flow': backwash_pump_flow,           # 反洗水泵流量
            'backwash_tank_volume': backwash_tank_volume,       # 反洗水箱容积
            'raw_water_tank_volume': raw_water_tank_volume      # 原水箱容积
        }
        
        # 打印选型计算结果
        print("\n=== 超滤单元选型计算结果 ===")
        print(f"给水泵流量: {feed_pump_flow:.2f} m³/h")
        print(f"超滤膜支数: {membrane_count} 支")
        print(f"反洗水泵流量: {backwash_pump_flow:.2f} m³/h")
        print(f"反洗水箱容积: {backwash_tank_volume:.2f} L")
        print(f"原水箱容积: {raw_water_tank_volume:.2f} m³")
        print("========================\n")
        
        return sizing_results
    
    def reset(self) -> None:
        """
        重置超滤单元的内部状态
        """
        self._inputs = []
        self._feed_flow = 0.0
        self._permeate_flow = 0.0
        self._concentrate_flow = 0.0


if __name__ == "__main__":
    # 测试超滤单元
    uf_unit = UltrafiltrationUnit()
    
    # 设置参数 (使用中文参数名)
    params = {
        '回收率': 0.95,      # 0--1
        '给水泵扬程': 25,       # m
        '膜型号': "ZW1500", 
        '膜面积': 57,        # m²
        '产水通量': 45,       # L/m²/h
        '反洗泵扬程': 25    # m
    }
    uf_unit.read_parameters(params)
    
    # 测试输入：进水水流量100 m³/h
    feed_flow = 100.0
    uf_unit.read_inputs([feed_flow])
    
    # 计算输出
    outputs = uf_unit.compute_outputs(time=0)
    print(f"进水水流量: {feed_flow} m³/h")
    print(f"产水水流量: {outputs[0]:.2f} m³/h")
    print(f"浓水水流量: {outputs[1]:.2f} m³/h")
    
    # 计算选型
    sizing_results = uf_unit.compute_sizing()
    
    # 测试不同的进水流量
    print("\n=== 测试不同进水流量 ===")
    test_flows = [20, 70, 100]
    for flow in test_flows:
        uf_unit.read_inputs([flow])
        outputs = uf_unit.compute_outputs(time=0)
        print(f"\n进水: {flow} m³/h -> 产水: {outputs[0]:.2f} m³/h, 浓水: {outputs[1]:.2f} m³/h")
        uf_unit.compute_sizing()