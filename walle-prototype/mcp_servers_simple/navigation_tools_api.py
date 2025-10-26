#!/usr/bin/env python3
"""
使用地图Web API的导航工具实现
支持高德地图、百度地图的Web API
"""

import requests
import webbrowser
from urllib.parse import urlencode
import json
from typing import Dict, Optional, Tuple

class MapAPIError(Exception):
    """地图API调用错误"""
    pass

class AmapAPI:
    """高德地图Web API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://restapi.amap.com/v3"
    
    def geocode(self, address: str) -> Optional[Dict]:
        """
        地理编码 - 将地址转换为坐标
        
        Args:
            address: 地址
            
        Returns:
            {"location": "经度,纬度", "address": "格式化地址"}
        """
        url = f"{self.base_url}/geocode/geo"
        params = {
            "key": self.api_key,
            "address": address,
            "output": "json"
        }
        
        try:
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") == "1" and data.get("geocodes"):
                geocode = data["geocodes"][0]
                location = geocode["location"]
                formatted_address = geocode.get("formatted_address", address)
                
                return {
                    "location": location,
                    "formatted_address": formatted_address
                }
            
            raise MapAPIError(f"未找到地址: {address}")
            
        except requests.RequestException as e:
            raise MapAPIError(f"API请求失败: {e}")
    
    def direction_driving(self, origin: str, destination: str) -> Dict:
        """
        驾车路线规划
        
        Args:
            origin: 起点
            destination: 终点
            
        Returns:
            路线信息
        """
        # 先获取起终点坐标
        origin_geo = self.geocode(origin)
        dest_geo = self.geocode(destination)
        
        if not origin_geo or not dest_geo:
            raise MapAPIError("无法获取起终点坐标")
        
        url = f"{self.base_url}/direction/driving"
        params = {
            "key": self.api_key,
            "origin": origin_geo["location"],
            "destination": dest_geo["location"],
            "extensions": "all",
            "output": "json"
        }
        
        try:
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") == "1":
                route = data.get("route", {})
                paths = route.get("paths", [])
                
                if paths:
                    best_path = paths[0]
                    distance = best_path.get("distance", 0)  # 米
                    duration = best_path.get("duration", 0)    # 秒
                    
                    # 格式化路段信息
                    steps = best_path.get("steps", [])
                    
                    return {
                        "origin": origin_geo["formatted_address"],
                        "destination": dest_geo["formatted_address"],
                        "distance": f"{distance / 1000:.1f}公里",
                        "duration": f"{duration / 60:.0f}分钟",
                        "steps": [
                            {
                                "instruction": step.get("instruction", ""),
                                "distance": step.get("road", "")
                            }
                            for step in steps[:5]  # 只显示前5个路段
                        ]
                    }
            
            raise MapAPIError("路线规划失败")
            
        except requests.RequestException as e:
            raise MapAPIError(f"API请求失败: {e}")


class BaiduAPI:
    """百度地图Web API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.map.baidu.com"
    
    def geocode(self, address: str) -> Optional[Dict]:
        """
        地理编码 - 将地址转换为坐标
        """
        url = f"{self.base_url}/geocoding/v3/"
        params = {
            "ak": self.api_key,
            "address": address,
            "output": "json"
        }
        
        try:
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") == 0:
                result = data.get("result", {})
                location = result.get("location", {})
                
                return {
                    "location": f"{location['lng']},{location['lat']}",
                    "formatted_address": result.get("formatted_address", address)
                }
            
            raise MapAPIError(f"未找到地址: {address}")
            
        except requests.RequestException as e:
            raise MapAPIError(f"API请求失败: {e}")
    
    def direction_driving(self, origin: str, destination: str) -> Dict:
        """
        驾车路线规划
        """
        # 先获取起终点坐标
        origin_geo = self.geocode(origin)
        dest_geo = self.geocode(destination)
        
        if not origin_geo or not dest_geo:
            raise MapAPIError("无法获取起终点坐标")
        
        # 百度API需要坐标顺序为纬度,经度
        origin_coords = origin_geo["location"].split(",")
        dest_coords = dest_geo["location"].split(",")
        origin_lat_lng = f"{origin_coords[1]},{origin_coords[0]}"
        dest_lat_lng = f"{dest_coords[1]},{dest_coords[0]}"
        
        url = f"{self.base_url}/direction/v2/driving"
        params = {
            "ak": self.api_key,
            "origin": origin_lat_lng,
            "destination": dest_lat_lng,
            "output": "json"
        }
        
        try:
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") == 0:
                result = data.get("result", {})
                routes = result.get("routes", [])
                
                if routes:
                    route = routes[0]
                    distance = route.get("distance", 0)  # 米
                    duration = route.get("duration", 0)  # 秒
                    
                    steps = route.get("steps", [])
                    
                    return {
                        "origin": origin_geo["formatted_address"],
                        "destination": dest_geo["formatted_address"],
                        "distance": f"{distance / 1000:.1f}公里",
                        "duration": f"{duration / 60:.0f}分钟",
                        "steps": [
                            {
                                "instruction": step.get("instructions", "")[:50],
                                "distance": ""
                            }
                            for step in steps[:5]
                        ]
                    }
            
            raise MapAPIError("路线规划失败")
            
        except requests.RequestException as e:
            raise MapAPIError(f"API请求失败: {e}")


