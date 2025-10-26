#!/usr/bin/env python3
"""
简化版天气工具 (不依赖 MCP 库)
用于快速验证,无需安装 mcp 包
"""

import webbrowser
from urllib.parse import quote

def get_weather(city: str, date: str = "today") -> str:
    """
    Get weather information for a city
    
    Args:
        city: City name
        date: Date query (today, tomorrow, or specific date)
    
    Returns:
        Weather information or redirect message
    """
    query = f"{city}{date}天气"
    url = f"https://www.baidu.com/s?wd={quote(query)}"
    webbrowser.open(url)
    
    return f"已打开{city}{date}天气查询"

def compare_weather(city1: str, city2: str) -> str:
    """
    Compare weather between two cities
    
    Args:
        city1: First city
        city2: Second city
    
    Returns:
        Status message
    """
    query = f"{city1} {city2} 天气对比"
    url = f"https://www.baidu.com/s?wd={quote(query)}"
    webbrowser.open(url)
    
    return f"已打开{city1}和{city2}天气对比"

TOOLS = {
    "get_weather": get_weather,
    "compare_weather": compare_weather,
}
