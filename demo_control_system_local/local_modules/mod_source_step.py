# source block for generating step signal
from pyingraph import BlockBase

class StepSource(BlockBase):
    """
    基于时间的Block，当时间超过预设阈值后切换输出
    """
    def __init__(self):
        super().__init__()
        self.attrNamesArr = ["initial_output", "final_output", "time_threshold"]
    
    def compute_outputs(self, time: float) -> list:
        """根据时间决定输出"""
        if time >= self.time_threshold:
            self._current_output = self.final_output
        else:
            self._current_output = self.initial_output
            
        return [self._current_output]
    
    def reset(self) -> None:
        """重置内部状态"""
        # self._current_output = self.initial_output

    def read_inputs(self, inputs: list) -> None:
        pass

# 示例用法
if __name__ == "__main__":
    # 创建实例：初始输出为0，最终输出为100，step阈值为5
    step_source = StepSource()
    parDict = {
        "initial_output": 0,
        "final_output": 1,
        "time_threshold": 1
    }
    step_source.read_parameters(parDict)
    
    # 模拟计数器变化
    time = 0
    for _ in range(20):
        time += 0.1  # 假设时间以秒为单位
        output = step_source.compute_outputs(time)
        print(f"Time: {time:.2f}, Output: {output[0]:.2f}")