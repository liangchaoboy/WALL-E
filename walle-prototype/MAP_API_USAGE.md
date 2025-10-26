# 地图Web API使用指南

## 概述

本功能使用高德地图和百度地图的Web API，可以：
- ✅ **获取详细路线信息**：距离、预计时间、途径路段
- ✅ **不需要用户手动操作**：直接返回路线规划结果
- ✅ **可以集成到语音播报**：把路线信息读给用户听

## 申请API密钥

### 高德地图API（推荐）

1. **注册账号**
   - 访问: https://console.amap.com/
   - 使用支付宝账号快速注册

2. **创建应用**
   - 登录控制台
   - 应用管理 → 创建新应用
   - 应用名称：WALL-E

3. **添加Key**
   - 在应用中添加Key
   - 类型选择：Web服务
   - 服务选择：Web服务API
   - 提交后获取Key

4. **免费配额**
   - 每天30万次调用
   - 足够个人和小规模使用

### 百度地图API

1. **注册账号**
   - 访问: https://lbsyun.baidu.com/
   - 使用手机号注册

2. **创建应用**
   - 控制台 → 应用管理 → 创建应用
   - 应用名称：WALL-E
   - 应用类型：服务端

3. **配置服务**
   - 点击应用 → 添加Key
   - 服务类型：Geocoding API、Route Planning API
   - 白名单：可设置0.0.0.0/0允许所有IP

4. **免费配额**
   - 每天30万次调用

## 配置使用

### 方法1：环境变量（推荐）

```bash
# 复制配置模板
cp .env.example .env

# 编辑配置
vim .env

# 添加你的API密钥
AMAP_API_KEY=your_amap_api_key_here
BAIDU_API_KEY=your_baidu_api_key_here
```

### 方法2：直接传参

```python
from mcp_servers_simple.navigation_tools_api import navigate_with_api

result = navigate_with_api(
    origin="上海",
    destination="北京",
    map_service="amap",
    api_key="your_api_key",
    use_api=True
)

print(result)
```

## 使用示例

### 基础使用

```python
from mcp_servers_simple.navigation_tools_api import navigate_with_api
import os

# 从环境变量读取
result = navigate_with_api(
    origin="上海七牛云",
    destination="虹桥机场",
    map_service="amap",
    api_key=os.getenv("AMAP_API_KEY"),
    use_api=True
)

print(result)
```

**输出示例**：
```
🗺️  路线规划完成

📍 起点：上海市浦东新区金科路
📍 终点：虹桥国际机场
🛣️  距离：25.3公里
⏱️  时间：42分钟

📋 主要路段：
   1. 金科路 → 科苑路
   2. 科苑路 → 中环高架
   3. 中环高架 → 延安西路
   4. 延安西路 → 虹桥机场
   5. 到达虹桥国际机场
```

### 在语音助手中使用

```python
import os
from mcp_servers_simple.navigation_tools_api import navigate_with_api

def voice_navigate(origin: str, destination: str):
    """语音导航"""
    
    # 使用API获取路线信息
    result = navigate_with_api(
        origin=origin,
        destination=destination,
        map_service="amap",
        api_key=os.getenv("AMAP_API_KEY"),
        use_api=True
    )
    
    # 可以播放这个结果
    return result

# 使用
info = voice_navigate("上海七牛云", "虹桥机场")
print(info)
```

### 集成到MCP工具

```python
# 在 mcp_servers/navigation_server.py 中添加API版本

@mcp.tool()
def navigate_with_details(
    origin: str,
    destination: str,
    map_service: str = "amap",
    use_api: bool = False
) -> str:
    """
    导航（带详细信息）
    
    Args:
        origin: 起点
        destination: 终点
        map_service: 地图服务 (amap, baidu)
        use_api: 是否使用API获取详细信息
    """
    if use_api:
        from mcp_servers_simple.navigation_tools_api import navigate_with_api
        
        api_key = os.getenv(
            "AMAP_API_KEY" if map_service == "amap" else "BAIDU_API_KEY"
        )
        
        return navigate_with_api(
            origin, destination, map_service, api_key, use_api=True
        )
    else:
        # 回退到普通导航
        from mcp_servers_simple.navigation_tools import navigate
        return navigate(origin, destination, map_service)
```

