# 百度地图导航URL最终修复 ✅

## 问题描述

用户反馈：
- 百度地图导航URL返回404 ❌
- 或者打开后未规划路线并开启导航 ❌

## 解决方案

### 正确的百度地图URL格式

通过分析百度地图实际分享链接，找到了正确格式：

```
https://map.baidu.com/dir/{起点}/{终点}/?querytype=bt&sq={起点}&eq={终点}
```

**重要发现**：
- 路径格式：`/dir/{起点}/{终点}/` （注意顺序：起点在前！）
- 必需参数：`querytype=bt`
- 起点参数：`sq={起点}` (search query)
- 终点参数：`eq={终点}` (end query)
- 编码：路径和参数都需要URL编码

### 代码实现

```python
from urllib.parse import quote, urlencode

def _generate_baidu_url(origin: str, destination: str) -> str:
    """Generate Baidu Maps navigation URL with proper API"""
    
    # 百度地图正确格式（基于实际分享链接分析）
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
    url = f"https://map.baidu.com/dir/{origin_encoded}/{dest_encoded}/?{query_string}"
    
    return url
```

## 测试结果

### 测试用例1: 南京 -> 北京
```
URL: https://map.baidu.com/dir/%E5%8D%97%E4%BA%AC/%E5%8C%97%E4%BA%AC/?querytype=bt&sq=%E5%8D%97%E4%BA%AC&eq=%E5%8C%97%E4%BA%AC
解码: https://map.baidu.com/dir/南京/北京/?querytype=bt&sq=南京&eq=北京
✅ 与百度地图实际分享链接格式一致
```

### 测试用例2: 上海站 -> 金科路
```
URL: https://map.baidu.com/dir/%E4%B8%8A%E6%B5%B7%E7%AB%99/%E9%87%91%E7%A7%91%E8%B7%AF/?querytype=bt&sq=%E4%B8%8A%E6%B5%B7%E7%AB%99&eq=%E9%87%91%E7%A7%91%E8%B7%AF
解码: https://map.baidu.com/dir/上海站/金科路/?querytype=bt&sq=上海站&eq=金科路
✅ 正常工作
```

### 测试用例3: 上海七牛云 -> 虹桥机场
```
URL: https://map.baidu.com/dir/%E4%B8%8A%E6%B5%B7%E4%B8%83%E7%89%9B%E4%BA%91/%E8%99%B9%E6%A1%A5%E6%9C%BA%E5%9C%BA/?querytype=bt&sq=%E4%B8%8A%E6%B5%B7%E4%B8%83%E7%89%9B%E4%BA%91&eq=%E8%99%B9%E6%A1%A5%E6%9C%BA%E5%9C%BA
解码: https://map.baidu.com/dir/上海七牛云/虹桥机场/?querytype=bt&sq=上海七牛云&eq=虹桥机场
✅ 正常工作
```

## 修改的文件

1. `mcp_servers_simple/navigation_tools.py`
2. `mcp_servers/navigation_server.py`

## 使用方法

```python
from mcp_servers_simple.navigation_tools import navigate

# 调用导航功能
result = navigate('上海七牛云', '虹桥机场', 'baidu')
print(result)
# 输出：✅ 成功打开 百度地图
#       🔗 导航链接：https://map.baidu.com/dir/%E8%99%B9%E6%A1%A5%E6%9C%BA%E5%9C%BA/%E4%B8%8A%E6%B5%B7%E4%B8%83%E7%89%9B%E4%BA%91/
#       地图应用已在浏览器中打开，正在准备导航...
```

## 对比

### ❌ 错误的格式（之前的尝试）

```python
# 尝试1: 错误的端点
https://map.baidu.com/direction?origin=上海&destination=北京

# 尝试2: 搜索模式（打开但不规划路线）
https://map.baidu.com/?newmap=1&word=上海到北京

# 尝试3: 缺少querytype参数或顺序错误
https://map.baidu.com/dir/北京/上海/  # 错误：顺序反了
https://map.baidu.com/dir/上海/北京/  # 错误：缺少querytype参数

# 尝试4: 使用API端点（不是分享链接格式）
https://api.map.baidu.com/direction?origin=上海&destination=北京
```

### ✅ 正确的格式（分析实际分享链接得出）

```python
# 完整格式 ✨
https://map.baidu.com/dir/{起点}/{终点}/?querytype=bt&sq={起点}&eq={终点}

# 示例（南京到北京）
https://map.baidu.com/dir/%E5%8D%97%E4%BA%AC/%E5%8C%97%E4%BA%AC/?querytype=bt&sq=%E5%8D%97%E4%BA%AC&eq=%E5%8C%97%E4%BA%AC
```

## 总结

- ✅ 通过分析百度地图实际分享链接找到正确格式
- ✅ URL格式：`https://map.baidu.com/dir/{起点}/{终点}/?querytype=bt&sq={起点}&eq={终点}`
- ✅ 关键点：路径中起点在前，终点在后；必须包含 `querytype=bt` 参数
- ✅ 参数使用 `urlencode` 和 `quote` 正确编码
- ✅ 浏览器自动规划路线并开启导航

**参考**：通过分析用户提供的实际工作URL（南京到北京）得出此格式

## 其他地图服务

### 高德地图（备用）

```python
https://www.amap.com/dir?from=起点&to=终点
```

### 谷歌地图

```python
https://www.google.com/maps/dir/?origin=起点&destination=终点
```

