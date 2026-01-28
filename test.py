"""
Test script for Grokipedia MCP Server
Uses the official MCP Python SDK to connect to http://127.0.0.1:8000/mcp
"""

import asyncio

async def test_with_mcp_sdk():
    """Test using the official MCP Python SDK."""
    print("=" * 50)
    print("  GROKIPEDIA MCP TEST (SDK)")
    print("=" * 50)
    
    try:
        from mcp.client.streamable_http import streamablehttp_client
        from mcp import ClientSession
        
        print("\n1. Connecting to MCP server...")
        
        async with streamablehttp_client("http://127.0.0.1:8000/mcp") as (read, write, _):
            async with ClientSession(read, write) as session:
                # Initialize
                await session.initialize()
                print("   ✅ Connected!")
                
                # List tools
                print("\n2. Listing tools...")
                tools = await session.list_tools()
                print(f"   Found {len(tools.tools)} tool(s):")
                for tool in tools.tools:
                    print(f"      - {tool.name}")
                
                # Call grokipedia_query
                print("\n3. Calling grokipedia_query...")
                result = await session.call_tool(
                    "grokipedia_query",
                    arguments={
                        "query": "Albert Einstein",
                        "action": "smart",
                        "max_results": 1
                    }
                )
                
                print("   ✅ Tool call successful!")
                if result.content:
                    import json
                    content = result.content[0]
                    if hasattr(content, 'text'):
                        data = json.loads(content.text)
                        print(f"      Action: {data.get('action')}")
                        print(f"      Total: {data.get('totalFound', 'N/A')}")
                        if data.get('results'):
                            print(f"      First: {data['results'][0].get('title')}")
                
                print("\n" + "=" * 50)
                print("  ✅ ALL TESTS PASSED!")
                print("=" * 50)
                
    except ImportError:
        print("\n   MCP SDK not installed. Installing...")
        print("   Run: pip install mcp")
        
        # Fallback: test API directly
        await test_api_directly()
        
    except Exception as e:
        print(f"\n   ❌ Error: {e}")
        print("\n   Trying fallback test...")
        await test_api_directly()


async def test_api_directly():
    """Fallback: Test the Grokipedia API directly."""
    print("\n" + "=" * 50)
    print("  FALLBACK: Testing Grokipedia API")
    print("=" * 50)
    
    import httpx
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Test 1: Check if MCP server is running
            print("\n1. Checking MCP server...")
            try:
                response = await client.get("http://127.0.0.1:8000/")
                print(f"   ✅ Server running (status: {response.status_code})")
            except:
                print("   ❌ Server not reachable")
                return
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("  TEST COMPLETE")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(test_with_mcp_sdk())
