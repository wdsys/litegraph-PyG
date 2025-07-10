#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module for a lead compensator block.
"""

from pyingraph import BlockBase


class LeadCompensator(BlockBase):
    """
    A block that implements a lead compensator.
    The transfer function is G(s) = k * (s/omega_num + 1) / (s/omega_den + 1), where omega_den > omega_num.
    k is the true DC gain of the compensator.
    """
    def __init__(self):
        super().__init__()
        self.prev_time = None
        self.prev_output = 0.0
        self.prev_input = 0.0
        self.attrNamesArr = ['k', 'omega_num', 'omega_den']

    def compute_outputs(self, time: float) -> list:
        """
        Implements the lead compensator logic.
        State-space representation:
        x_dot = -omega_den*x + u
        y = k*(omega_den-omega_num)*x + k*u
        """
        if not hasattr(self, '_inputs') or not self._inputs:
            return [0.0]

        if self.prev_time is None:
            self.prev_time = time
            return [0.0]

        dt = time - self.prev_time
        if dt <= 0:
            # If time has not advanced, output the last known value based on current state
            # input_signal = self._inputs[0]
            # output = self.k * (self.omega_den - self.omega_num) * self.state + self.k * input_signal
            output = self.prev_output
            # self.prev_output = output
            return [output]

        input_signal = self._inputs[0]
        
        u = self._inputs[0]
        du = u - self.prev_input
        self.prev_input = u
        
        udot = du / dt
        ydot = (-self.omega_den * self.prev_output 
                + self.k * self.omega_den / self.omega_num * udot
                + self.k * self.omega_den * u)
        y = self.prev_output + ydot * dt

        self.prev_time = time
        self.prev_input = u
        self.prev_output = y

        return [y]

    def reset(self) -> None:
        """Resets the compensator state."""
        self.prev_time = None
        self.prev_output = 0
        self.prev_input = 0

    def read_inputs(self, inputs: list) -> None:
        """
        Reads the input signal.
        """
        if inputs is None:
            self._inputs = []
        else:
            if len(inputs) != 1:
                raise ValueError("Input list must contain exactly one value")
            self._inputs = inputs

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import numpy as np

    compensator = LeadCompensator()
    params = {
        "k": 2.0,           # True DC gain
        "omega_num": 5.0,   # Numerator break frequency (zero)
        "omega_den": 10.0   # Denominator break frequency (pole)
    }
    compensator.read_parameters(params)

    time_points = np.arange(0, 5, 0.01)
    inputs = []
    outputs = []

    for t in time_points:
        # Step input at t=1.0
        input_val = 1.0 if t >= 1.0 else 0.0
        inputs.append(input_val)
        compensator.read_inputs([input_val])
        output = compensator.compute_outputs(t)
        outputs.append(output[0])

    plt.figure(figsize=(10, 6))
    plt.plot(time_points, inputs, label='Input (Step)')
    plt.plot(time_points, outputs, label='Lead Compensator Output')
    plt.title(f'Step Response of Lead Compensator (k={params["k"]}, ωn={params["omega_num"]}, ωd={params["omega_den"]})')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.grid(True)
    plt.show()