# LiteGraph for 🐷PyG

A LiteGraph-based graph editor for creating and editing PyInGraph (https://pypi.org/project/pyingraph) computational workflows. This tool provides an intuitive drag-and-drop interface to build complex python algorithm pipelines that can be executed with the PyInGraph framework.

## What is this?

LiteGraph for PyG is a browser-based visual editor that allows you to:
- **Create computational graphs** by dragging and dropping nodes
- **Connect algorithm blocks** with visual links to define data flow
- **Configure node parameters** through an intuitive interface
- **Export graphs** to PyInGraph JSON format for execution
- **Select and run** a user-defined graph-solving script
- **Load and save** your work for later editing

## Quick Start

### Prerequisites
- A modern browser, Chrome is recommended
- A python running environment (>= python 3.7) with `pyingraph` package installed, check [PyInGraph package on PyPI](https://pypi.org/project/pyingraph)
- A local project folder, containing your PyInGraph-compatible Python modules (for the example below, all are in the `📁local_modules/` folder) as well as the global graph-computing script (for the example below, the `📄run_graph.py` script):

```
📁your_project_folder/
├── 📁local_modules/
│   ├── 📄mod_1.py
│   └── 📄mod_2.py
│   └── 📁mod_sub_folder/
│       ├── 📄mod_3.py
│       └── ...
└── 📄run_graph.py
```

### Steps

1. **Open the tool**: Open `index.html` in your web browser
2. **Get nodes from modules**: 
   - In the left pane, use the "🔍 Get PyG Nodes from Folder" (orange button) to auto-detect your Python modules in the selected folder
   - After parsing the modules, the detected nodes will appear below the "🔍 Get PyG Nodes from Folder" button
   - Drag nodes from the left panel onto the canvas
3. **Connect nodes**: Click and drag from output ports to input ports. For each node, the number of input and output ports can be modified in the node's widget.
4. **Configure parameters**: Set nodes' parameters (that appear in the node's widget)
5. **Run**: In the top pane, use "▶️ Run Selected PyG Script" (green button), a dialogue appears, where we
   1. selects the graph-computing script (e.g., the `📄run_graph.py` script in the example above)
   2. export the graph to the project folder  (e.g., `📁your_project_folder/`)
   3. start a terminal from the project folder, activate the python environment (e.g., `conda activate your_env`)
   4. copy the dialogue-generated command
   5. paste the generated command to the terminal to run the graph. (**Due to browser security restrictions, we cannot directly execute Python scripts from the browser. You'll need to run this command manually in your terminal/command prompt.**)

### Other Functions
- **Load/Save Designs**: Use `💾 Save LiteGraph JSON` and `📁 Open LiteGraph JSON` in the top pane to save and load your work
- **Export to PyG Graph**: Use `📤 Export to PyG Graph JSON` to export the LiteGraph file to PyInGraph graph format (in case you are to run the graph on another machine)
- **Load/Save User-Defined Nodes**:
  - Each node dragged on canvas has a `Save Node` button on the node's widget. After modifying the node's parameters (e.g., number of inputs/outputs, node-specific parameters, etc.), you can click `Save Node` to save it to the `💾 Saved Nodes` pane (bottom left). Nodes in that pane can be dragged back to the canvas to facilitate graph design
  - After having a set of nodes in the pane, you can use `📤 Save Loaded Nodes as JSON` (button above the saved nodes), to store the node definitions in a JSON file.
  - You can also use `📥 Load Nodes from JSON` (button above the saved nodes), to load the saved JSON file containing node definitions. This helps restoring the graph-design context.

## Key Features

### ➿ Cyclic graph!
Unlike [ComfyUI](https://www.comfy.org/) that is designed for acyclic workflows, LiteGraph for PyG (with PyInGraph) does not restrict the graph to be acyclic. How to address the graph computation is up to the graph-computing script.

### 🔧 Node Management
- **Auto-discovery**: Automatically finds PyInGraph-compatible classes in your Python files
- **Parameter detection**: Extracts configurable parameters from your code
- **Save/Load nodes**: Store frequently used node configurations

### 📊 Visual Editing
- **Drag-and-drop interface**: Easy node placement and connection
- **Real-time preview**: See your graph structure as you build it

### 💾 File Operations
- **Open/Save**: Load and save LiteGraph JSON files
- **Export**: Convert to PyInGraph format for execution
- **New graph**: Start fresh projects

### ▶️ Execution Integration
- **Run with script**: Execute your graphs directly from the editor
- **PyInGraph compatibility**: Seamless integration with the PyInGraph execution engine

## Supported Node Types

- **PyG Nodes**: Custom algorithm blocks that inherit from `BlockBase`, see [PyInGraph package on PyPI](https://pypi.org/project/pyingraph)


## File Structure

```
litegraph-PyG/
├── index.html          # Main application
├── litegraph.js        # LiteGraph library
├── litegraph.css       # Styling
└── README.md           # This file
```

## Getting Help

For issues with:
- **Graph execution**: Check the PyInGraph documentation
- **Node creation**: Ensure your classes inherit from `BlockBase`
- **Parameter detection**: Verify your `attrNamesArr` definitions

---

*Part of the PyInGraph project - A Python framework for visual computational graphs*