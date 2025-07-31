from fastapi import FastAPI
from fastapi_mcp import FastApiMCP

# Your existing FastAPI application
app = FastAPI()

# Define your API endpoints with clear descriptions and operation IDs
@app.get("/weather/{country}", operation_id="get_weather_info",
         description="Retrieves the current weather information for a given country.")
async def get_weather(country: str):
    """
    This function simulates fetching weather data.
    In a real application, you would integrate with a weather API.
    """
    if country.lower() == "usa":
        return {"country": country, "temperature": "25°C", "condition": "Sunny"}
    else:
        return {"country": country, "temperature": "Unknown", "condition": "Data not available"}

# Create an instance of FastApiMCP, passing your FastAPI app
mcp = FastApiMCP(
    app,
    name="Weather API MCP",
    description="MCP server for retrieving weather information."
)

# Mount the MCP server to your FastAPI app (using both HTTP and SSE transport)
mcp.mount_http()  # HTTP transport
mcp.mount_sse()   # SSE transport

# Add health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "server": "party2-weather-mcp"}

# Add status endpoint
@app.get("/mcp/status")
async def mcp_status():
    return {
        "server_name": "party2",
        "server_description": "Party 2 Weather MCP Server",
        "server_version": "1.0.0",
        "capabilities": {
            "tools": {},
            "resources": {}
        }
    }

if __name__ == "__main__":
    import uvicorn
    import os
    
    # Get port from environment variable or use default
    port = int(os.getenv("PARTY2_PORT", "9001"))
    uvicorn.run(app, host="127.0.0.1", port=port)