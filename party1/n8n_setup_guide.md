# n8n MCP Tools Integration Guide

This guide explains how to configure n8n to use the Party1 MCP server as a tools node.

## Overview

The MCP server provides three main tools that can be integrated into n8n workflows:
- **compute_mpc**: Perform MPC computations with party1 data
- **get_party_data**: Retrieve party1's private data
- **validate_input**: Validate input data for MPC operations

## Setup Steps

### 1. Start the n8n MCP Server

```bash
cd party1
pdm run python n8n_mcp_server.py
```

The server will start on `http://localhost:8003` (configurable via `N8N_MCP_PORT`)

### 2. Verify Server is Running

```bash
# Check server status
curl http://localhost:8003/health

# List available tools
curl http://localhost:8003/n8n/tools

# List available resources
curl http://localhost:8003/n8n/resources
```

### 3. Configure n8n HTTP Request Nodes

#### Tool 1: Compute MPC

**Node Configuration:**
- **Method**: POST
- **URL**: `http://localhost:8003/mcp/tools/compute_mpc`
- **Headers**: `Content-Type: application/json`

**Request Body:**
```json
{
  "operation": "add",
  "values": [1, 2, 3, 4, 5],
  "threshold": 3
}
```

**Available Operations:**
- `add`: Sum of values
- `multiply`: Product of values
- `compare`: Compare values against threshold
- `sum`: Sum of values
- `average`: Mean of values

#### Tool 2: Get Party Data

**Node Configuration:**
- **Method**: POST
- **URL**: `http://localhost:8003/mcp/tools/get_party_data`
- **Headers**: `Content-Type: application/json`

**Request Body:**
```json
{
  "data_type": "financial",
  "format": "json"
}
```

**Available Data Types:**
- `financial`: Income, expenses, savings, investments
- `personal`: Age, location, occupation
- `preferences`: Risk tolerance, investment style, time horizon

**Available Formats:**
- `json`: JSON format (default)
- `csv`: CSV format
- `xml`: XML format

#### Tool 3: Validate Input

**Node Configuration:**
- **Method**: POST
- **URL**: `http://localhost:8003/mcp/tools/validate_input`
- **Headers**: `Content-Type: application/json`

**Request Body:**
```json
{
  "data": [10, 20, 30, 40, 50],
  "constraints": {
    "min_value": 0,
    "max_value": 100,
    "required_length": 5
  }
}
```

## n8n Workflow Examples

### Example 1: Basic MPC Computation

```json
{
  "name": "Basic MPC Computation",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "url": "http://localhost:8003/mcp/tools/compute_mpc",
        "sendBody": true,
        "bodyParameters": {
          "parameters": [
            {
              "name": "operation",
              "value": "add"
            },
            {
              "name": "values",
              "value": "={{ $json.values || [1, 2, 3, 4, 5] }}"
            }
          ]
        }
      },
      "name": "Compute MPC",
      "type": "n8n-nodes-base.httpRequest"
    }
  ]
}
```

### Example 2: Data Retrieval and Processing

```json
{
  "name": "Data Retrieval and Processing",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "url": "http://localhost:8003/mcp/tools/get_party_data",
        "sendBody": true,
        "bodyParameters": {
          "parameters": [
            {
              "name": "data_type",
              "value": "financial"
            }
          ]
        }
      },
      "name": "Get Financial Data",
      "type": "n8n-nodes-base.httpRequest"
    },
    {
      "parameters": {
        "jsCode": "// Process financial data\nconst data = $json;\nconst netWorth = data.income + data.savings + data.investments - data.expenses;\nreturn {\n  json: {\n    ...data,\n    netWorth,\n    processed: true\n  }\n}"
      },
      "name": "Process Data",
      "type": "n8n-nodes-base.code"
    }
  ]
}
```

### Example 3: Validation Workflow

```json
{
  "name": "Validation Workflow",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "url": "http://localhost:8003/mcp/tools/validate_input",
        "sendBody": true,
        "bodyParameters": {
          "parameters": [
            {
              "name": "data",
              "value": "={{ $json.values || [10, 20, 30, 40, 50] }}"
            },
            {
              "name": "constraints",
              "value": "={{ { \"min_value\": 0, \"max_value\": 100 } }}"
            }
          ]
        }
      },
      "name": "Validate Input",
      "type": "n8n-nodes-base.httpRequest"
    },
    {
      "parameters": {
        "conditions": {
          "conditions": [
            {
              "leftValue": "={{ $json.is_valid }}",
              "rightValue": true,
              "operator": {
                "type": "boolean",
                "operation": "equal"
              }
            }
          ]
        }
      },
      "name": "Check Validation",
      "type": "n8n-nodes-base.if"
    }
  ]
}
```

## Environment Variables

Configure the server using environment variables:

```bash
# Set custom port
export N8N_MCP_PORT=8004

# Start server
pdm run python n8n_mcp_server.py
```

## Error Handling

The MCP server returns proper HTTP status codes:

- **200**: Success
- **400**: Bad Request (invalid parameters)
- **500**: Internal Server Error

Example error response:
```json
{
  "detail": "Values array is required"
}
```

## Security Considerations

1. **Network Access**: The server runs on `0.0.0.0` by default. Consider firewall rules.
2. **Authentication**: Add authentication if needed for production use.
3. **Data Privacy**: The server contains mock data. Replace with real data sources.

## Troubleshooting

### Common Issues

1. **Connection Refused**: Ensure the MCP server is running
2. **Port Already in Use**: Change the port using `N8N_MCP_PORT`
3. **Invalid JSON**: Check request body format

### Debug Commands

```bash
# Check if server is running
lsof -i :8003

# Test endpoints
curl -X POST http://localhost:8003/mcp/tools/compute_mpc \
  -H "Content-Type: application/json" \
  -d '{"operation": "add", "values": [1, 2, 3]}'

# Check server logs
tail -f party1_mcp.log
```

## Integration with Other Tools

The MCP server can be integrated with:
- **n8n**: As shown in this guide
- **Zapier**: Using webhooks
- **Make (Integromat)**: Using HTTP modules
- **Custom Applications**: Using the REST API

## Next Steps

1. **Customize Tools**: Modify the tool implementations in `n8n_mcp_server.py`
2. **Add Authentication**: Implement API key or OAuth authentication
3. **Connect Real Data**: Replace mock data with real data sources
4. **Scale**: Deploy to production with proper monitoring 