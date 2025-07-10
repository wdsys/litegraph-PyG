# import numpy as np
from pyingraph import BlockBase

class SecondOrderFilter(BlockBase):
    def __init__(self):
        super().__init__()
        self.prev_time = None  # 用于存储上一次调用的时间
        self.state = [0.0, 0.0]
        self.attrNamesArr = ['omega_n', 'zeta']  # 新增属性名称数组，用于存储属性名称
        
    def xdot_2nd_order_ODE(self, xvec:list, u:float) -> list:
        """
        二阶ODE系统的导数函数
        :param xvec: 状态向量[x1, x2]
        """
        x1, x2 = xvec
        xdot1 = x2
        xdot2 = -2*self.zeta*self.omega_n*x2 - self.omega_n**2*x1 + u
        return [xdot1, xdot2]  # 状态向量的导数，即 dx/dt = [xdot1, xdot2]

    def compute_outputs(self, time: float) -> list:
        """
        实现二阶低通滤波
        :param time: 当前时间
        :return: 滤波后的输出
        """
        if not hasattr(self, '_inputs') or not self._inputs:
            return [0.0]
            
        # 计算时间间隔dt
        if self.prev_time is None:
            # dt = 0.01  # 第一次调用时的默认值
            self.prev_time = time  # 记录第一次调用的时间
            return [0.0]
        else:
            dt = time - self.prev_time
            
        input_signal = self._inputs[0]
        xdotvec = self.xdot_2nd_order_ODE(self.state, input_signal)
        # Euler前向近似方法更新状态
        self.state[0] += xdotvec[0] * dt  # 更新状态x1
        self.state[1] += xdotvec[1] * dt  # 更新状态x2
        current_output = self.state[0]  # 输出状态x1
        self.prev_time = time  # 更新上一次调用的时间
        
        return [current_output]
    
    def reset(self) -> None:
        """重置滤波器状态"""
        self.prev_time = None  # 重置时间
        self.state = [0.0, 0.0]
    
    def read_inputs(self, inputs: list) -> None:
        """
        读取输入信号
        :param inputs: 输入信号列表，长度应为1
        """
        if inputs is None: # intialize
            self._inputs = 0
        else:
            if len(inputs) != 1:
                raise ValueError("Input list must contain exactly one value")
            self._inputs = inputs


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    
    # 创建滤波器实例(调试模式)
    filter = SecondOrderFilter()
    # 设置参数
    parDict = {
        "omega_n": 1.0,  # 自然频率
        "zeta": 0.3     # 阻尼比
    }
    filter.read_parameters(parDict)
    
    # 模拟阶跃输入
    time_points = [i*0.1 for i in range(200)]
    outputs = []
    
    for t in time_points:
        # 设置阶跃输入(从t=2.0开始)
        input_val = 1.0 if t >= 2.0 else 0.0
        if input_val > 0.5:
            input_val = 1.0
        filter.read_inputs([input_val])
        
        # 计算输出
        output = filter.compute_outputs(t)
        outputs.append(output[0])
    
    # 绘制响应曲线
    plt.figure(figsize=(10, 5))
    plt.plot(time_points, outputs, label='Filter Output')
    plt.axvline(x=2.0, color='r', linestyle='--', label='Step Input')
    plt.xlabel('Time (s)')
    plt.ylabel('Output')
    plt.title('Step Response of 2nd-order LPF (ω_n=1.0, ζ=0.3)')
    plt.grid(True)
    plt.legend()
    plt.show()