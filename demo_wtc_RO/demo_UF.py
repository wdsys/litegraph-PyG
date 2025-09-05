#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple graph simulation solver
Extracted from system_graph_load.py main section
"""

from pyingraph import GraphLoader
import numpy as np

def main(argv=None):
    
    file_name = 'pyingraph_export.json'
    
    # Check if a file name was provided as an argument
    if argv and len(argv) > 0:
        file_name = argv[0]

    loader = GraphLoader(file_name, flag_remote=False)
    # load graph
    loader.load()
    
    # get nx graph
    nx_graph = loader.get_nx_graph()
    
    # visualize the graph
    loader.visualize_graph()
    
    # return
    
    # debug print
    print("\033[1;32m🚀 Before Traverse: \033[1;33mStarting Graph Simulation\033[0m")
    
    # simulation (dynamic!)
    loader.reset_graph_edges()
    for _ in range(10):
        # traverse the graph with a built-in, simple algorithm
        loader.simple_traverse_graph(time=0)

if __name__ == '__main__':
    import sys
    # Pass command line arguments (excluding script name)
    main(sys.argv[1:])