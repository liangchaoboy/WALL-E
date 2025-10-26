#!/usr/bin/env python3
"""
简化版导航工具 (不依赖 MCP 库)
用于快速验证,无需安装 mcp 包
"""

import webbrowser
from urllib.parse import urlencode

def _extract_city_name(address: str) -> str:
    """Extract city name from address"""
    cities = [
        "北京", "上海", "天津", "重庆",
        "广州", "深圳", "杭州", "成都", "西安", "南京",
        "武汉", "苏州", "郑州", "长沙", "济南", "青岛",
        "沈阳", "大连", "哈尔滨", "长春", "福州", "厦门",
        "昆明", "兰州", "乌鲁木齐", "石家庄", "太原",
    ]
    
    for city in cities:
        if address.startswith(city):
            return city
    
    if len(address) <= 4:
        return address
    
    return "全国"

def _generate_baidu_url(origin: str, destination: str) -> str:
    """Generate Baidu Maps navigation URL with proper API"""
    base_url = "http://api.map.baidu.com/direction"
    params = {
        "origin": origin,
        "destination": destination,
        "mode": "transit",
        "region": _extract_city_name(destination),
        "output": "html",
        "src": "webapp.walle.navigation"
    }
    return f"{base_url}?{urlencode(params)}"

def _generate_amap_url(origin: str, destination: str) -> str:
    """Generate Amap navigation URL"""
    base_url = "https://www.amap.com/dir"
    params = {
        "from": origin,
        "to": destination
    }
    return f"{base_url}?{urlencode(params)}"

def _generate_google_url(origin: str, destination: str) -> str:
    """Generate Google Maps navigation URL"""
    base_url = "https://www.google.com/maps/dir/"
    params = {
        "api": "1",
        "origin": origin,
        "destination": destination,
        "travelmode": "transit"
    }
    return f"{base_url}?{urlencode(params)}"

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
    if not origin or not destination:
        return "错误: 起点和终点不能为空"
    
    url_generators = {
        "baidu": _generate_baidu_url,
        "google": _generate_google_url,
        "amap": _generate_amap_url
    }
    
    generator = url_generators.get(map_service, url_generators["baidu"])
    url = generator(origin, destination)
    
    try:
        webbrowser.open(url)
        map_names = {
            "baidu": "百度地图",
            "google": "Google Maps",
            "amap": "高德地图"
        }
        map_name = map_names.get(map_service, "百度地图")
        
        return (
            f"✅ 成功打开 {map_name}\n\n"
            f"📍 起点：{origin}\n"
            f"📍 终点：{destination}\n"
            f"🔗 导航链接：{url}\n\n"
            f"地图应用已在浏览器中打开，正在准备导航..."
        )
    except Exception as e:
        return f"打开地图失败: {e}"

def search_location(query: str, map_service: str = "baidu") -> str:
    """
    Search for a location on the map
    
    Args:
        query: Location search query
        map_service: Map service to use (baidu, google, amap)
    
    Returns:
        Status message
    """
    if not query:
        return "错误: 搜索关键词不能为空"
    
    from urllib.parse import quote
    
    search_urls = {
        "baidu": f"https://map.baidu.com/?query={quote(query)}",
        "google": f"https://www.google.com/maps/search/{quote(query)}",
        "amap": f"https://www.amap.com/search?query={quote(query)}"
    }
    
    url = search_urls.get(map_service, search_urls["baidu"])
    
    try:
        webbrowser.open(url)
        map_names = {
            "baidu": "百度地图",
            "google": "Google Maps",
            "amap": "高德地图"
        }
        map_name = map_names.get(map_service, "百度地图")
        return f"✅ 已在{map_name}搜索: {query}\n🔗 {url}"
    except Exception as e:
        return f"打开地图搜索失败: {e}"

TOOLS = {
    "navigate": navigate,
    "search_location": search_location,
}
