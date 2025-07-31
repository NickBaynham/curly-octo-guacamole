# Party2 Weather MCP Server

This is a Multi-Party Computation (MCP) server for Party2 that provides weather information services.

## Features

- **Weather API**: Retrieve weather information for different countries
- **MCP Integration**: Full MCP protocol support with FastApiMCP
- **Health Monitoring**: Built-in health check endpoints
- **Configurable Port**: Environment variable support for port configuration

## Quick Start

### 1. Start the Server

```bash
cd party2
pdm run python main.py
```

The server will start on `http://localhost:9001` by default.

### 2. Configure Custom Port (Optional)

```bash
export PARTY2_PORT=9002
pdm run python main.py
```

### 3. Verify Server is Running

```bash
# Health check
curl http://localhost:9001/health

# Test weather endpoint
curl http://localhost:9001/weather/USA

# Check MCP status
curl http://localhost:9001/mcp/status
```

## API Endpoints

### Core Endpoints

- `GET /` - Server root
- `GET /health` - Health check
- `GET /mcp/status` - MCP server status

### Weather API

- `GET /weather/{country}` - Get weather information for a country

**Example Response:**
```json
{
  "country": "USA",
  "temperature": "25°C",
  "condition": "Sunny"
}
```

## MCP Integration

The server uses FastApiMCP to provide MCP protocol support:

- **HTTP Transport**: Mounted using `mount_http()`
- **Tool Registration**: Weather endpoint automatically registered as MCP tool
- **Operation ID**: `get_weather_info`

### MCP Tool Details

**Tool Name**: `get_weather_info`
**Description**: Retrieves the current weather information for a given country
**Parameters**: 
- `country` (string): The country to get weather for

## Configuration

### Environment Variables

- `PARTY2_PORT`: Server port (default: 9001)

### Server Configuration

The server is configured with:
- **Host**: `0.0.0.0` (accessible from any IP)
- **Port**: Configurable via `PARTY2_PORT`
- **Protocol**: HTTP/HTTPS
- **MCP Transport**: HTTP

## Error Handling

The server returns proper HTTP status codes:
- **200**: Success
- **404**: Country not found or endpoint not available
- **500**: Internal server error

## Testing

### Manual Testing

```bash
# Test health endpoint
curl http://localhost:9001/health

# Test weather for USA
curl http://localhost:9001/weather/USA

# Test weather for unknown country
curl http://localhost:9001/weather/UnknownCountry
```

### Automated Testing

```bash
# Run with custom port
PARTY2_PORT=9002 pdm run python main.py

# Test in background
pdm run python main.py &
sleep 3
curl http://localhost:9001/health
```

## Troubleshooting

### Common Issues

1. **Port Already in Use**:
   ```bash
   # Check what's using the port
   lsof -i :9001
   
   # Kill the process
   kill <PID>
   
   # Or use a different port
   export PARTY2_PORT=9002
   ```

2. **Module Not Found**:
   ```bash
   # Ensure you're in the virtual environment
   pdm run python main.py
   ```

3. **MCP Connection Issues**:
   - Verify the server is running: `curl http://localhost:9001/health`
   - Check MCP status: `curl http://localhost:9001/mcp/status`
   - Ensure proper mounting: `mount_http()` is called

### Debug Commands

```bash
# Check server logs
pdm run python main.py

# Test endpoints
curl -v http://localhost:9001/weather/USA

# Check process
ps aux | grep "main.py" | grep -v grep
```

## Architecture

```
Party2 MCP Server
├── FastAPI Application
│   ├── Weather Endpoint (/weather/{country})
│   ├── Health Check (/health)
│   └── MCP Status (/mcp/status)
├── FastApiMCP Integration
│   ├── HTTP Transport (mount_http)
│   └── Tool Registration
└── Uvicorn Server
    ├── Host: 0.0.0.0
    └── Port: 9001 (configurable)
```

## Integration with Other Services

This server can be integrated with:
- **n8n**: Using HTTP Request nodes
- **Zapier**: Using webhooks
- **Custom Applications**: Using the REST API
- **MCP Clients**: Using the MCP protocol

## Security Considerations

1. **Network Access**: Server runs on `0.0.0.0` by default
2. **Authentication**: No authentication implemented (add for production)
3. **Data Privacy**: Contains mock weather data (replace with real API)

## Next Steps

1. **Add Real Weather API**: Replace mock data with actual weather service
2. **Implement Authentication**: Add API key or OAuth authentication
3. **Add More Endpoints**: Expand weather functionality
4. **Production Deployment**: Configure for production environment 