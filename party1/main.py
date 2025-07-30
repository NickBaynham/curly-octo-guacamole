from fastapi import FastAPI
from fastapi_mcp import FastApiMCP
import uvicorn
import logging
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for FastAPI."""
    # Startup
    logger.info("Starting MCP server...")
    try:
        # Setup the MCP server
        mcp_app.setup_server()
        logger.info("MCP server started successfully")
    except Exception as e:
        logger.error(f"Failed to start MCP server: {e}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down MCP server...")

app = FastAPI(lifespan=lifespan)

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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
