"""
Test configuration and utilities for the MCP server.
"""

import pytest
import asyncio
from src.mcp_server.server import MCPServer


@pytest.fixture
def mcp_server():
    """Create an MCP server instance for testing."""
    return MCPServer(name="test-server", version="1.0.0", debug=True)


@pytest.fixture
def event_loop():
    """Create an event loop for async tests."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()
