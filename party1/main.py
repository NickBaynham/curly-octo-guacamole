from fastapi import FastAPI
from fastapi_mcp import FastApiMCP
import uvicorn
import asyncio
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Initialize MCP app
mcp_app = FastApiMCP(app)

@app.get("/")
async def root():
    return {"message": "Party Ready", "mcp_enabled": True}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "mcp_server": "running"}

# MCP-specific endpoints
@app.get("/mcp/status")
async def mcp_status():
    return {
        "server_name": "party1",
        "server_description": "Party 1 MCP Server",
        "server_version": "1.0.0",
        "capabilities": {
            "tools": {},
            "resources": {}
        }
    }

# Start the MCP server
async def start_mcp_server():
    """Start the MCP server in the background."""
    try:
        await mcp_app.start()
        logger.info("MCP server started successfully")
    except Exception as e:
        logger.error(f"Failed to start MCP server: {e}")

@app.on_event("startup")
async def startup_event():
    """Start the MCP server when the FastAPI app starts."""
    asyncio.create_task(start_mcp_server())

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
