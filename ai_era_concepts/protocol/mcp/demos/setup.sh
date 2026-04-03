#!/bin/bash
# setup.sh: Setup instructions and dependency installation for MCP Demos

# Exit on error
set -e

echo "Setting up MCP Demos..."

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required but not installed. Aborting."
    exit 1
fi

# Check for Node.js
if ! command -v node &> /dev/null; then
    echo "Node.js is required but not installed. Aborting."
    exit 1
fi

# 1. FastAPI MCP Setup
echo "Installing FastAPI MCP dependencies..."
cd fastapi_mcp
pip install fastapi mcp uvicorn
cd ..

# 2. Node.js MCP Setup
echo "Installing Node.js MCP dependencies..."
cd node_mcp
npm init -y
npm install @modelcontextprotocol/sdk zod express
# Add "type": "module" to package.json for ESM support
sed -i '' 's/"main": "index.js"/"main": "server.js",\n  "type": "module"/g' package.json
cd ..

echo "Setup complete! Refer to README.md for how to run the servers."
