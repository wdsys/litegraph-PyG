#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
水流终点节点 (Water Sink Node)
用于接收和显示水流信息
"""

from pyingraph import BlockBase
import time

class WaterSink(BlockBase):
    """
    水流终点节点
    
    功能：
    - 接收水流输入
    - 打印显示接收到的流量信息
    - 记录流量历史数据
    - 作为水处理系统的终端节点
    
    输入：
    - 水流量 (m³/h)
    
    输出：
    - 无输出（终点节点）
    """
    
    def __init__(self):
        super().__init__()
        # 终点节点没有用户可配置的参数
        self.attrNamesArr = []
        
        # 输入输出数量
        self.numInputs = 1   # 接收一个水流输入
        self.numOutputs = 0  # 终点节点没有输出
        
        # 节点描述
        self.title = "水流终点"
        self.desc = "接收和显示水流信息"
        
        # 内部状态
        self._inputs = [0.0]
        self._flow_history = []  # 流量历史记录
        self._total_volume = 0.0  # 累计处理水量
        self._last_update_time = None
        
    def read_inputs(self, inputs: list) -> None:
        """
        读取输入水流
        :param inputs: 输入列表 [流量]
        """
        if inputs is None:
            self._inputs = [0.0]
        else:
            self._inputs = inputs if inputs else [0.0]
            
        # 记录接收到的流量
        current_time = time.time()
        flow_rate = self._inputs[0]
        
        # 打印接收到的输入
        timestamp = time.strftime("%H:%M:%S", time.localtime(current_time))
        print(f"[{timestamp}] 水流终点接收到流量: {flow_rate:.2f} m³/h")
        
        # 记录流量历史
        self._flow_history.append({
            'time': current_time,
            'timestamp': timestamp,
            'flow_rate': flow_rate
        })
        
        # 计算累计水量（如果有上次更新时间）
        if self._last_update_time is not None:
            time_diff_hours = (current_time - self._last_update_time) / 3600.0
            volume_increment = flow_rate * time_diff_hours
            self._total_volume += volume_increment
            
        self._last_update_time = current_time
        
        # 保持历史记录在合理范围内（最多保留100条记录）
        if len(self._flow_history) > 100:
            self._flow_history = self._flow_history[-100:]
    
    def read_parameters(self, params: dict) -> None:
        """
        读取参数配置（终点节点没有参数）
        :param params: 参数字典
        """
        # 终点节点没有参数需要配置
        pass
    
    def compute_outputs(self, time: float) -> list:
        """
        计算输出（终点节点没有输出）
        :param time: 当前时间
        :return: 空列表（没有输出）
        """
        # 终点节点没有输出
        return []
    
    def get_current_flow(self) -> float:
        """
        获取当前流量
        :return: 当前流量值
        """
        return self._inputs[0] if self._inputs else 0.0
    
    def get_flow_statistics(self) -> dict:
        """
        获取流量统计信息
        :return: 流量统计字典
        """
        if not self._flow_history:
            return {
                '当前流量': 0.0,
                '历史记录数': 0,
                '累计水量': 0.0,
                '平均流量': 0.0,
                '最大流量': 0.0,
                '最小流量': 0.0
            }
        
        flows = [record['flow_rate'] for record in self._flow_history]
        
        return {
            '当前流量': self.get_current_flow(),
            '历史记录数': len(self._flow_history),
            '累计水量': self._total_volume,
            '平均流量': sum(flows) / len(flows),
            '最大流量': max(flows),
            '最小流量': min(flows),
            '单位': 'm³/h'
        }
    
    def print_statistics(self):
        """
        打印流量统计信息
        """
        stats = self.get_flow_statistics()
        print("\n=== 水流终点统计信息 ===")
        for key, value in stats.items():
            if key == '单位':
                continue
            if isinstance(value, float):
                print(f"{key}: {value:.2f} {stats.get('单位', '')}")
            else:
                print(f"{key}: {value}")
        print("========================")
    
    def get_recent_history(self, count: int = 10) -> list:
        """
        获取最近的流量历史记录
        :param count: 返回记录数量
        :return: 最近的流量记录列表
        """
        return self._flow_history[-count:] if self._flow_history else []
    
    def reset(self) -> None:
        """
        重置节点状态
        """
        self._inputs = [0.0]
        self._flow_history = []
        self._total_volume = 0.0
        self._last_update_time = None
        print("水流终点节点已重置")
    
    def __str__(self):
        current_flow = self.get_current_flow()
        return f"WaterSink(当前流量={current_flow:.2f} m³/h, 历史记录={len(self._flow_history)}条)"

# 测试代码
if __name__ == "__main__":
    print("=== 水流终点节点测试 ===")
    
    # 创建水流终点实例
    water_sink = WaterSink()
    
    print(f"\n节点信息: {water_sink}")
    
    # 模拟接收不同的流量输入
    print("\n=== 模拟流量输入 ===")
    test_flows = [100.0, 120.0, 95.0, 110.0, 0.0, 150.0]
    
    for i, flow in enumerate(test_flows):
        print(f"\n--- 第{i+1}次输入 ---")
        water_sink.read_inputs([flow])
        
        # 短暂延时模拟时间流逝
        import time
        time.sleep(0.1)
    
    # 显示统计信息
    water_sink.print_statistics()
    
    # 显示最近历史记录
    print("\n=== 最近流量历史 ===")
    recent_history = water_sink.get_recent_history(5)
    for record in recent_history:
        print(f"[{record['timestamp']}] 流量: {record['flow_rate']:.2f} m³/h")
    
    # 测试重置功能
    print("\n=== 测试重置功能 ===")
    water_sink.reset()
    print(f"重置后节点信息: {water_sink}")
    
    print("\n=== 水流终点节点测试完成 ===")