#!/usr/bin/env python3
"""
MCP Server for Navigation
Provides navigation tools for WALL-E
"""

import webbrowser

try:
    from mcp.server.fastmcp import FastMCP
    mcp = FastMCP("Navigation")
    HAS_MCP = True
except ImportError:
    HAS_MCP = False
    mcp = None
    print("⚠️  MCP 库未安装,使用简化模式")

@mcp.tool()
def navigate(origin: str, destination: str, map_service: str = "baidu") -> str:
    """
    Open map navigation from origin to destination
    
    Args:
        origin: Starting location
        destination: Target location
        map_service: Map service to use (baidu, google, amap)
    
    Returns:
        Status message
    """
    map_urls = {
        "baidu": f"https://map.baidu.com/?from={origin}&to={destination}",
        "google": f"https://www.google.com/maps/dir/{origin}/{destination}",
        "amap": f"https://uri.amap.com/navigation?from={origin}&to={destination}"
    }
    
    url = map_urls.get(map_service, map_urls["baidu"])
    webbrowser.open(url)
    
    return f"已打开{map_service}地图: {origin} → {destination}"

@mcp.tool()
def search_location(query: str, map_service: str = "baidu") -> str:
    """
    Search for a location on the map
    
    Args:
        query: Location search query
        map_service: Map service to use (baidu, google, amap)
    
    Returns:
        Status message
    """
    search_urls = {
        "baidu": f"https://map.baidu.com/?query={query}",
        "google": f"https://www.google.com/maps/search/{query}",
        "amap": f"https://uri.amap.com/marker?position={query}"
    }
    
    url = search_urls.get(map_service, search_urls["baidu"])
    webbrowser.open(url)
    
    return f"已在{map_service}地图搜索: {query}"

@mcp.resource("navigation://help")
def get_help() -> str:
    """Get navigation tools help"""
    return """
    Navigation MCP Server - Available Tools:
    
    1. navigate(origin, destination, map_service="baidu")
       - Open map navigation between two locations
       - Example: navigate("上海", "北京")
    
    2. search_location(query, map_service="baidu")
       - Search for a location on the map
       - Example: search_location("虹桥机场")
    
    Supported map services: baidu, google, amap
    """
