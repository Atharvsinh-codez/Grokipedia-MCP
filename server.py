from fastmcp import FastMCP
import httpx
import json
from typing import Optional

mcp = FastMCP("Grokipedia MCP Agent")

@mcp.tool
async def grokipedia_query(
    query: str,
    action: str = "smart",
    slug: Optional[str] = None,
    max_results: int = 2
) -> str:
    """
    🌟 All-in-one Grokipedia tool - your gateway to knowledge.
    
    This tool intelligently handles all Grokipedia queries in ONE call.
    
    Actions:
        - "smart" (default): Searches and automatically fetches full details for top results
        - "search": Just return search results with slugs (for browsing)
        - "page": Get specific page details with citations (requires slug)
        - "content": Get full text content of a page (requires slug)
    
    Args:
        query: What you're looking for (topic, person, concept, etc.)
        action: How to process your query (default: "smart")
        slug: Specific page slug (required for "page" and "content" actions)
        max_results: Number of top results to fetch full details for in "smart" mode (default: 2)
    
    Returns:
        Complete information in one response - no need for multiple tool calls!
    
    Examples:
        - grokipedia_query("Albert Einstein") → Gets top 2 results with full content
        - grokipedia_query("Python programming", action="search") → Just search results
        - grokipedia_query("", action="content", slug="Albert_Einstein") → Full article text
    """
    try:
        # ACTION: Get specific page by slug
        if action == "page" and slug:
            url = f"https://grokipedia.com/api/page?slug={slug}&includeContent=false&validateLinks=true"
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=30.0)
                response.raise_for_status()
                data = response.json()
            
            if not data.get("found", False):
                return json.dumps({
                    "error": "Page not found",
                    "slug": slug,
                    "x": "https://x.com/athrix_codes",
                    "github": "https://github.com/Atharvsinh-codez"
                }, indent=2)
            
            page_data = data.get("page", {})
            citations = [
                {
                    "id": c.get("id", ""),
                    "title": c.get("title", ""),
                    "url": c.get("url", "")
                }
                for c in page_data.get("citations", [])
            ]
            
            return json.dumps({
                "action": "page",
                "slug": slug,
                "citations": citations[:10],  # Limit to first 10
                "categories": page_data.get("metadata", {}).get("categories", []),
                "stats": page_data.get("stats", {}),
                "x": "https://x.com/athrix_codes",
                "github": "https://github.com/Atharvsinh-codez"
            }, indent=2)
        
        # ACTION: Get full content by slug
        elif action == "content" and slug:
            url = f"https://grokipedia-api.com/page/{slug}"
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=30.0)
                
                if response.status_code == 429:
                    return json.dumps({
                        "error": "Rate limit exceeded - please try again in a moment",
                        "slug": slug,
                        "x": "https://x.com/athrix_codes",
                        "github": "https://github.com/Atharvsinh-codez"
                    }, indent=2)
                
                response.raise_for_status()
                data = response.json()
            
            return json.dumps({
                "action": "content",
                "title": data.get("title", ""),
                "slug": data.get("slug", ""),
                "url": data.get("url", ""),
                "content_text": data.get("content_text", ""),
                "word_count": data.get("word_count", 0),
                "char_count": data.get("char_count", 0),
                "x": "https://x.com/athrix_codes",
                "github": "https://github.com/Atharvsinh-codez"
            }, indent=2)
        
        # ACTION: Search (either just search, or smart search with details)
        else:
            # Step 1: Search
            search_url = f"https://grokipedia.com/api/full-text-search?query={query}&limit=11&offset=0"
            async with httpx.AsyncClient() as client:
                response = await client.get(search_url, timeout=30.0)
                response.raise_for_status()
                search_data = response.json()
            
            search_results = [
                {
                    "slug": item.get("slug", ""),
                    "title": item.get("title", ""),
                    "snippet": item.get("snippet", "").replace("<em>", "").replace("</em>", ""),
                    "relevanceScore": item.get("relevanceScore", 0)
                }
                for item in search_data.get("results", [])
            ]
            
            if action == "search":
                # Just return search results
                return json.dumps({
                    "action": "search",
                    "query": query,
                    "results": search_results,
                    "totalCount": search_data.get("totalCount", 0),
                    "x": "https://x.com/athrix_codes",
                    "github": "https://github.com/Atharvsinh-codez"
                }, indent=2)
            
            # ACTION: Smart mode - fetch full content for top results
            if not search_results:
                return json.dumps({
                    "action": "smart",
                    "query": query,
                    "message": "No results found",
                    "x": "https://x.com/athrix_codes",
                    "github": "https://github.com/Atharvsinh-codez"
                }, indent=2)
            
            # Step 2: Fetch full content for top N results
            detailed_results = []
            async with httpx.AsyncClient() as client:
                for result in search_results[:max_results]:
                    try:
                        content_url = f"https://grokipedia-api.com/page/{result['slug']}"
                        content_response = await client.get(content_url, timeout=30.0)
                        
                        if content_response.status_code == 200:
                            content_data = content_response.json()
                            detailed_results.append({
                                "slug": result["slug"],
                                "title": content_data.get("title", result["title"]),
                                "snippet": result["snippet"],
                                "relevanceScore": result["relevanceScore"],
                                "content_preview": content_data.get("content_text", "")[:500] + "...",
                                "word_count": content_data.get("word_count", 0),
                                "url": content_data.get("url", "")
                            })
                        else:
                            # Fallback to search result if content fetch fails
                            detailed_results.append(result)
                    except:
                        # Fallback to search result if error
                        detailed_results.append(result)
            
            return json.dumps({
                "action": "smart",
                "query": query,
                "results": detailed_results,
                "totalFound": search_data.get("totalCount", 0),
                "showing": len(detailed_results),
                "x": "https://x.com/athrix_codes",
                "github": "https://github.com/Atharvsinh-codez"
            }, indent=2)
    
    except Exception as e:
        return json.dumps({
            "error": str(e),
            "query": query,
            "action": action,
            "x": "https://x.com/athrix_codes",
            "github": "https://github.com/Atharvsinh-codez"
        }, indent=2)


if __name__ == "__main__":
    mcp.run(transport="http", port=8000)