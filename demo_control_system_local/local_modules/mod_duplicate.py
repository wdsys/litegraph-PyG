#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module for a duplication block.
"""

from pyingraph import BlockBase

class Duplicate(BlockBase):
    """
    A block that duplicates its single input to multiple outputs.
    The number of outputs is specified by the n_output parameter.
    """
    def __init__(self):
        super().__init__()
        self.attrNamesArr = ['n_output']  # Parameter for number of outputs
        self._inputs = []
        self.n_output = 2  # Default number of outputs

    def read_inputs(self, inputs: list) -> None:
        """Reads and stores the input values."""
        self._inputs = inputs

    def compute_outputs(self, time: float) -> list:
        """Duplicates the single input to n_output outputs."""
        if not self._inputs:
            # If no input, return zeros for all outputs
            return [0.0] * self.n_output
        
        # Take the first input and duplicate it to all outputs
        input_value = self._inputs[0] if self._inputs[0] is not None else 0.0
        
        # Return the same value duplicated n_output times
        return [input_value] * self.n_output

    def reset(self) -> None:
        """Resets the internal state of the block."""
        self._inputs = []


if __name__ == "__main__":
    # Test the Duplicate block
    duplicate_block = Duplicate()
    
    # Set parameters: duplicate to 4 outputs
    params = {'n_output': 4}
    duplicate_block.read_parameters(params)
    
    # Test with a single input
    inputs = [(5.0, 1.2)]
    duplicate_block.read_inputs(inputs)
    
    # Compute outputs
    output = duplicate_block.compute_outputs(time=0)
    print(f"Input: {inputs[0]}")
    print(f"Number of outputs: {duplicate_block.n_output}")
    print(f"Duplicated outputs: {output}")  # Expected: [5.0, 5.0, 5.0, 5.0]
    
    # Test with no input
    duplicate_block.read_inputs([])
    output_no_input = duplicate_block.compute_outputs(time=0)
    print(f"\nNo input case:")
    print(f"Outputs: {output_no_input}")  # Expected: [0.0, 0.0, 0.0, 0.0]