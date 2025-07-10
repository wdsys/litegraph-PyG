import matplotlib.pyplot as plt
from pyingraph import BlockBase

class ScopeSink(BlockBase):
    """
    输入信号可视化模块
    功能：实时绘制输入信号随时间变化的曲线
    """
    
    def __init__(self):
        super().__init__()
        self._time_data = []
        self._input_data = []
        self._figure, self._ax, self._line = None, None, None
        # self._figure, self._ax = plt.subplots()
        # self._line, = self._ax.plot([], [])
        # self._ax.set_xlabel('Time')
        # self._ax.set_ylabel('Input Value')
        # self._ax.set_title('Input Signal Scope')
        # plt.ioff()  # 关闭交互模式
    
    def read_parameters(self, parDict):
        """
        读取配置参数
        Args:
            parDict: 参数字典
        """
        # 可以添加配置参数如窗口大小、刷新率等
        pass
    
    def read_inputs(self, inputs):
        """
        存储输入信号
        Args:
            inputs: 输入信号值
        """
        if inputs is None:
            self._inputs = 0
        else:
            self._inputs = inputs
    
    def compute_outputs(self, time: float):
        """
        记录数据但不实时刷新
        """
        self._time_data.append(time)
        self._input_data.append(self._inputs)
    
    def show_final_plot(self):
        if self._figure is None:
            self._figure, self._ax = plt.subplots()
            self._line, = self._ax.plot([], [])
            self._ax.set_xlabel('Time')
            self._ax.set_ylabel('Input Value')
            self._ax.set_title('Input Signal Scope')
            self._ax.grid(True)
        """显示最终结果并添加网格线"""
        self._line.set_data(self._time_data, self._input_data)
        self._ax.relim()
        self._ax.autoscale_view()
        self._ax.grid(True)  # 添加网格线
        plt.show()  # 阻塞式显示最终结果

    def reset(self):
        """重置状态"""
        self._time_data = []
        self._input_data = []
        self._line.set_data([], [])
        self._ax.relim()
        self._ax.autoscale_view()


if __name__ == '__main__':
    # 测试代码
    import time
    import numpy as np
    
    scope = ScopeSink()
    
    # 模拟输入信号
    start_time = time.time()
    while time.time() - start_time < 5:  # 运行10秒
        t = time.time() - start_time
        value = np.sin(t)
        scope.read_inputs(value)
        scope.compute_outputs(t)
        time.sleep(0.01)
    
    scope.show_final_plot()  # 结束后显示最终图像