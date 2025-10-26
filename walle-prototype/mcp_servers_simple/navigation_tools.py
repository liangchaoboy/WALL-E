#!/usr/bin/env python3
"""
简化版导航工具 (不依赖 MCP 库)
用于快速验证,无需安装 mcp 包
"""

import webbrowser
from urllib.parse import urlencode, quote

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
    
    # 百度地图正确格式（基于实际分享链接）
    # 路径: /dir/{起点}/{终点}/
    # 查询参数: querytype=bt&sq={起点}&eq={终点}
    
    # URL编码地点名称
    origin_encoded = quote(origin)
    dest_encoded = quote(destination)
    
    # 构建查询参数
    params = {
        "querytype": "bt",  # 必需参数
        "sq": origin,       # 起点 (search query)
        "eq": destination   # 终点 (end query)
    }
    query_string = urlencode(params, doseq=False)
    
    # 构建完整URL：路径中起点在前，终点在后
    # 注意：路径末尾不要加斜杠，直接用?连接查询参数
    url = f"https://map.baidu.com/dir/{origin_encoded}/{dest_encoded}?{query_string}"
    
    return url

def _generate_amap_url(origin: str, destination: str) -> str:
    """Generate Amap navigation URL
    
    使用高德地图URI API格式：
    https://uri.amap.com/navigation?from=起点&to=终点&mode=car
    """
    base_url = "https://uri.amap.com/navigation"
    params = {
        "from": origin,
        "to": destination,
        "mode": "car"  # car:驾车, bus:公交, walk:步行
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

def navigate(origin: str, destination: str, map_service: str = "amap") -> str:
    """
    Open map navigation from origin to destination
    
    Args:
        origin: Starting location
        destination: Target location
        map_service: Map service to use (amap, baidu, google)
                    默认使用高德地图(amap)，体验更好，会自动规划路线
    
    Returns:
        Status message
    """
    if not origin or not origin.strip() or not destination or not destination.strip():
        return "错误: 起点和终点不能为空"
    
    origin = origin.strip()
    destination = destination.strip()
    
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
        map_name = map_names.get(map_service, "高德地图")
        
        return (
            f"✅ {map_name}已打开\n\n"
            f"📍 起点：{origin}\n"
            f"📍 终点：{destination}\n"
            f"🔗 {url}\n\n"
            f"📌 下一步操作：\n"
            f"   1. 在打开的页面中确认起点和终点\n"
            f"   2. 点击【开始导航】或【路线规划】按钮\n"
            f"   3. 选择出行方式（驾车/公交/步行）"
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
    if not query or not query.strip():
        return "错误: 搜索关键词不能为空"
    
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
        map_name = map_names.get(map_service, "高德地图")
        return f"✅ 已在{map_name}搜索: {query}\n🔗 {url}"
    except Exception as e:
        return f"打开地图搜索失败: {e}"

TOOLS = {
    "navigate": navigate,
    "search_location": search_location,
}
