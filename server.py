#!/usr/bin/env python3
"""
Python server for LiteGraph PyG execution
This server allows the web interface to execute PyG scripts directly
without requiring manual terminal operations.
"""

import os
import sys
import json
import subprocess
import tempfile
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import threading
import time
import uuid
import shutil

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Store running processes
running_processes = {}

# Configuration
SERVER_PORT = 8080
WORKING_DIR = Path(__file__).parent.absolute()

# Environment detection functions
def detect_python_environments():
    """Detect available Python environments"""
    environments = []
    
    # Current Python executable
    current_python = sys.executable
    environments.append({
        'name': 'Current Python',
        'path': current_python,
        'type': 'system',
        'version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    })
    
    # Check for conda environments
    conda_envs = detect_conda_environments()
    environments.extend(conda_envs)
    
    # Check for virtual environments
    venv_envs = detect_virtual_environments()
    environments.extend(venv_envs)
    
    return environments

def detect_conda_environments():
    """Detect conda environments"""
    environments = []
    
    # Try to find conda in PATH first
    conda_cmd = shutil.which('conda')
    print(f"Conda command found in PATH: {conda_cmd}")
    
    # If not found in PATH, try common conda installation locations
    if not conda_cmd:
        print("Conda not found in PATH, checking common locations...")
        common_conda_paths = [
            Path.home() / 'anaconda3' / 'Scripts' / 'conda.exe',
            Path.home() / 'miniconda3' / 'Scripts' / 'conda.exe',
            Path('C:/ProgramData/Anaconda3/Scripts/conda.exe'),
            Path('C:/ProgramData/Miniconda3/Scripts/conda.exe'),
            Path('D:/anaconda3/Scripts/conda.exe'),
            Path('D:/miniconda3/Scripts/conda.exe'),
            Path('D:/TorchStudio/Scripts/conda.exe'),
            Path('C:/Users') / os.getenv('USERNAME', '') / 'anaconda3' / 'Scripts' / 'conda.exe',
            Path('C:/Users') / os.getenv('USERNAME', '') / 'miniconda3' / 'Scripts' / 'conda.exe'
        ]
        
        for conda_path in common_conda_paths:
            print(f"Checking: {conda_path}")
            if conda_path.exists():
                conda_cmd = str(conda_path)
                print(f"Found conda at: {conda_cmd}")
                break
    
    if not conda_cmd:
        print("Conda not found in PATH or common locations")
        return environments
    
    try:
        print(f"Running: {conda_cmd} env list --json")
        result = subprocess.run([conda_cmd, 'env', 'list', '--json'], 
                              capture_output=True, text=True, timeout=10)
        print(f"Conda command return code: {result.returncode}")
        print(f"Conda stdout: {result.stdout[:500]}...")  # First 500 chars
        if result.stderr:
            print(f"Conda stderr: {result.stderr}")
            
        if result.returncode == 0:
            conda_info = json.loads(result.stdout)
            env_paths = conda_info.get('envs', [])
            print(f"Found {len(env_paths)} conda environments")
            
            for env_path in env_paths:
                env_path = Path(env_path)
                env_name = env_path.name
                python_exe = env_path / 'python.exe' if os.name == 'nt' else env_path / 'bin' / 'python'
                
                print(f"Checking environment: {env_name} at {env_path}")
                print(f"Python executable path: {python_exe}")
                print(f"Python executable exists: {python_exe.exists()}")
                
                if python_exe.exists():
                    env_info = {
                        'name': f'conda: {env_name}',
                        'path': str(python_exe),
                        'type': 'conda',
                        'env_path': str(env_path)
                    }
                    environments.append(env_info)
                    print(f"Added conda environment: {env_info}")
                else:
                    print(f"Python executable not found for {env_name}")
        else:
            print(f"Conda command failed with return code {result.returncode}")
            
    except (subprocess.TimeoutExpired, json.JSONDecodeError, Exception) as e:
        print(f"Error detecting conda environments: {e}")
        import traceback
        traceback.print_exc()
    
    print(f"Total conda environments detected: {len(environments)}")
    return environments

def detect_virtual_environments():
    """Detect virtual environments in common locations"""
    environments = []
    
    # Common venv locations
    venv_locations = [
        Path.home() / '.virtualenvs',
        Path.cwd() / 'venv',
        Path.cwd() / '.venv',
        Path.cwd().parent / 'venv',
        Path.cwd().parent / '.venv'
    ]
    
    for location in venv_locations:
        if location.exists() and location.is_dir():
            if location.name in ['venv', '.venv']:
                # Single venv directory
                python_exe = location / 'Scripts' / 'python.exe' if os.name == 'nt' else location / 'bin' / 'python'
                if python_exe.exists():
                    environments.append({
                        'name': f'venv: {location.name}',
                        'path': str(python_exe),
                        'type': 'virtualenv',
                        'env_path': str(location)
                    })
            else:
                # Directory containing multiple venvs
                for subdir in location.iterdir():
                    if subdir.is_dir():
                        python_exe = subdir / 'Scripts' / 'python.exe' if os.name == 'nt' else subdir / 'bin' / 'python'
                        if python_exe.exists():
                            environments.append({
                                'name': f'venv: {subdir.name}',
                                'path': str(python_exe),
                                'type': 'virtualenv',
                                'env_path': str(subdir)
                            })
    
    return environments

@app.route('/')
def index():
    """Serve the main HTML file"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files (CSS, JS, etc.)"""
    return send_from_directory('.', filename)

@app.route('/api/execute', methods=['POST'])
def execute_script():
    """Execute a Python script with the exported graph data"""
    try:
        data = request.get_json()
        print(f"Received request data: {data}")
        
        if not data:
            error_msg = 'No data provided'
            print(f"Error: {error_msg}")
            return jsonify({'error': error_msg}), 400
            
        script_path = data.get('script_path')
        graph_data = data.get('graph_data')
        working_directory = data.get('working_directory', str(WORKING_DIR))
        python_executable = data.get('python_executable', sys.executable)
        
        print(f"Script path: {script_path}")
        print(f"Graph data keys: {list(graph_data.keys()) if graph_data else 'None'}")
        print(f"Working directory: {working_directory}")
        print(f"Python executable: {python_executable}")
        
        if not script_path:
            error_msg = 'No script path provided'
            print(f"Error: {error_msg}")
            return jsonify({'error': error_msg}), 400
            
        if not graph_data:
            error_msg = 'No graph data provided'
            print(f"Error: {error_msg}")
            return jsonify({'error': error_msg}), 400
        
        # Validate script path
        print(f"Validating script path: {script_path}")
        script_path = Path(script_path)
        print(f"Script path as Path object: {script_path}")
        print(f"Script path absolute: {script_path.absolute()}")
        print(f"Script path exists: {script_path.exists()}")
        
        if not script_path.exists():
            # Try relative to working directory
            relative_path = WORKING_DIR / script_path
            print(f"Trying relative path: {relative_path}")
            print(f"Relative path exists: {relative_path.exists()}")
            
            if relative_path.exists():
                script_path = relative_path
                print(f"Using relative path: {script_path}")
            else:
                # Search for the script in subdirectories of WORKING_DIR
                found_script = None
                script_name = script_path.name
                print(f"Searching for script '{script_name}' in subdirectories...")
                
                for subdir in WORKING_DIR.iterdir():
                    if subdir.is_dir():
                        potential_script = subdir / script_name
                        print(f"Checking: {potential_script}")
                        if potential_script.exists():
                            found_script = potential_script
                            print(f"Found script in subdirectory: {found_script}")
                            break
                
                # If not found in subdirectories, search in sibling directories
                if not found_script:
                    project_root = WORKING_DIR.parent
                    print(f"Searching for script '{script_name}' in sibling directories of project root: {project_root}...")
                    
                    for sibling_dir in project_root.iterdir():
                        if sibling_dir.is_dir() and sibling_dir != WORKING_DIR:
                            potential_script = sibling_dir / script_name
                            print(f"Checking sibling: {potential_script}")
                            if potential_script.exists():
                                found_script = potential_script
                                print(f"Found script in sibling directory: {found_script}")
                                break
                
                if found_script:
                    script_path = found_script
                    print(f"Using found script: {script_path}")
                else:
                    error_msg = f'Script file not found: {script_path} (also tried: {relative_path}, subdirectories, and sibling directories)'
                    print(f"Error: {error_msg}")
                    return jsonify({'error': error_msg}), 400
            
        if not script_path.suffix == '.py':
            error_msg = 'Script must be a Python file (.py)'
            print(f"Error: {error_msg}")
            return jsonify({'error': error_msg}), 400
        
        # Create temporary file for graph data
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
            json.dump(graph_data, temp_file, indent=2)
            temp_graph_path = temp_file.name
        
        try:
            # Change to script's directory as working directory
            script_directory = script_path.parent
            original_cwd = os.getcwd()
            os.chdir(script_directory)
            print(f"Changed working directory to: {script_directory}")
            
            # Execute the script
            print(f"Executing: {python_executable} {script_path} {temp_graph_path}")
            cmd = [python_executable, str(script_path), temp_graph_path]
            
            # Set environment variables for UTF-8 encoding
            env = os.environ.copy()
            env['PYTHONIOENCODING'] = 'utf-8'
            env['PYTHONLEGACYWINDOWSSTDIO'] = '0'
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=script_directory,
                env=env
            )
            
            # Wait for process to complete with timeout
            try:
                stdout, stderr = process.communicate(timeout=30)  # 30 second timeout
                return_code = process.returncode
                
                result = {
                    'success': return_code == 0,
                    'return_code': return_code,
                    'stdout': stdout,
                    'stderr': stderr,
                    'script_path': str(script_path),
                    'graph_file': temp_graph_path
                }
                
                return jsonify(result)
                
            except subprocess.TimeoutExpired:
                process.kill()
                return jsonify({
                    'error': 'Script execution timed out (30 seconds)',
                    'success': False
                }), 408
                
        finally:
            # Restore original working directory
            os.chdir(original_cwd)
            
            # Clean up temporary file
            try:
                os.unlink(temp_graph_path)
            except:
                pass  # Ignore cleanup errors
                
    except Exception as e:
        return jsonify({
            'error': f'Server error: {str(e)}',
            'success': False
        }), 500

@app.route('/api/execute_async', methods=['POST'])
def execute_script_async():
    """Execute a Python script asynchronously for long-running processes"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        script_path = data.get('script_path')
        graph_data = data.get('graph_data')
        working_directory = data.get('working_directory', str(WORKING_DIR))
        python_executable = data.get('python_executable', sys.executable)
        
        if not script_path:
            return jsonify({'error': 'No script path provided'}), 400
            
        if not graph_data:
            return jsonify({'error': 'No graph data provided'}), 400
        
        # Validate script path
        script_path = Path(script_path)
        if not script_path.exists():
            # Try relative to working directory
            relative_path = WORKING_DIR / script_path
            
            if relative_path.exists():
                script_path = relative_path
            else:
                # Search for the script in subdirectories of WORKING_DIR
                found_script = None
                script_name = script_path.name
                
                for subdir in WORKING_DIR.iterdir():
                    if subdir.is_dir():
                        potential_script = subdir / script_name
                        if potential_script.exists():
                            found_script = potential_script
                            break
                
                # If not found in subdirectories, search in sibling directories
                if not found_script:
                    project_root = WORKING_DIR.parent
                    
                    for sibling_dir in project_root.iterdir():
                        if sibling_dir.is_dir() and sibling_dir != WORKING_DIR:
                            potential_script = sibling_dir / script_name
                            if potential_script.exists():
                                found_script = potential_script
                                break
                
                if found_script:
                    script_path = found_script
                else:
                    return jsonify({'error': f'Script file not found: {script_path} (also tried: {relative_path}, subdirectories, and sibling directories)'}), 400
            
        if not script_path.suffix == '.py':
            return jsonify({'error': 'Script must be a Python file (.py)'}), 400
        
        # Create temporary file for graph data
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
            json.dump(graph_data, temp_file, indent=2)
            temp_graph_path = temp_file.name
        
        # Generate unique process ID
        process_id = str(uuid.uuid4())
        
        # Start process asynchronously
        def run_async():
            try:
                # Change to script's directory as working directory
                script_directory = script_path.parent
                original_cwd = os.getcwd()
                os.chdir(script_directory)
                
                cmd = [python_executable, str(script_path), temp_graph_path]
                
                # Set environment variables for UTF-8 encoding
                env = os.environ.copy()
                env['PYTHONIOENCODING'] = 'utf-8'
                env['PYTHONLEGACYWINDOWSSTDIO'] = '0'
                
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    cwd=script_directory,
                    env=env
                )
                
                running_processes[process_id]['process'] = process
                running_processes[process_id]['status'] = 'running'
                
                stdout, stderr = process.communicate()
                return_code = process.returncode
                
                running_processes[process_id].update({
                    'status': 'completed',
                    'return_code': return_code,
                    'stdout': stdout,
                    'stderr': stderr,
                    'success': return_code == 0
                })
                
            except Exception as e:
                running_processes[process_id].update({
                    'status': 'error',
                    'error': str(e),
                    'success': False
                })
            finally:
                os.chdir(original_cwd)
                try:
                    os.unlink(temp_graph_path)
                except:
                    pass
        
        # Initialize process info
        running_processes[process_id] = {
            'status': 'starting',
            'script_path': str(script_path),
            'graph_file': temp_graph_path,
            'start_time': time.time()
        }
        
        # Start thread
        thread = threading.Thread(target=run_async)
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'process_id': process_id,
            'status': 'started',
            'message': 'Script execution started'
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Server error: {str(e)}',
            'success': False
        }), 500

@app.route('/api/status/<process_id>', methods=['GET'])
def get_process_status(process_id):
    """Get the status of an asynchronous process"""
    if process_id not in running_processes:
        return jsonify({'error': 'Process not found'}), 404
    
    process_info = running_processes[process_id].copy()
    
    # Remove the actual process object from response
    if 'process' in process_info:
        del process_info['process']
    
    return jsonify(process_info)

@app.route('/api/stop/<process_id>', methods=['POST'])
def stop_process(process_id):
    """Stop a running process"""
    if process_id not in running_processes:
        return jsonify({'error': 'Process not found'}), 404
    
    process_info = running_processes[process_id]
    
    if 'process' in process_info and process_info['status'] == 'running':
        try:
            process_info['process'].terminate()
            process_info['status'] = 'terminated'
            return jsonify({'message': 'Process terminated successfully'})
        except Exception as e:
            return jsonify({'error': f'Failed to terminate process: {str(e)}'}), 500
    else:
        return jsonify({'error': 'Process is not running'}), 400

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Server is running'}), 200

@app.route('/api/environments', methods=['GET'])
def list_environments():
    """List available Python environments"""
    try:
        environments = detect_python_environments()
        return jsonify({'environments': environments}), 200
    except Exception as e:
        print(f"Error listing environments: {e}")
        return jsonify({'error': f'Failed to list environments: {str(e)}'}), 500

if __name__ == '__main__':
    print(f"Starting LiteGraph PyG Server...")
    print(f"Working directory: {WORKING_DIR}")
    print(f"Server will be available at: http://localhost:{SERVER_PORT}")
    print(f"Open your browser and navigate to: http://localhost:{SERVER_PORT}")
    print("\nPress Ctrl+C to stop the server")
    
    try:
        app.run(host='0.0.0.0', port=SERVER_PORT, debug=False)
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Server error: {e}")