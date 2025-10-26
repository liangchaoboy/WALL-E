# 高德地图URL修复说明

## 问题描述

用户反馈：打开高德地图后导航地址不对

## 原因分析

原URL格式：
```
https://www.amap.com/dir?from=起点&to=终点
```

这个URL会打开高德地图的路线规划页面，但存在以下问题：
- ❌ 不会自动规划路线
- ❌ 页面显示不正确
- ❌ 用户体验差

## 解决方案

改用高德地图URI API：
```
https://uri.amap.com/navigation?from=起点&to=终点&mode=car
```

### URL参数说明
- `from`: 起点位置
- `to`: 终点位置  
- `mode`: 出行方式
  - `car`: 驾车（默认）
  - `bus`: 公交
  - `walk`: 步行

## 修改内容

### 修改的文件
1. `mcp_servers_simple/navigation_tools.py`
2. `mcp_servers/navigation_server.py`

### 修改内容
```python
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
```

## 测试结果

### 测试命令
```python
from mcp_servers_simple.navigation_tools import _generate_amap_url
url = _generate_amap_url('上海', '北京')
print(url)
```

### 输出
```
https://uri.amap.com/navigation?from=%E4%B8%8A%E6%B5%B7&to=%E5%8C%97%E4%BA%AC&mode=car
```

解码后：
```
https://uri.amap.com/navigation?from=上海&to=北京&mode=car
```

## 预期效果

✅ **新URL应该**：
- 自动打开高德地图
- 自动规划从起点到终点的驾车路线
- 显示完整的地图界面

⚠️ **注意事项**：
- URI API主要支持移动端高德地图APP
- 桌面端（浏览器）可能仍需要手动操作
- 如果需要完全自动的导航体验，建议使用Web API（见MAP_API_USAGE.md）

## 相关文档

- `MAP_API_USAGE.md` - Web API详细使用方法
- `MAP_NAVIGATION_LIMITATION.md` - 网页版限制说明
- `NAVIGATION_CURRENT_STATUS.md` - 当前状态总结

