"""
MCP Server Implementation

A minimal Model Context Protocol server for the Shai Hackathon.
"""

import asyncio
import json
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from pydantic import BaseModel


@dataclass
class MCPTool:
    """Represents an MCP tool/function."""

    name: str
    description: str
    parameters: Dict[str, Any]


class MCPMessage(BaseModel):
    """Base MCP message structure."""

    method: str
    params: Optional[Dict[str, Any]] = None
    id: Optional[str] = None


class MCPServer:
    """
    A minimal MCP (Model Context Protocol) server implementation.

    This server provides basic MCP functionality including:
    - Tool registration and execution
    - Resource management
    - Protocol message handling
    """

    def __init__(
        self, name: str = "mcp-server", version: str = "1.0.0", debug: bool = False
    ):
        self.name = name
        self.version = version
        self.debug = debug
        self.tools: Dict[str, MCPTool] = {}
        self.resources: Dict[str, Any] = {}

        # Set up logging
        log_level = logging.DEBUG if debug else logging.INFO
        logging.basicConfig(level=log_level)
        self.logger = logging.getLogger(__name__)

        # Register default tools
        self._register_default_tools()

    def _register_default_tools(self):
        """Register default tools for the MCP server."""

        # Hello World tool
        hello_tool = MCPTool(
            name="hello",
            description="Say hello with an optional name",
            parameters={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name to greet",
                        "default": "World",
                    }
                },
            },
        )
        self.register_tool(hello_tool, self._hello_handler)

        # Echo tool
        echo_tool = MCPTool(
            name="echo",
            description="Echo back the provided message",
            parameters={
                "type": "object",
                "properties": {
                    "message": {"type": "string", "description": "Message to echo back"}
                },
                "required": ["message"],
            },
        )
        self.register_tool(echo_tool, self._echo_handler)

        # Server info tool
        info_tool = MCPTool(
            name="server_info",
            description="Get information about the MCP server",
            parameters={"type": "object", "properties": {}},
        )
        self.register_tool(info_tool, self._info_handler)

    def register_tool(self, tool: MCPTool, handler):
        """Register a tool with its handler function."""
        self.tools[tool.name] = tool
        setattr(self, f"_handle_{tool.name}", handler)
        self.logger.debug(f"Registered tool: {tool.name}")

    async def _hello_handler(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handler for the hello tool."""
        name = params.get("name", "World")
        return {"content": f"Hello, {name}! Welcome to the Shai Hackathon MCP Server!"}

    async def _echo_handler(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handler for the echo tool."""
        message = params.get("message", "")
        return {"content": f"Echo: {message}"}

    async def _info_handler(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handler for the server info tool."""
        return {
            "content": {
                "name": self.name,
                "version": self.version,
                "tools_count": len(self.tools),
                "available_tools": list(self.tools.keys()),
                "debug_mode": self.debug,
            }
        }

    async def handle_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming MCP messages."""
        try:
            mcp_msg = MCPMessage(**message)

            if mcp_msg.method == "tools/list":
                return await self._handle_tools_list()
            elif mcp_msg.method == "tools/call":
                return await self._handle_tool_call(mcp_msg.params or {})
            elif mcp_msg.method == "initialize":
                return await self._handle_initialize(mcp_msg.params or {})
            else:
                return {"error": f"Unknown method: {mcp_msg.method}"}

        except Exception as e:
            self.logger.error(f"Error handling message: {e}")
            return {"error": f"Error processing message: {str(e)}"}

    async def _handle_tools_list(self) -> Dict[str, Any]:
        """Handle tools/list request."""
        tools_list = []
        for tool in self.tools.values():
            tools_list.append(
                {
                    "name": tool.name,
                    "description": tool.description,
                    "inputSchema": tool.parameters,
                }
            )

        return {"tools": tools_list}

    async def _handle_tool_call(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tools/call request."""
        tool_name = params.get("name")
        tool_params = params.get("arguments", {})

        if tool_name not in self.tools:
            return {"error": f"Unknown tool: {tool_name}"}

        handler = getattr(self, f"_handle_{tool_name}", None)
        if not handler:
            return {"error": f"No handler for tool: {tool_name}"}

        try:
            result = await handler(tool_params)
            return {"content": [result]}
        except Exception as e:
            self.logger.error(f"Error executing tool {tool_name}: {e}")
            return {"error": f"Error executing tool: {str(e)}"}

    async def _handle_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle initialize request."""
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}, "resources": {}},
            "serverInfo": {"name": self.name, "version": self.version},
        }

    async def run(self, host: str = "localhost", port: int = 8000):
        """Run the MCP server."""
        self.logger.info(f"Starting {self.name} v{self.version}")
        self.logger.info(f"Server running on {host}:{port}")
        self.logger.info(f"Registered tools: {list(self.tools.keys())}")

        # Simple demonstration - in a real implementation, this would
        # handle actual MCP protocol communication
        print(f"\\n🚀 MCP Server '{self.name}' is running!")
        print(f"📍 Version: {self.version}")
        print(f"🔧 Available tools: {', '.join(self.tools.keys())}")
        print(f"🐛 Debug mode: {self.debug}")
        print("\\n📝 Example tool calls:")

        # Demonstrate tool calls
        test_messages = [
            {"method": "initialize", "params": {}},
            {"method": "tools/list"},
            {
                "method": "tools/call",
                "params": {"name": "hello", "arguments": {"name": "Shai"}},
            },
            {
                "method": "tools/call",
                "params": {"name": "echo", "arguments": {"message": "Hello MCP!"}},
            },
            {
                "method": "tools/call",
                "params": {"name": "server_info", "arguments": {}},
            },
        ]

        for i, msg in enumerate(test_messages, 1):
            print(f"\\n{i}. Testing: {msg['method']}")
            result = await self.handle_message(msg)
            print(f"   Result: {json.dumps(result, indent=2)}")

        print("\\n✅ MCP Server demonstration complete!")
        print("🛑 Press Ctrl+C to stop the server")

        # Keep server running
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            self.logger.info("Server shutdown requested")
            print("\\n👋 MCP Server stopped!")
