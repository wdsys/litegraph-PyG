#!/usr/bin/env python3
"""
Example PyG script for testing the LiteGraph PyG server functionality.
This script demonstrates how to process graph data exported from LiteGraph.
"""

import sys
import json
from pathlib import Path

def main():
    if len(sys.argv) != 2:
        print("Usage: python example_script.py <graph_file.json>")
        sys.exit(1)
    
    graph_file = Path(sys.argv[1])
    
    if not graph_file.exists():
        print(f"Error: Graph file '{graph_file}' not found.")
        sys.exit(1)
    
    try:
        # Load the graph data
        with open(graph_file, 'r') as f:
            graph_data = json.load(f)
        
        print("🎉 Successfully loaded graph data!")
        print(f"📊 Graph contains {len(graph_data.get('nodes', []))} nodes and {len(graph_data.get('edges', []))} edges")
        
        # Process nodes
        print("\n📋 Node Information:")
        for i, node in enumerate(graph_data.get('nodes', []), 1):
            print(f"  {i}. {node.get('name', 'Unnamed')} (ID: {node.get('id', 'N/A')})")
            if node.get('class_name'):
                print(f"     Class: {node.get('class_name')}")
            if node.get('parameters'):
                print(f"     Parameters: {node.get('parameters')}")
        
        # Process edges
        if graph_data.get('edges'):
            print("\n🔗 Edge Information:")
            for i, edge in enumerate(graph_data.get('edges', []), 1):
                source = edge.get('source_node_id', 'N/A')
                target = edge.get('target_node_id', 'N/A')
                print(f"  {i}. {source} → {target}")
        
        # Metadata
        if graph_data.get('metadata'):
            metadata = graph_data['metadata']
            print("\n📝 Metadata:")
            print(f"  Version: {metadata.get('version', 'N/A')}")
            print(f"  Description: {metadata.get('description', 'N/A')}")
            print(f"  Created: {metadata.get('created', 'N/A')}")
        
        print("\n✅ Script execution completed successfully!")
        
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing JSON: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()