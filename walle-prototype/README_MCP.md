# WALL-E MCP 集成版本

基于 Model Context Protocol (MCP) 的可扩展架构版本。

## 🎯 什么是 MCP?

MCP (Model Context Protocol) 是一个开放协议,用于在 AI 应用和外部工具之间建立标准化连接。

### MCP 的优势

- **可扩展性**: 通过插件化架构轻松添加新功能
- **标准化**: 统一的工具接口和调用方式
- **解耦**: AI 逻辑与工具实现分离
- **可维护**: 每个工具独立开发和测试

## 📁 项目结构

```
walle-prototype/
├── mcp_servers/              # MCP 服务器目录
│   ├── navigation_server.py  # 地图导航工具
│   ├── weather_server.py     # 天气查询工具
│   └── music_server.py       # 音乐播放工具
├── mcp_client.py             # MCP 客户端
├── voice_nav_mcp.py          # MCP 版语音助手
├── voice_nav.py              # 原始版本(保留)
└── requirements.txt          # 依赖包含 mcp>=1.0.0
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件,填入 API_KEY, BASE_URL, MODEL
```

### 3. 测试 MCP 客户端

```bash
python mcp_client.py
```

这会显示所有可用的工具并执行测试调用。

### 4. 运行语音助手

```bash
python voice_nav_mcp.py
```

## 🔧 可用工具

### 导航工具 (Navigation)

- `navigate(origin, destination, map_service="baidu")` - 地图导航
- `search_location(query, map_service="baidu")` - 搜索地点

### 天气工具 (Weather)

- `get_weather(city, date="today")` - 查询天气
- `compare_weather(city1, city2)` - 对比天气

### 音乐工具 (Music)

- `play_music(song, artist="", platform="qq")` - 播放音乐
- `search_playlist(keyword, platform="qq")` - 搜索歌单

## 📝 使用示例

### 示例 1: 地图导航

```
用户: "从上海到北京"
系统: [调用 navigate 工具] 打开百度地图导航
```

### 示例 2: 天气查询

```
用户: "查看明天上海的天气"
系统: [调用 get_weather 工具] 打开天气查询页面
```

### 示例 3: 播放音乐

```
用户: "播放周杰伦的晴天"
系统: [调用 play_music 工具] 在QQ音乐搜索并播放
```

### 示例 4: 组合查询

```
用户: "对比北京和上海的天气"
系统: [调用 compare_weather 工具] 打开天气对比页面
```

## 🔌 添加新的 MCP 工具

### 步骤 1: 创建 MCP Server

在 `mcp_servers/` 目录下创建新的服务器文件:

```python
# mcp_servers/calculator_server.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Calculator")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract b from a"""
    return a - b
```

### 步骤 2: 注册到 MCP Client

在 `mcp_client.py` 的 `create_mcp_client()` 函数中添加:

```python
server_modules = {
    "navigation": servers_dir / "navigation_server.py",
    "weather": servers_dir / "weather_server.py",
    "music": servers_dir / "music_server.py",
    "calculator": servers_dir / "calculator_server.py",  # 新增
}
```

### 步骤 3: 更新 AI 提示词

在 `voice_nav_mcp.py` 的 `understand_with_mcp()` 函数中添加工具描述:

```python
tools_description = """
可用工具:
1. navigate(...) - 地图导航
2. get_weather(...) - 查询天气
3. play_music(...) - 播放音乐
4. add(a, b) - 加法计算  # 新增
5. subtract(a, b) - 减法计算  # 新增
"""
```

### 步骤 4: 测试

```bash
python mcp_client.py
python voice_nav_mcp.py
```

## 🏗️ 架构说明

### MCP 架构流程

```
用户语音/文字
    ↓
语音识别 (STT)
    ↓
AI 理解 (LLM) → 选择工具和参数
    ↓
MCP Client → 调用对应的 MCP Server
    ↓
MCP Server → 执行具体操作
    ↓
返回结果
```

### 关键组件

1. **MCP Servers** (`mcp_servers/*.py`)
   - 独立的工具服务器
   - 使用 FastMCP 框架定义工具
   - 每个工具有明确的输入输出

2. **MCP Client** (`mcp_client.py`)
   - 管理所有 MCP Server
   - 提供统一的工具调用接口
   - 处理工具发现和路由

3. **语音助手** (`voice_nav_mcp.py`)
   - 集成语音识别
   - 使用 LLM 理解意图
   - 通过 MCP Client 调用工具

## 🆚 对比原始版本

| 特性 | 原始版本 | MCP 版本 |
|------|---------|---------|
| 架构 | 单体代码 | 插件化 MCP |
| 工具数量 | 1 个(导航) | 6+ 个 |
| 扩展性 | 需修改主代码 | 添加新 Server |
| 维护性 | 耦合度高 | 解耦独立 |
| 标准化 | 自定义 | MCP 标准 |

## 🧪 测试

### 测试 MCP Client

```bash
python mcp_client.py
```

预期输出:
```
✅ 注册 MCP Server: navigation
✅ 注册 MCP Server: weather
✅ 注册 MCP Server: music

📋 可用工具:
  - navigate
  - search_location
  - get_weather
  - compare_weather
  - play_music
  - search_playlist

🧪 测试工具调用:
1. 测试导航工具:
   已打开baidu地图: 上海 → 北京
...
```

### 测试语音助手

```bash
python voice_nav_mcp.py
```

预期流程:
1. 启动后显示已加载工具数量
2. 说出指令(如 "从上海到北京")
3. AI 理解并选择 navigate 工具
4. 调用工具打开地图
5. 显示执行结果

## 📚 相关资源

- [MCP 官方文档](https://modelcontextprotocol.io)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [WALL-E PRD](../PRD.md)
- [WALL-E 架构设计](../docs/架构设计文档.md)

## ⚠️ 已知限制

- 需要 Python 3.10+
- 需要联网(语音识别和 LLM)
- 需要配置第三方 LLM API
- 需要麦克风权限
- 工具调用结果依赖浏览器打开

## 🎉 下一步

1. 添加更多 MCP Server (系统控制、应用启动等)
2. 实现本地工具(不依赖浏览器)
3. 添加 GUI 界面
4. 支持唤醒词
5. 优化错误处理和重试机制
6. 添加工具调用历史记录

---

**MCP 让 WALL-E 更强大、更灵活!** 🚀
