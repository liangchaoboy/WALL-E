#!/usr/bin/env python3
"""
MCP Server for Music
Provides music control tools for WALL-E
"""

import webbrowser
from mcp.server.fastmcp import FastMCP
from urllib.parse import quote, urlencode

mcp = FastMCP("Music")

@mcp.tool()
def play_music(song: str, artist: str = "", platform: str = "qq") -> str:
    """
    Play music on a music platform
    
    Args:
        song: Song name
        artist: Artist name (optional)
        platform: Music platform (qq, netease, spotify)
    
    Returns:
        Status message
    """
    query = f"{artist} {song}" if artist else song
    
    # QQ音乐需要正确编码中文，避免乱码
    if platform == "qq":
        qq_params = {"w": query}
        qq_query_str = urlencode(qq_params, doseq=False)
        url = f"https://y.qq.com/n/ryqq/search?{qq_query_str}"
    else:
        platform_urls = {
            "netease": f"https://music.163.com/#/search/m/?s={quote(query)}",
            "spotify": f"https://open.spotify.com/search/{quote(query)}"
        }
        url = platform_urls.get(platform, f"https://y.qq.com/n/ryqq/search?{urlencode({'w': query}, doseq=False)}")
    
    webbrowser.open(url)
    
    return f"已在{platform}音乐平台搜索: {query}"

@mcp.tool()
def search_playlist(keyword: str, platform: str = "qq") -> str:
    """
    Search for a music playlist
    
    Args:
        keyword: Playlist search keyword
        platform: Music platform (qq, netease, spotify)
    
    Returns:
        Status message
    """
    # QQ音乐需要正确编码中文，避免乱码
    if platform == "qq":
        qq_params = {"w": keyword, "t": "playlist"}
        qq_query_str = urlencode(qq_params, doseq=False)
        url = f"https://y.qq.com/n/ryqq/search?{qq_query_str}"
    else:
        platform_urls = {
            "netease": f"https://music.163.com/#/search/m/?s={quote(keyword)}&type=1000",
            "spotify": f"https://open.spotify.com/search/{quote(keyword)}%20playlist"
        }
        url = platform_urls.get(platform, f"https://y.qq.com/n/ryqq/search?{urlencode({'w': keyword, 't': 'playlist'}, doseq=False)}")
    
    webbrowser.open(url)
    
    return f"已在{platform}搜索歌单: {keyword}"

@mcp.resource("music://help")
def get_help() -> str:
    """Get music tools help"""
    return """
    Music MCP Server - Available Tools:
    
    1. play_music(song, artist="", platform="qq")
       - Play music on a platform
       - Example: play_music("晴天", "周杰伦")
    
    2. search_playlist(keyword, platform="qq")
       - Search for a music playlist
       - Example: search_playlist("流行音乐")
    
    Supported platforms: qq, netease, spotify
    """
