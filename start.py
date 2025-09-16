#!/usr/bin/env python3
"""
MCP Server Starter for Shai Hackathon

This is the main entry point for the MCP (Model Context Protocol) server.
"""

import os
import sys
import asyncio
from dotenv import load_dotenv

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from mcp_server.server import MCPServer


def main():
    """Main entry point for the MCP server."""
    # Load environment variables
    load_dotenv()

    # Get configuration from environment
    server_name = os.getenv("MCP_SERVER_NAME", "shaiwtf-mcp-server")
    server_version = os.getenv("MCP_SERVER_VERSION", "1.0.0")
    port = int(os.getenv("MCP_SERVER_PORT", 8000))
    debug = os.getenv("DEBUG", "false").lower() == "true"

    print(f"Starting {server_name} v{server_version}")
    print(f"Debug mode: {debug}")
    print(f"Port: {port}")

    # Create and run the MCP server
    server = MCPServer(name=server_name, version=server_version, debug=debug)

    try:
        asyncio.run(server.run(port=port))
    except KeyboardInterrupt:
        print("\nShutting down server...")
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
