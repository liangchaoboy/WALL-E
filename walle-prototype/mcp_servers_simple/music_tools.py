#!/usr/bin/env python3
"""
简化版音乐工具 (不依赖 MCP 库)
用于快速验证,无需安装 mcp 包
"""

import webbrowser
from urllib.parse import quote

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
    if not song or not song.strip():
        return "错误: 歌曲名称不能为空"
    
    song = song.strip()
    artist = artist.strip() if artist else ""
    query = f"{artist} {song}" if artist else song
    
    platform_urls = {
        "qq": f"https://y.qq.com/n/ryqq/search?w={quote(query)}",
        "netease": f"https://music.163.com/#/search/m/?s={quote(query)}",
        "spotify": f"https://open.spotify.com/search/{quote(query)}"
    }
    
    url = platform_urls.get(platform, platform_urls["qq"])
    webbrowser.open(url)
    
    return f"已在{platform}音乐平台搜索: {query}"

def search_playlist(keyword: str, platform: str = "qq") -> str:
    """
    Search for a music playlist
    
    Args:
        keyword: Playlist search keyword
        platform: Music platform (qq, netease, spotify)
    
    Returns:
        Status message
    """
    if not keyword or not keyword.strip():
        return "错误: 搜索关键词不能为空"
    
    keyword = keyword.strip()
    platform_urls = {
        "qq": f"https://y.qq.com/n/ryqq/search?w={quote(keyword)}&t=playlist",
        "netease": f"https://music.163.com/#/search/m/?s={quote(keyword)}&type=1000",
        "spotify": f"https://open.spotify.com/search/{quote(keyword)}%20playlist"
    }
    
    url = platform_urls.get(platform, platform_urls["qq"])
    webbrowser.open(url)
    
    return f"已在{platform}搜索歌单: {keyword}"

TOOLS = {
    "play_music": play_music,
    "search_playlist": search_playlist,
}
