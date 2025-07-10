# LiteGraph PyG Server

This server enables direct execution of PyG scripts from the web interface, eliminating the need for manual terminal operations.

## Setup Instructions

### 1. Install Dependencies

First, install the required Python packages:

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install Flask==2.3.3 Flask-CORS==4.0.0
```

### 2. Start the Server

Run the server from the project directory:

```bash
python server.py
```

The server will start on `http://localhost:8080` and serve both the web interface and API endpoints.

### 3. Access the Web Interface

Open your browser and navigate to:

```
http://localhost:8080
```

## Features

### Server-Based Execution
- **Direct Script Execution**: Run PyG scripts directly from the web interface
- **Real-time Output**: See script output and errors immediately
- **Async Execution**: Support for long-running scripts
- **Automatic Graph Export**: No need to manually export graph files

### Manual Execution (Fallback)
- **Traditional Method**: Export graph and copy command for manual execution
- **Browser Compatibility**: Works even if server is not available

## How to Use

1. **Start the Server**: Run `python server.py`
2. **Open Web Interface**: Navigate to `http://localhost:8080`
3. **Create Your Graph**: Use the LiteGraph interface to build your PyG workflow
4. **Run Script**: Click "▶️ Run Selected PyG Script" button
5. **Choose Execution Method**:
   - **🚀 Run via Server**: Direct execution with real-time output
   - **⚡ Run Async**: For long-running scripts
   - **📋 Manual Terminal**: Traditional copy-paste method

## API Endpoints

- `GET /api/health` - Check server status
- `POST /api/execute` - Execute script synchronously (30s timeout)
- `POST /api/execute_async` - Execute script asynchronously
- `GET /api/status/<process_id>` - Get async process status
- `POST /api/stop/<process_id>` - Stop running async process

## Security Notes

- The server runs locally on `localhost:8080`
- Only Python scripts (.py files) can be executed
- Scripts are executed in the server's working directory
- Temporary graph files are automatically cleaned up

## Troubleshooting

### Server Not Available
- Make sure you've started the server with `python server.py`
- Check that port 8080 is not being used by another application
- Verify Flask and Flask-CORS are installed

### Script Execution Errors
- Check the script path is correct and the file exists
- Ensure your Python environment has all required dependencies
- Review the error output in the execution panel

### Browser Compatibility
- Use modern browsers (Chrome 86+, Edge 86+, Firefox 90+)
- File System Access API is required for script selection
- CORS must be enabled (handled automatically by the server)

## Development

To modify the server:

1. Edit `server.py` for backend changes
2. Edit `index.html` for frontend changes
3. Restart the server to apply backend changes
4. Refresh the browser to apply frontend changes

The server includes CORS headers and serves static files, making it suitable for development and testing.