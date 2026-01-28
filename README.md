# Grokipedia MCP Server

A Model Context Protocol (MCP) server that provides intelligent access to Grokipedia's knowledge base through a single, unified tool.

## Features

This MCP server provides **one powerful tool** that handles everything:

### **grokipedia_query** - Your All-in-One Knowledge Gateway

A smart tool that adapts to your needs with different action modes:

#### **"smart" mode (default)**

- Searches and automatically fetches full details for top results
- Returns complete information in ONE call
- Perfect for most queries
- Example: `grokipedia_query("Albert Einstein")`

#### **"search" mode**

- Returns search results with slugs for browsing
- Lightweight and fast
- Example: `grokipedia_query("Python programming", action="search")`

#### **"page" mode**

- Gets detailed page information with citations
- Includes metadata and statistics
- Example: `grokipedia_query("", action="page", slug="Albert_Einstein")`

#### **"content" mode**

- Fetches full article text content
- Clean, HTML-stripped text
- Example: `grokipedia_query("", action="content", slug="Albert_Einstein")`

**Key Benefits:**

- ✅ No multiple tool calls needed
- ✅ Smart defaults that just work
- ✅ Flexible when you need specific data
- ✅ Optimized for LLM usage

## Usage

### Connecting to Claude Desktop

Add this to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "grokipedia": {
      "url": "http://127.0.0.1:8000/mcp"
    }
  }
}
```



### Connecting to VS Code (Cline Extension)

1. Install the [Cline extension](https://marketplace.visualstudio.com/items?itemName=saoudrizwan.claude-dev)
2. Open Cline settings
3. Add MCP server:

```json
{
  "mcpServers": {
    "grokipedia": {
      "url": "http://127.0.0.1:8000/mcp"
    }
  }
}
```

### Connecting to Cursor

Add to your Cursor MCP settings:

```json
{
  "mcpServers": {
    "grokipedia": {
      "url": "http://127.0.0.1:8000/mcp"
    }
  }
}
```

### Connecting to Other MCP Clients

For any MCP-compatible client, use the server URL:

```
http://127.0.0.1:8000/mcp
```

## Server Information

- **Name**: Grokipedia MCP Agent
- **Version**: 2.13.0.2
- **Generation**: FastMCP 2.x
- **Tools**: 1 (unified)
- **Prompts**: 0
- **Resources**: 0

## Dependencies

- `fastmcp>=2.0.0` - FastMCP framework
- `httpx>=0.27.0` - Async HTTP client

## Acknowledgments

Built with:

- [FastMCP](https://github.com/jlowin/fastmcp) - MCP server framework
- [Grokipedia API](https://github.com/dataxapi/grokipedia-api) - Knowledge base API

By [Atharvsinh-codez](https://x.com/athrix_codes)
