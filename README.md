# Shai Hackathon MCP Project

A minimal Python implementation of an MCP (Model Context Protocol) server for the Shai Hackathon.

## 🚀 Quick Start

1. **Clone and setup**:
   ```bash
   git clone <repository-url>
   cd shaiwtf
   chmod +x setup.sh
   ./setup.sh
   ```

2. **Activate virtual environment**:
   ```bash
   source venv/bin/activate
   ```

3. **Run the MCP server**:
   ```bash
   python start.py
   ```

## 📁 Project Structure

```
shaiwtf/
├── .env                    # Environment configuration
├── .gitignore             # Git ignore patterns
├── requirements.txt       # Python dependencies
├── start.py              # Main entry point
├── setup.sh              # Development setup script
├── src/
│   └── mcp_server/
│       ├── __init__.py
│       └── server.py     # MCP server implementation
├── tests/
│   ├── __init__.py
│   └── test_server.py    # Test cases
└── docs/                 # Documentation (empty for now)
```

## 🔧 Configuration

The project uses environment variables for configuration. Copy `.env` and modify as needed:

- `MCP_SERVER_NAME`: Name of the MCP server
- `MCP_SERVER_VERSION`: Version of the server
- `MCP_SERVER_PORT`: Port to run the server on
- `DEBUG`: Enable debug logging

## 🛠 Available Tools

The MCP server comes with three built-in tools:

1. **hello** - Say hello with an optional name
2. **echo** - Echo back the provided message  
3. **server_info** - Get information about the MCP server

## 🧪 Testing

Run the test suite:

```bash
pytest tests/
```

Run with verbose output:

```bash
pytest tests/ -v
```

## 📋 Features

- ✅ Minimal MCP server implementation
- ✅ Environment-based configuration
- ✅ Built-in example tools
- ✅ Comprehensive test suite
- ✅ Easy development setup
- ✅ Clean project structure

## 🤝 Contributing

1. Make sure tests pass: `pytest tests/`
2. Follow the existing code style
3. Add tests for new features

## 📝 License

This project is created for the Shai Hackathon.

## 🔗 MCP Resources

- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
