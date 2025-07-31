from fastapi import FastAPI, HTTPException
import uvicorn
import logging
import os
import json
from typing import Dict, Any, List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mock party1 data for demonstration
PARTY1_DATA = {
    "financial": {
        "income": 75000,
        "expenses": 45000,
        "savings": 30000,
        "investments": 150000
    },
    "personal": {
        "age": 35,
        "location": "New York",
        "occupation": "Software Engineer"
    },
    "preferences": {
        "risk_tolerance": "medium",
        "investment_style": "balanced",
        "time_horizon": "10-15 years"
    }
}

app = FastAPI(title="n8n MCP Tools API", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "n8n MCP Tools API Ready", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "server": "n8n-mcp-tools"}

@app.get("/tools")
async def list_tools():
    """List available tools for n8n integration."""
    return {
        "tools": [
            {
                "name": "compute_mpc",
                "description": "Perform MPC computations with party1 data",
                "endpoint": "/tools/compute_mpc",
                "method": "POST",
                "parameters": {
                    "operation": "string (add, multiply, compare, sum, average)",
                    "values": "array of numbers",
                    "threshold": "number (optional, for compare operation)"
                }
            },
            {
                "name": "get_party_data",
                "description": "Retrieve party1's private data",
                "endpoint": "/tools/get_party_data",
                "method": "POST",
                "parameters": {
                    "data_type": "string (financial, personal, preferences)",
                    "format": "string (json, csv, xml, default: json)"
                }
            },
            {
                "name": "validate_input",
                "description": "Validate input data for MPC operations",
                "endpoint": "/tools/validate_input",
                "method": "POST",
                "parameters": {
                    "data": "array of numbers",
                    "constraints": "object (min_value, max_value, required_length)"
                }
            }
        ]
    }

@app.get("/resources")
async def list_resources():
    """List available resources for n8n integration."""
    return {
        "resources": [
            {
                "name": "party1_data",
                "description": "Access to party1's private data",
                "uri": "party1://data",
                "types": ["financial", "personal", "preferences"]
            },
            {
                "name": "mpc_results",
                "description": "MPC computation results",
                "uri": "party1://results",
                "operations": ["add", "multiply", "compare", "sum", "average"]
            }
        ]
    }

@app.post("/tools/compute_mpc")
async def compute_mpc_tool(request: Dict[str, Any]):
    """Perform MPC computations with party1 data."""
    try:
        operation = request.get("operation")
        values = request.get("values", [])
        threshold = request.get("threshold")
        
        if not values:
            raise HTTPException(status_code=400, detail="Values array is required")
        
        if not isinstance(values, list):
            raise HTTPException(status_code=400, detail="Values must be an array")
        
        result = None
        
        if operation == "add":
            result = sum(values)
        elif operation == "multiply":
            result = 1
            for v in values:
                result *= v
        elif operation == "compare":
            if threshold is None:
                raise HTTPException(status_code=400, detail="Threshold required for compare operation")
            result = [1 if v > threshold else 0 for v in values]
        elif operation == "sum":
            result = sum(values)
        elif operation == "average":
            result = sum(values) / len(values) if values else 0
        else:
            raise HTTPException(status_code=400, detail=f"Unknown operation: {operation}")
        
        return {
            "result": result,
            "operation": operation,
            "input_values": values,
            "party1_contribution": True,
            "status": "success"
        }
        
    except Exception as e:
        logger.error(f"Error in compute_mpc_tool: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tools/get_party_data")
async def get_party_data_tool(request: Dict[str, Any]):
    """Retrieve party1's private data."""
    try:
        data_type = request.get("data_type")
        output_format = request.get("format", "json")
        
        if not data_type:
            raise HTTPException(status_code=400, detail="data_type is required")
        
        if data_type not in PARTY1_DATA:
            raise HTTPException(status_code=400, detail=f"Unknown data type: {data_type}")
        
        data = PARTY1_DATA[data_type]
        
        if output_format == "json":
            return {
                "data": data,
                "data_type": data_type,
                "format": output_format,
                "status": "success"
            }
        elif output_format == "csv":
            # Convert to CSV format
            csv_lines = []
            for key, value in data.items():
                csv_lines.append(f"{key},{value}")
            return {
                "csv_data": "\n".join(csv_lines),
                "data_type": data_type,
                "format": output_format,
                "status": "success"
            }
        elif output_format == "xml":
            # Convert to XML format
            xml_parts = ["<data>"]
            for key, value in data.items():
                xml_parts.append(f"  <{key}>{value}</{key}>")
            xml_parts.append("</data>")
            return {
                "xml_data": "\n".join(xml_parts),
                "data_type": data_type,
                "format": output_format,
                "status": "success"
            }
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported format: {output_format}")
            
    except Exception as e:
        logger.error(f"Error in get_party_data_tool: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tools/validate_input")
async def validate_input_tool(request: Dict[str, Any]):
    """Validate input data for MPC operations."""
    try:
        data = request.get("data", [])
        constraints = request.get("constraints", {})
        
        if not data:
            raise HTTPException(status_code=400, detail="Data array is required")
        
        if not isinstance(data, list):
            raise HTTPException(status_code=400, detail="Data must be an array")
        
        validation_results = {
            "is_valid": True,
            "errors": [],
            "warnings": [],
            "data_length": len(data),
            "status": "success"
        }
        
        # Check min/max values
        min_value = constraints.get("min_value")
        max_value = constraints.get("max_value")
        
        for i, value in enumerate(data):
            if min_value is not None and value < min_value:
                validation_results["errors"].append(f"Value at index {i} ({value}) is below minimum ({min_value})")
                validation_results["is_valid"] = False
            
            if max_value is not None and value > max_value:
                validation_results["errors"].append(f"Value at index {i} ({value}) is above maximum ({max_value})")
                validation_results["is_valid"] = False
        
        # Check required length
        required_length = constraints.get("required_length")
        if required_length is not None and len(data) != required_length:
            validation_results["errors"].append(f"Data length ({len(data)}) does not match required length ({required_length})")
            validation_results["is_valid"] = False
        
        return validation_results
        
    except Exception as e:
        logger.error(f"Error in validate_input_tool: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# n8n-specific convenience endpoints
@app.get("/n8n/status")
async def n8n_status():
    """Get n8n integration status."""
    return {
        "server_name": "party1",
        "server_description": "Party 1 MCP Tools for n8n Integration",
        "server_version": "1.0.0",
        "n8n_integration": True,
        "available_tools": ["compute_mpc", "get_party_data", "validate_input"],
        "available_resources": ["party1_data", "mpc_results"],
        "endpoints": {
            "tools": "/tools",
            "resources": "/resources",
            "health": "/health"
        }
    }

@app.get("/n8n/example")
async def n8n_example():
    """Get example n8n workflow configuration."""
    return {
        "workflow_name": "MPC Party1 Integration",
        "description": "Example workflow using Party1 MCP tools",
        "nodes": [
            {
                "name": "Compute MPC",
                "type": "HTTP Request",
                "method": "POST",
                "url": "http://localhost:8003/tools/compute_mpc",
                "body": {
                    "operation": "add",
                    "values": [1, 2, 3, 4, 5]
                }
            },
            {
                "name": "Get Party Data",
                "type": "HTTP Request",
                "method": "POST",
                "url": "http://localhost:8003/tools/get_party_data",
                "body": {
                    "data_type": "financial",
                    "format": "json"
                }
            }
        ]
    }

if __name__ == "__main__":
    # Get port from environment variable or use default
    port = int(os.getenv("N8N_REST_PORT", "8003"))
    uvicorn.run(app, host="0.0.0.0", port=port) 