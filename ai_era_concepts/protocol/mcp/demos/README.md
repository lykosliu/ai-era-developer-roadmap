---
name: mcp demos
description: Hands-on examples and runnable code for Model Context Protocol.
---

# MCP Demos: Building MCP-Compliant Servers

This directory contains two example implementations of **Model Context Protocol (MCP)** servers, demonstrating how to expose tools and resources to AI assistants.

## 📁 Demos Included

### 1. [FastMCP Server (Python)](./fastapi_mcp/server.py)
A Python implementation using the `mcp` SDK's **FastMCP** interface to provide an HTTP-based server with **SSE (Server-Sent Events)** transport.

- **Tools Exposed:** `get_weather(city: str)`
- **Resources Exposed:** `mcp://demo/hello`

### 2. [Node.js MCP Server](./node_mcp/server.js)
A TypeScript/JavaScript implementation using the `@modelcontextprotocol/sdk` to provide a local server with **STDIO** transport.

- **Tools Exposed:** `calculate_sum(a: number, b: number)`
- **Resources Exposed:** `mcp://node-demo/status`

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+
- Node.js 18+

### 2. Setup Dependencies
Run the included setup script to install all necessary packages for both demos:
```bash
bash setup.sh
```

### 3. Running the FastAPI Server
```bash
cd fastapi_mcp
python3 server.py
```
By default, the server will run on `http://localhost:8000`. You can test the connection by querying the discovery endpoint.

### 4. Running the Node.js Server
Since this demo uses the **STDIO** transport, it's designed to be invoked by an MCP client (like Claude Desktop or the MCP Inspector). To test it manually, you can run:
```bash
cd node_mcp
node server.js
```
*Note: You won't see interactive output because it expects JSON-RPC over standard input/output.*

## 🧪 Testing with MCP Inspector
The easiest way to test these servers is using the [MCP Inspector](https://github.com/modelcontextprotocol/inspector):

**For Node.js (STDIO):**
```bash
npx @modelcontextprotocol/inspector node node_mcp/server.js
```

**For FastMCP (SSE):**
1. Start the server: `python3 fastapi_mcp/server.py`
2. Run the Inspector: `npx @modelcontextprotocol/inspector`
3. Open `http://localhost:6274` in your browser.
4. Select **SSE** and enter `http://localhost:8000/sse` to connect.
