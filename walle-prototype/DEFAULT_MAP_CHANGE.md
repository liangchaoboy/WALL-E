# 默认地图服务变更说明

## 变更内容

**默认地图服务已从百度地图改为高德地图**

## 变更原因

1. **用户体验问题**：百度地图网页版打开后不会自动规划路线，需要用户手动点击"开始导航"
2. **自动化需求**：高德地图网页版会自动规划并显示路线，更符合语音助手的自动化需求
3. **URL稳定性**：高德地图的URL格式更简单稳定

## 修改的文件

1. `mcp_servers_simple/navigation_tools.py` - 默认参数改为 `map_service="amap"`
2. `mcp_servers/navigation_server.py` - 默认参数改为 `map_service="amap"`

## 使用说明

### 默认使用（高德地图）

```python
from mcp_servers_simple.navigation_tools import navigate

# 不指定地图服务，默认使用高德
result = navigate("南京", "北京")
# URL: https://www.amap.com/dir?from=南京&to=北京
# ✅ 自动规划路线并显示
```

### 明确指定地图服务

```python
# 使用高德地图
result = navigate("上海", "北京", "amap")

# 使用百度地图（备选）
result = navigate("上海", "北京", "baidu")
# ⚠️ 注意：需要用户手动点击'开始导航'

# 使用谷歌地图
result = navigate("Shanghai", "Beijing", "google")
```

## 地图服务对比

| 地图服务 | URL示例 | 自动规划 | 用户操作 | 推荐度 |
|---------|---------|---------|---------|--------|
| 高德地图(默认) | `https://www.amap.com/dir?from=...&to=...` | ✅ 是 | 无需操作 | ⭐⭐⭐⭐⭐ |
| 百度地图(备选) | `https://map.baidu.com/dir/.../?querytype=bt&...` | ❌ 否 | 需点击导航 | ⭐⭐⭐ |
| 谷歌地图 | `https://www.google.com/maps/dir/?...` | ✅ 是 | 无需操作 | ⭐⭐⭐⭐ (国内不可用) |

## 测试结果

### 测试1：南京 → 北京
```
✅ 成功打开 高德地图
📍 起点：南京
📍 终点：北京
🔗 导航链接：https://www.amap.com/dir?from=%E5%8D%97%E4%BA%AC&to=%E5%8C%97%E4%BA%AC
地图应用已在浏览器中打开，正在准备导航...
```
✅ 高德地图自动规划路线

### 测试2：上海七牛云 → 虹桥机场
```
✅ 成功打开 高德地图
📍 起点：上海七牛云
📍 终点：虹桥机场
🔗 导航链接：https://www.amap.com/dir?from=%E4%B8%8A%E6%B5%B7%E4%B8%83%E7%89%9B%E4%BA%91&to=%E8%99%B9%E6%A1%A5%E6%9C%BA%E5%9C%BA
```
✅ 自动显示路线

### 测试3：上海站 → 金科路
```
✅ 成功打开 高德地图
📍 起点：上海站
📍 终点：金科路
🔗 导航链接：https://www.amap.com/dir?from=%E4%B8%8A%E6%B5%B7%E7%AB%99&to=%E9%87%91%E7%A7%91%E8%B7%AF
```
✅ 正常工作

## 向后兼容

- ✅ 保留了所有地图服务的支持
- ✅ 用户仍可通过参数选择百度地图或其他地图
- ✅ 只是改变了默认值，不影响现有代码

## 建议

**推荐使用默认的高德地图**，因为：
1. 自动规划路线，用户体验更好
2. 无需手动操作
3. URL格式简单稳定

如果有特殊需求需要使用百度地图，可以明确指定：
```python
navigate(origin, destination, "baidu")
```

## 总结

这次变更显著改善了用户体验：
- ✅ 从"打开地图后需要手动操作"变为"自动规划并显示路线"
- ✅ 更符合语音助手的自动化定位
- ✅ 保持了灵活性，用户仍可选择其他地图服务

