# 水流节点说明文档

## 概述

本文档介绍了两个用于水处理系统的基础节点：**水流源节点 (WaterSource)** 和 **水流终点节点 (WaterSink)**。这两个节点为构建复杂的水处理流程图提供了基础组件。

## 节点列表

### 1. 水流源节点 (WaterSource)

**文件**: `mod_water_source.py`

#### 功能描述
- 生成指定流量的水流
- 作为水处理系统的起始节点
- 支持配置水流参数（流量、水温、水质类型）

#### 输入输出
- **输入**: 无（源节点）
- **输出**: 水流量 (m³/h)

#### 可配置参数

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| 输出流量 | float | 100.0 | 输出水流量，单位：m³/h |

#### 使用示例

```python
from mod_water_source import WaterSource

# 创建水流源
water_source = WaterSource()

# 配置参数
params = {
    '输出流量': 150.0
}
water_source.read_parameters(params)

# 获取输出
output = water_source.compute_outputs(time=0)
flow_rate = output[0]  # 150.0 m³/h
```

#### 主要方法

- `read_parameters(params)`: 读取配置参数
- `compute_outputs(time)`: 计算输出流量
- `get_water_info()`: 获取水流信息
- `reset()`: 重置节点状态

### 2. 水流终点节点 (WaterSink)

**文件**: `mod_water_sink.py`

#### 功能描述
- 接收和显示水流信息
- 记录流量历史数据
- 提供流量统计功能
- 作为水处理系统的终端节点

#### 输入输出
- **输入**: 水流量 (m³/h)
- **输出**: 无（终点节点）

#### 可配置参数
- 无（终点节点没有用户可配置参数）

#### 使用示例

```python
from mod_water_sink import WaterSink

# 创建水流终点
water_sink = WaterSink()

# 接收流量输入
water_sink.read_inputs([120.0])  # 输入120 m³/h

# 获取统计信息
stats = water_sink.get_flow_statistics()
print(f"当前流量: {stats['当前流量']} m³/h")

# 打印统计信息
water_sink.print_statistics()
```

#### 主要方法

- `read_inputs(inputs)`: 读取输入流量（自动打印接收信息）
- `get_current_flow()`: 获取当前流量
- `get_flow_statistics()`: 获取流量统计信息
- `print_statistics()`: 打印统计信息
- `get_recent_history(count)`: 获取最近的流量历史
- `reset()`: 重置节点状态

#### 统计功能

水流终点节点自动记录和统计以下信息：

- 当前流量
- 历史记录数量
- 累计处理水量
- 平均流量
- 最大流量
- 最小流量
- 流量变化历史（带时间戳）

## 系统集成示例

### 基本水流系统

```python
from mod_water_source import WaterSource
from mod_water_sink import WaterSink

# 创建源和终点
source = WaterSource()
sink = WaterSink()

# 配置源参数
source.read_parameters({'输出流量': 100.0})

# 获取源输出并传递给终点
flow = source.compute_outputs(time=0)[0]
sink.read_inputs([flow])

# 查看结果
sink.print_statistics()
```

### 多源汇聚系统

```python
# 创建多个源
source1 = WaterSource()
source2 = WaterSource()
sink = WaterSink()

# 配置不同流量
source1.read_parameters({'输出流量': 50.0})
source2.read_parameters({'输出流量': 80.0})

# 汇聚流量
flow1 = source1.compute_outputs(time=0)[0]
flow2 = source2.compute_outputs(time=0)[0]
total_flow = flow1 + flow2

# 输入到终点
sink.read_inputs([total_flow])
```

### 动态流量变化

```python
source = WaterSource()
sink = WaterSink()

# 模拟不同时间段的流量变化
flow_schedule = [100, 150, 80, 200, 0, 120]

for i, flow in enumerate(flow_schedule):
    source.read_parameters({'输出流量': flow})
    output = source.compute_outputs(time=i)
    sink.read_inputs(output)
    
# 查看流量变化历史
history = sink.get_recent_history()
for record in history:
    print(f"[{record['timestamp']}] 流量: {record['flow_rate']} m³/h")
```

