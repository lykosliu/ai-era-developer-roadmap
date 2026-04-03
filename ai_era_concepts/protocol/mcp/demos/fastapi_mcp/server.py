import os
import sys

# Requirements for FastAPI MCP Server:
# pip install fastapi mcp uvicorn

from mcp.server.fastmcp import FastMCP

# Initialize the FastMCP app
app = FastMCP(
    name="FastAPI MCP Demo",
    instructions="A demo MCP server built with FastMCP",
    host="0.0.0.0",
    port=8000
)

# Define a sample tool
@app.tool()
async def get_weather(city: str) -> str:
    """Get the current weather for a given city."""
    # In a real app, you'd call an external API here
    return f"The weather in {city} is sunny and 25°C."

# Define a sample resource
@app.resource("mcp://demo/hello")
async def get_hello_resource() -> str:
    """A sample resource that returns a greeting."""
    return "Hello from the FastAPI MCP Server!"

if __name__ == "__main__":
    # Run the server with SSE transport
    app.run(transport="sse")
