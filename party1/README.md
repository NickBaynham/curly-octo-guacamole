# Party1 MCP Server

This is a FastAPI-based MCP (Model Context Protocol) server for Party1 in a multi-party computation setup.

## Features

- ✅ **FastAPI Integration**: Built on FastAPI for high-performance API serving
- ✅ **MCP Protocol Support**: Implements the Model Context Protocol for AI model integration
- ✅ **Health Monitoring**: Built-in health check endpoints
- ✅ **Status Reporting**: MCP server status and capabilities endpoint
- ✅ **Configurable Port**: Environment variable support for port configuration

## API Endpoints

### Core Endpoints

- `GET /` - Root endpoint with server status
- `GET /health` - Health check endpoint
- `GET /mcp/status` - MCP server status and capabilities

### Example Responses

**Root Endpoint:**
```json
{
  "message": "Party Ready",
  "mcp_enabled": true
}
```

**Health Check:**
```json
{
  "status": "healthy",
  "mcp_server": "running"
}
```

**MCP Status:**
```json
{
  "server_name": "party1",
  "server_description": "Party 1 MCP Server",
  "server_version": "1.0.0",
  "capabilities": {
    "tools": {},
    "resources": {}
  }
}
```

## Running the Server

### Prerequisites

1. Install dependencies:
```bash
pdm add fastapi-mcp
```

2. **Port Configuration**: The server uses port 8002 by default, but you can configure it via environment variable

### Starting the Server

#### Option 1: Default port (8002) - Recommended
```bash
cd party1
pdm run python main.py
```
Server will run on `http://localhost:8002`

#### Option 2: Custom port via environment variable
```bash
cd party1
PARTY1_PORT=8003 pdm run python main.py
```
Server will run on `http://localhost:8003`

#### Option 3: From root directory
```bash
pdm run python party1/main.py
```
Server will run on `http://localhost:8002`

#### Option 4: Check for port conflicts first
```bash
lsof -i :8001  # Check if port 8001 is in use
lsof -i :8002  # Check if port 8002 is in use
```

### Environment Variables

- `PARTY1_PORT`: Set the port number (default: 8002)
  ```bash
  export PARTY1_PORT=8003
  pdm run python main.py
  ```

### Testing

Test the server endpoints:
```bash
# Root endpoint
curl http://localhost:8002/

# Health check
curl http://localhost:8002/health

# MCP status
curl http://localhost:8002/mcp/status
```

### Troubleshooting Port Conflicts

If you get a port conflict error:

1. **Check what's using the port:**
   ```bash
   lsof -i :8002
   ```

2. **Kill the process if needed:**
   ```bash
   kill <PID>
   ```

3. **Use a different port:**
   ```bash
   PARTY1_PORT=8003 pdm run python main.py
   ```

## MCP Integration

The server is configured to work with MCP clients and can be integrated into AI model workflows. The MCP server provides:

- Standard MCP protocol endpoints
- Server capabilities reporting
- Tool and resource management
- SSE (Server-Sent Events) support for real-time communication

## Configuration

The server uses default MCP configuration. To customize:

1. Modify the `mcp_config.json` file
2. Update the server capabilities in `main.py`
3. Add custom tools and resources as needed

## Development

To extend the server:

1. Add new API endpoints in `main.py`
2. Implement MCP tools in the capabilities
3. Add custom resources for data sharing
4. Configure authentication if needed

## Architecture

```
FastAPI App
├── MCP Server (FastApiMCP)
├── Health Endpoints
├── Status Endpoints
└── Custom API Endpoints
```

## Quick Start

1. **Navigate to the party1 directory:**
   ```bash
   cd party1
   ```

2. **Start the server:**
   ```bash
   pdm run python main.py
   ```

3. **Test the server:**
   ```bash
   curl http://localhost:8002/
   ```

The server is ready for integration with MCP clients and can be extended with additional functionality as needed. 