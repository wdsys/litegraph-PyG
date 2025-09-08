# 超滤单元节点 (UltrafiltrationUnit)

## 概述

超滤单元节点是一个专为水处理领域设计的pyingraph兼容节点，用于模拟和计算超滤工艺的运行参数和设备选型。

## 功能特性

### 输入输出
- **输入**: 进水水流量 (m³/h)
- **输出**: 
  - 输出0: 产水水流量 (m³/h)
  - 输出1: 浓水水流量 (m³/h)

### 用户可配置参数
- `recovery_rate`: 回收率 (0-1之间的小数，默认0.85)
- `feed_pump_head`: 给水泵扬程 (m，默认50)
- `membrane_model`: 膜型号 (字符串，默认"UF-100")
- `membrane_area`: 膜面积 (m²，默认40)
- `permeate_flux`: 产水通量 (L/m²/h，默认80)
- `backwash_pump_head`: 反洗泵扬程 (m，默认30)

## 计算算法

### 输出计算
```
产水水流量 = 进水水流量 × 回收率
浓水水流量 = 进水水流量 - 产水水流量
```

### 选型计算
```
给水泵流量 = 进水水流量
超滤膜支数 = round(产水水流量 × 1000 / 产水通量 / 膜面积)
反洗水泵流量 = 超滤膜支数 × 1.8
反洗水箱容积 = 35 × 2 × 超滤膜支数 (L)
原水箱容积 = 进水水流量 × 2 (m³)
```

## 使用方法

### 基本使用

```python
from mod_ultrafiltration_unit import UltrafiltrationUnit

# 创建超滤单元实例
uf_unit = UltrafiltrationUnit()

# 设置参数
params = {
    'recovery_rate': 0.90,      # 回收率90%
    'feed_pump_head': 60,       # 给水泵扬程60m
    'membrane_model': "UF-200", # 膜型号
    'membrane_area': 50,        # 膜面积50m²
    'permeate_flux': 100,       # 产水通量100L/m²/h
    'backwash_pump_head': 40    # 反洗泵扬程40m
}
uf_unit.read_parameters(params)

# 设置输入
feed_flow = 100.0  # 进水流量100 m³/h
uf_unit.read_inputs([feed_flow])

# 计算输出
outputs = uf_unit.compute_outputs(time=0)
permeate_flow = outputs[0]  # 产水流量
concentrate_flow = outputs[1]  # 浓水流量

print(f"产水流量: {permeate_flow} m³/h")
print(f"浓水流量: {concentrate_flow} m³/h")

# 计算选型参数
sizing_results = uf_unit.compute_sizing()
```

### 在pyingraph图中使用

1. 将 `mod_ultrafiltration_unit.py` 文件放置在项目的 `local_modules` 目录中
2. 在LiteGraph编辑器中创建自定义节点
3. 设置节点属性:
   - 类文件: `mod_ultrafiltration_unit.py`
   - 类名: `UltrafiltrationUnit`
   - 配置所需的参数

## 重要说明

### 调用顺序
1. **必须先调用** `compute_outputs()` 计算输出流量
2. **然后调用** `compute_sizing()` 进行选型计算

这是因为选型计算需要使用输出计算的中间结果（产水流量等）。

### 选型计算结果
选型计算的结果会通过console打印显示，包括:
- 给水泵流量
- 超滤膜支数
- 反洗水泵流量
- 反洗水箱容积
- 原水箱容积

同时，`compute_sizing()` 方法也会返回包含这些结果的字典。

## 示例场景

### 典型工业应用参数
```python
# 中等规模水处理厂
params = {
    'recovery_rate': 0.85,
    'feed_pump_head': 55,
    'membrane_model': "UF-150",
    'membrane_area': 45,
    'permeate_flux': 90,
    'backwash_pump_head': 35
}
```

### 高效率配置
```python
# 高回收率配置
params = {
    'recovery_rate': 0.95,
    'feed_pump_head': 65,
    'membrane_model': "UF-200",
    'membrane_area': 60,
    'permeate_flux': 120,
    'backwash_pump_head': 45
}
```

## 文件结构

```
local_modules/
├── mod_ultrafiltration_unit.py     # 超滤单元节点实现
└── README_UltrafiltrationUnit.md   # 本说明文档

demo_control_system_local/
└── ultrafiltration_demo.py         # 使用演示脚本
```

## 扩展和定制

如需修改计算算法或添加新的参数，可以:

1. 修改 `attrNamesArr` 列表添加新参数
2. 在 `__init__()` 方法中设置新参数的默认值
3. 在 `compute_outputs()` 或 `compute_sizing()` 方法中实现新的计算逻辑

## 注意事项

- 确保所有参数值都在合理范围内
- 回收率应在0-1之间
- 膜面积和产水通量不能为0，否则会导致除零错误
- 在实际工程应用中，膜支数通常按最大设计流量确定，不会频繁变化