## 特性和优势

### 🌊 水流源节点特性

1. **灵活配置**: 支持流量、水温、水质类型等多种参数
2. **实时输出**: 根据配置参数实时计算输出流量
3. **信息丰富**: 提供完整的水流信息（流量、温度、水质）
4. **易于集成**: 标准的pyingraph节点接口

### 📊 水流终点节点特性

1. **自动记录**: 自动记录所有接收到的流量数据
2. **实时显示**: 实时打印接收到的流量信息
3. **统计分析**: 提供丰富的流量统计功能
4. **历史追踪**: 保存流量变化历史（带时间戳）
5. **数据管理**: 自动管理历史数据，防止内存溢出

## 应用场景

### 1. 水处理工艺设计
- 作为工艺流程的起点和终点
- 模拟不同水源的供水情况
- 监控处理后的出水流量

### 2. 系统性能测试
- 测试水处理设备的处理能力
- 验证系统在不同流量下的表现
- 分析流量变化对系统的影响

### 3. 流量平衡计算
- 多水源汇聚计算
- 流量分配优化
- 水量平衡验证

### 4. 运行监控
- 实时监控系统流量
- 记录运行历史数据
- 异常流量检测

## 文件结构

```
demo_wtc_RO/
├── mod_water_source.py              # 水流源节点实现
├── mod_water_sink.py                # 水流终点节点实现
├── test_water_flow_system.py        # 综合测试脚本
└── README_WaterFlowNodes.md         # 本说明文档
```

## 测试验证

### 单独测试

```bash
# 测试水流源节点
python mod_water_source.py

# 测试水流终点节点
python mod_water_sink.py
```

### 综合测试

```bash
# 运行完整的系统测试
python test_water_flow_system.py
```

测试包括：
- ✅ 基本功能测试
- ✅ 动态流量变化测试
- ✅ 多源单汇测试
- ✅ 参数验证和边界测试
- ✅ 异常情况处理测试

## 扩展和定制

### 扩展水流源节点

```python
class AdvancedWaterSource(WaterSource):
    def __init__(self):
        super().__init__()
        # 添加更多参数
        self.attrNamesArr.extend(['压力', 'pH值', '浊度'])
    
    def compute_outputs(self, time):
        # 添加时间相关的流量变化
        base_flow = super().compute_outputs(time)[0]
        time_factor = 1 + 0.1 * math.sin(time)  # 周期性变化
        return [base_flow * time_factor]
```

### 扩展水流终点节点

```python
class AnalyticsWaterSink(WaterSink):
    def __init__(self):
        super().__init__()
        self.alerts = []  # 报警记录
    
    def read_inputs(self, inputs):
        super().read_inputs(inputs)
        
        # 添加流量异常检测
        flow = self.get_current_flow()
        if flow > 500:  # 流量过高报警
            self.alerts.append(f"高流量报警: {flow} m³/h")
        elif flow < 10 and flow > 0:  # 流量过低报警
            self.alerts.append(f"低流量报警: {flow} m³/h")
```

## 注意事项

1. **参数单位**: 确保流量单位统一使用 m³/h
2. **时间处理**: 水流终点的时间戳基于系统时间
3. **内存管理**: 历史记录自动限制在100条以内
4. **异常处理**: 支持负流量和零流量的处理
5. **编码格式**: 文件使用UTF-8编码支持中文参数

## 兼容性

- ✅ Python 3.7+
- ✅ pyingraph框架
- ✅ 中文Unicode参数名
- ✅ Windows/Linux/macOS

---

**创建日期**: 2024年  
**版本**: 1.0  
**作者**: pyingraph开发团队  
**许可**: 遵循项目许可协议