"""
Tests for the MCP server implementation.
"""

import pytest
from src.mcp_server.server import MCPServer


class TestMCPServer:
    """Test cases for the MCP server."""

    def test_server_initialization(self):
        """Test that the server initializes correctly."""
        server = MCPServer(name="test-server", version="1.0.0")
        assert server.name == "test-server"
        assert server.version == "1.0.0"
        assert len(server.tools) > 0  # Should have default tools

    @pytest.mark.asyncio
    async def test_tools_list(self):
        """Test the tools/list functionality."""
        server = MCPServer()

        message = {"method": "tools/list"}
        result = await server.handle_message(message)

        assert "tools" in result
        assert len(result["tools"]) > 0

        # Check that default tools are present
        tool_names = [tool["name"] for tool in result["tools"]]
        assert "hello" in tool_names
        assert "echo" in tool_names
        assert "server_info" in tool_names

    @pytest.mark.asyncio
    async def test_hello_tool(self):
        """Test the hello tool."""
        server = MCPServer()

        message = {
            "method": "tools/call",
            "params": {"name": "hello", "arguments": {"name": "Test"}},
        }

        result = await server.handle_message(message)
        assert "content" in result
        assert "Hello, Test!" in str(result["content"])

    @pytest.mark.asyncio
    async def test_echo_tool(self):
        """Test the echo tool."""
        server = MCPServer()

        message = {
            "method": "tools/call",
            "params": {"name": "echo", "arguments": {"message": "Hello World"}},
        }

        result = await server.handle_message(message)
        assert "content" in result
        assert "Echo: Hello World" in str(result["content"])

    @pytest.mark.asyncio
    async def test_server_info_tool(self):
        """Test the server_info tool."""
        server = MCPServer(name="test-server", version="2.0.0")

        message = {
            "method": "tools/call",
            "params": {"name": "server_info", "arguments": {}},
        }

        result = await server.handle_message(message)
        assert "content" in result
        content = result["content"][0]["content"]
        assert content["name"] == "test-server"
        assert content["version"] == "2.0.0"

    @pytest.mark.asyncio
    async def test_unknown_method(self):
        """Test handling of unknown methods."""
        server = MCPServer()

        message = {"method": "unknown/method"}
        result = await server.handle_message(message)

        assert "error" in result
        assert "Unknown method" in result["error"]

    @pytest.mark.asyncio
    async def test_unknown_tool(self):
        """Test calling an unknown tool."""
        server = MCPServer()

        message = {
            "method": "tools/call",
            "params": {"name": "unknown_tool", "arguments": {}},
        }

        result = await server.handle_message(message)
        assert "error" in result
        assert "Unknown tool" in result["error"]
