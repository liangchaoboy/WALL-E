#!/usr/bin/env python3
"""
简化版导航工具 (不依赖 MCP 库)
用于快速验证,无需安装 mcp 包
"""

import webbrowser

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

TOOLS = {
    "navigate": navigate,
    "search_location": search_location,
}