def navigate_with_api(
    origin: str,
    destination: str,
    map_service: str = "amap",
    api_key: Optional[str] = None,
    use_api: bool = False
) -> str:
    """
    使用Web API进行导航
    
    Args:
        origin: 起点
        destination: 终点
        map_service: 地图服务 (amap, baidu)
        api_key: API密钥
        use_api: 是否使用API（如果False则直接打开网页）
        
    Returns:
        状态消息
    """
    if not origin or not destination:
        return "❌ 错误: 起点和终点不能为空"
    
    # 如果没有API Key或不使用API，则回退到普通导航
    if not use_api or not api_key:
        from mcp_servers_simple.navigation_tools import navigate
        return navigate(origin, destination, map_service)
    
    try:
        # 选择API
        if map_service == "amap":
            api = AmapAPI(api_key)
        elif map_service == "baidu":
            api = BaiduAPI(api_key)
        else:
            return f"❌ 不支持的地图服务: {map_service}"
        
        # 获取路线规划
        route_info = api.direction_driving(origin, destination)
        
        # 构建返回消息
        result = (
            f"🗺️  路线规划完成\n\n"
            f"📍 起点：{route_info['origin']}\n"
            f"📍 终点：{route_info['destination']}\n"
            f"🛣️  距离：{route_info['distance']}\n"
            f"⏱️  时间：{route_info['duration']}\n\n"
        )
        
        # 显示关键路段
        if route_info.get("steps"):
            result += "📋 主要路段：\n"
            for i, step in enumerate(route_info["steps"], 1):
                result += f"   {i}. {step['instruction'][:30]}...\n"
        
        return result
        
    except MapAPIError as e:
        return f"❌ 地图API错误: {e}"
    except Exception as e:
        return f"❌ 导航失败: {e}"


def get_api_key_info() -> str:
    """
    获取API Key配置说明
    """
    return """
📋 地图API配置说明：

1. 高德地图API
   申请地址: https://console.amap.com/dev/key/app
   免费配额: 每天30万次调用
   
   使用方法:
   export AMAP_API_KEY="your_api_key_here"

2. 百度地图API
   申请地址: https://lbsyun.baidu.com/apiconsole/key
   免费配额: 每天30万次调用
   
   使用方法:
   export BAIDU_API_KEY="your_api_key_here"

3. 在代码中使用:
   from navigation_tools_api import navigate_with_api
   
   result = navigate_with_api(
       "上海",
       "北京",
       map_service="amap",
       api_key=os.getenv("AMAP_API_KEY"),
       use_api=True
   )
"""
