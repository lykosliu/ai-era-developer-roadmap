/**
 * Node.js MCP Server Demo
 * Requirements:
 * npm install @modelcontextprotocol/sdk express
 */

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

// Create an MCP server instance
const server = new McpServer({
  name: "Node.js MCP Demo",
  version: "1.0.0",
});

// Register a tool with input validation using Zod
server.tool(
  "calculate_sum",
  {
    a: z.number().describe("The first number to add"),
    b: z.number().describe("The second number to add"),
  },
  async ({ a, b }) => {
    return {
      content: [
        {
          type: "text",
          text: `The sum of ${a} and ${b} is ${a + b}`,
        },
      ],
    };
  }
);

// Register a simple resource
server.resource(
  "mcp://node-demo/status",
  "Node.js Server Status",
  async (uri) => {
    return {
      contents: [
        {
          uri: uri.href,
          text: "The Node.js MCP server is running and ready for connections.",
        },
      ],
    };
  }
);

// Start the server using the STDIO transport
// (Commonly used for local tool integrations)
async function run() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Node.js MCP Server started on STDIO");
}

run().catch((error) => {
  console.error("Failed to start Node.js MCP server:", error);
});
