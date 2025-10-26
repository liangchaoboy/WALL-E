#!/usr/bin/env python3
"""
MCP Server for Weather
Provides weather query tools for WALL-E
"""

import webbrowser
from urllib.parse import quote
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather")

@mcp.tool()
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

@mcp.tool()
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

@mcp.resource("weather://help")
def get_help() -> str:
    """Get weather tools help"""
    return """
    Weather MCP Server - Available Tools:
    
    1. get_weather(city, date="today")
       - Get weather information for a city
       - Example: get_weather("上海", "明天")
    
    2. compare_weather(city1, city2)
       - Compare weather between two cities
       - Example: compare_weather("北京", "上海")
    
    Supported dates: today, tomorrow, or specific dates
    """