## 优势对比

| 特性 | 普通导航（无API） | API导航 |
|------|-----------------|---------|
| 是否需要API Key | ❌ 不需要 | ✅ 需要 |
| 打开方式 | 浏览器打开地图 | 返回文字信息 |
| 自动开始导航 | ⚠️ 需要手动点击 | ✅ 自动返回路线 |
| 获取详细信息 | ❌ 无法获取 | ✅ 距离、时间、路段 |
| 可以语音播报 | ⚠️ 只能播报基础信息 | ✅ 完整路线信息 |
| 网页展示 | ✅ 可视化地图 | ❌ 纯文字信息 |
| 适合场景 | 需要查看地图 | 纯语音交互 |

## 完整示例：语音导航助手

```python
#!/usr/bin/env python3
"""带API的语音导航"""

import os
from mcp_servers_simple.navigation_tools_api import navigate_with_api

def smart_navigate(user_query: str):
    """
    智能导航 - 从用户输入提取起终点
    例如: "从上海到北京" → origin="上海", destination="北京"
    """
    
    # TODO: 使用AI提取起终点（这里简化处理）
    if "从" in user_query and "到" in user_query:
        parts = user_query.split("到")
        origin = parts[0].replace("从", "").strip()
        destination = parts[1].strip()
    else:
        return "❌ 请使用格式：从[起点]到[终点]"
    
    # 使用API获取详细路线
    result = navigate_with_api(
        origin=origin,
        destination=destination,
        map_service="amap",
        api_key=os.getenv("AMAP_API_KEY"),
        use_api=True
    )
    
    return result

# 测试
if __name__ == "__main__":
    print(smart_navigate("从上海七牛云到虹桥机场"))
```

## 错误处理

```python
try:
    result = navigate_with_api(
        origin="起点",
        destination="终点",
        map_service="amap",
        api_key="invalid_key",
        use_api=True
    )
except Exception as e:
    print(f"❌ 错误: {e}")
    # 自动回退到普通导航
    from navigation_tools import navigate
    result = navigate("起点", "终点", "amap")
```

## 成本说明

### 高德地图
- **免费配额**: 每天30万次
- **个人使用**: 完全够用
- **超出后**: 按量计费，0.1元/千次

### 百度地图
- **免费配额**: 每天30万次
- **个人使用**: 完全够用
- **超出后**: 需购买服务包

## 最佳实践

### 1. 根据场景选择

```python
# 如果需要用户查看地图 → 使用普通导航
navigate("起点", "终点", "amap")

# 如果是纯语音交互 → 使用API导航
navigate_with_api("起点", "终点", "amap", api_key, use_api=True)
```

### 2. 优雅降级

```python
def navigate_smart(origin, destination, map_service="amap"):
    """智能导航 - 优先使用API，失败则回退"""
    
    try:
        api_key = os.getenv("AMAP_API_KEY")
        if api_key:
            return navigate_with_api(
                origin, destination, map_service, api_key, use_api=True
            )
    except Exception:
        pass  # API失败，回退到普通导航
    
    # 回退到普通导航
    from navigation_tools import navigate
    return navigate(origin, destination, map_service)
```

### 3. 缓存结果

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_navigate(origin, destination):
    """缓存常见路线，减少API调用"""
    return navigate_with_api(
        origin, destination, "amap", api_key, use_api=True
    )
```

## 总结

✅ **使用API的优势**：
- 获取详细路线信息
- 适合语音助手（无需手动操作）
- 可以集成到任何应用中

⚠️ **注意事项**：
- 需要申请API密钥
- 有调用配额限制
- 纯文字输出，不可视化

**推荐使用场景**：
- 纯语音交互场景
- 需要播报详细路线
- 需要集成到其他系统

**推荐方案**：
- 原型阶段：使用普通导航（简单快速）
- 完整产品：前端集成地图SDK（最佳体验）
- 语音场景：使用Web API（无需用户操作）

