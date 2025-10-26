# demo_mcp.py 详细使用说明

## 📖 概述

`demo_mcp.py` 是 WALL-E 项目的第一个示例代码,用于演示 MCP (Model Context Protocol) 功能集成。该脚本无需语音输入,直接测试 MCP 客户端的所有功能,帮助开发者快速了解和验证 WALL-E 的核心能力。

## 🎯 功能特性

### 核心功能
- ✅ **MCP 客户端初始化** - 自动加载所有 MCP 服务器
- ✅ **工具发现** - 列出所有可用的 MCP 工具
- ✅ **工具测试** - 逐个测试导航、天气、音乐等工具
- ✅ **AI 集成测试** - 演示 AI 如何理解自然语言并调用相应工具

### 支持的工具类型
1. **导航工具** (Navigation)
   - `navigate` - 地图导航(起点 → 终点)
   - `search_location` - 搜索地点

2. **天气工具** (Weather)
   - `get_weather` - 查询天气
   - `compare_weather` - 对比两个城市的天气

3. **音乐工具** (Music)
   - `play_music` - 播放音乐
   - `search_playlist` - 搜索歌单

## 🚀 快速开始

### 前置要求

1. **Python 环境**
   - Python 3.8 或更高版本
   - 推荐使用 Python 3.10+

2. **系统要求**
   - 支持 macOS, Linux, Windows
   - 需要联网环境
   - 需要浏览器(用于打开地图、天气等页面)

### 步骤 1: 安装依赖

进入项目目录并安装所需的 Python 包:

```bash
cd walle-prototype
pip install -r requirements.txt
```

**依赖包说明:**
- `openai` - 用于调用 AI 模型
- `python-dotenv` - 用于加载环境变量
- `mcp` (可选) - 完整 MCP 协议支持

### 步骤 2: 配置环境变量

1. 复制环境变量模板:
```bash
cp .env.example .env
```

2. 编辑 `.env` 文件,填入你的 API 配置:
```bash
# 必填: API Key
API_KEY=sk-your-api-key-here

# 必填: API 基础 URL
BASE_URL=https://api.openai.com/v1

# 必填: 模型名称
MODEL=gpt-3.5-turbo
```

**支持的 AI 服务商:**
- **OpenAI**: 
  ```
  BASE_URL=https://api.openai.com/v1
  MODEL=gpt-3.5-turbo 或 gpt-4
  ```
- **DeepSeek**:
  ```
  BASE_URL=https://api.deepseek.com/v1
  MODEL=deepseek-chat
  ```
- **其他兼容 OpenAI API 的服务**: 只需修改 BASE_URL 和 MODEL

### 步骤 3: 运行示例

```bash
python demo_mcp.py
```

## 📊 运行流程详解

### 阶段 1: 初始化 (约 1-2 秒)

```
1️⃣  初始化 MCP 客户端...
```

**发生的事情:**
- 加载 MCP 客户端配置
- 扫描 `mcp_servers/` 目录
- 启动所有可用的 MCP 服务器
- 建立客户端与服务器的连接

### 阶段 2: 工具发现 (即时)

```
2️⃣  列出所有可用工具:
   1. navigate
   2. search_location
   3. get_weather
   4. compare_weather
   5. play_music
   6. search_playlist
```

**发生的事情:**
- 查询所有已注册的 MCP 服务器
- 收集每个服务器提供的工具列表
- 去重并按字母顺序排序
- 展示给用户

### 阶段 3: 工具测试 (约 5-10 秒)

#### 导航工具测试
```
📍 导航工具测试:
   - navigate(上海, 北京)
   ✅ 已打开baidu地图: 上海 → 北京
   
   - search_location(虹桥机场)
   ✅ 已搜索baidu地图: 虹桥机场
```

**实际效果:**
- 打开默认浏览器
- 自动访问百度地图
- 显示导航路线或搜索结果

#### 天气工具测试
```
🌤️  天气工具测试:
   - get_weather(上海, 明天)
   ✅ 已打开天气查询: 上海 (明天)
   
   - compare_weather(北京, 上海)
   ✅ 已打开天气对比: 北京 vs 上海
```

**实际效果:**
- 打开天气查询网站
- 显示指定城市的天气信息
- 支持单城市查询和双城市对比

#### 音乐工具测试
```
🎵 音乐工具测试:
   - play_music(晴天, 周杰伦)
   ✅ 已在qq音乐搜索: 晴天 - 周杰伦
   
   - search_playlist(流行音乐)
   ✅ 已在qq音乐搜索歌单: 流行音乐
```

**实际效果:**
- 打开 QQ 音乐网页版
- 搜索指定歌曲或歌单
- 用户可以直接播放

### 阶段 4: AI 集成测试 (约 10-15 秒,可选)

**前提条件:** 必须配置 `.env` 文件中的 `API_KEY`

```
4️⃣  测试 AI + MCP 集成:

   用户: 从上海七牛云到虹桥机场
   AI理解: {"tool": "navigate", "params": {"origin": "上海七牛云", "destination": "虹桥机场"}}
   执行结果: 已打开baidu地图: 上海七牛云 → 虹桥机场
   
   用户: 查看明天北京的天气
   AI理解: {"tool": "get_weather", "params": {"city": "北京", "date": "明天"}}
   执行结果: 已打开天气查询: 北京 (明天)
   
   用户: 播放周杰伦的七里香
   AI理解: {"tool": "play_music", "params": {"song": "七里香", "artist": "周杰伦"}}
   执行结果: 已在qq音乐搜索: 七里香 - 周杰伦
```

**发生的事情:**
1. 脚本发送自然语言到 AI 模型
2. AI 分析用户意图,选择合适的工具
3. AI 提取参数并返回 JSON 格式
4. MCP 客户端调用对应工具
5. 工具执行并返回结果

**如果未配置 API_KEY:**
```
⚠️  未配置 API_KEY,跳过 AI 集成测试
   提示: 配置 .env 文件后可测试完整的 AI + MCP 功能
```

### 阶段 5: 完成

```
✅ MCP 功能演示完成!

📖 下一步:
   1. 运行 'python voice_nav_mcp.py' 测试语音助手
   2. 阅读 README_MCP.md 了解更多信息
   3. 添加自己的 MCP Server 扩展功能

🚀 WALL-E MCP 架构让扩展更简单!
```

## 🔧 配置选项

### 环境变量详解

| 变量名 | 必填 | 说明 | 示例 |
|--------|------|------|------|
| `API_KEY` | 否* | AI 服务的 API 密钥 | `sk-xxxxx` |
| `BASE_URL` | 否* | AI 服务的基础 URL | `https://api.openai.com/v1` |
| `MODEL` | 否* | 使用的模型名称 | `gpt-3.5-turbo` |

> *注: 如果不配置,脚本仍可运行阶段 1-3,但会跳过阶段 4 的 AI 集成测试

### MCP 服务器配置

默认加载的服务器位于 `mcp_servers/` 目录:
- `navigation_server.py` - 导航服务
- `weather_server.py` - 天气服务  
- `music_server.py` - 音乐服务

**自定义服务器:**
你可以在 `mcp_servers/` 目录添加自己的服务器,客户端会自动发现并加载。

## 🎓 使用场景

### 场景 1: 快速验证环境

在开发新功能前,先运行 `demo_mcp.py` 确保:
- Python 环境配置正确
- 依赖包已安装
- MCP 服务器正常工作
- AI API 可以正常调用

```bash
python demo_mcp.py
```

预期: 所有测试通过,没有错误信息

### 场景 2: 调试 MCP 工具

当添加新的 MCP 服务器或修改现有工具时:
1. 将新服务器文件放入 `mcp_servers/`
2. 运行 `demo_mcp.py`
3. 检查工具是否出现在列表中
4. 观察工具调用是否成功

### 场景 3: 演示项目能力

向他人展示 WALL-E 的功能时:
```bash
python demo_mcp.py
```

**演示要点:**
- 展示支持的工具类型(导航、天气、音乐)
- 展示工具的实际调用效果(浏览器自动打开)
- 如果配置了 API,展示 AI 如何理解自然语言

### 场景 4: 学习 MCP 架构

对于新加入项目的开发者:
1. 先运行 `demo_mcp.py` 了解整体功能
2. 阅读脚本源码理解调用流程
3. 查看 `mcp_servers/` 了解服务器实现
4. 参考 `mcp_client.py` 学习客户端实现

## ❓ 常见问题

### Q1: 运行时报错 "ModuleNotFoundError: No module named 'openai'"

**原因:** 未安装依赖包

**解决:**
```bash
pip install -r requirements.txt
```

### Q2: 运行时报错 "FileNotFoundError: [Errno 2] No such file or directory: '.env'"

**原因:** 未创建 `.env` 文件

**解决:**
```bash
cp .env.example .env
# 然后编辑 .env 文件
```

### Q3: AI 集成测试失败,报错 "AuthenticationError"

**原因:** API_KEY 配置错误或已过期

**解决:**
1. 检查 `.env` 文件中的 `API_KEY` 是否正确
2. 确认 API Key 没有过期
3. 确认账户有足够的额度

### Q4: 工具调用后浏览器没有打开

**可能原因:**
1. 系统没有设置默认浏览器
2. 浏览器被防火墙拦截
3. 权限不足

**解决:**
- 设置系统默认浏览器
- 检查防火墙设置
- 以管理员权限运行

### Q5: 只想测试工具,不想测试 AI 集成

**解决:** 
删除或注释掉 `.env` 文件中的 `API_KEY` 行:
```bash
# API_KEY=sk-xxxxx
```

脚本会自动跳过阶段 4 的 AI 集成测试。

### Q6: 想使用本地 AI 模型

**解决:**
如果你有本地部署的兼容 OpenAI API 的服务(如 LocalAI, Ollama with OpenAI compatibility):
```bash
BASE_URL=http://localhost:8080/v1
MODEL=your-local-model
API_KEY=not-needed  # 有些本地服务需要,有些不需要
```

## 🔍 深入理解

### 脚本结构

```python
# 1. 导入依赖
import os, json
from openai import OpenAI
from dotenv import load_dotenv
from mcp_client import create_mcp_client

# 2. 初始化环境
load_dotenv()  # 加载 .env 文件

# 3. 创建 MCP 客户端
mcp_client = create_mcp_client()

# 4. 列出工具
tools = mcp_client.list_tools()

# 5. 测试工具
result = mcp_client.call_tool("tool_name", param1=value1)

# 6. AI 集成测试(可选)
if os.getenv("API_KEY"):
    # 调用 AI 模型
    # 解析 AI 返回的工具和参数
    # 执行工具调用
```

### MCP 客户端工作原理

`mcp_client.py` 提供的核心功能:

1. **create_mcp_client()** - 创建客户端实例
   - 扫描 `mcp_servers/` 目录
   - 启动每个服务器
   - 建立连接

2. **list_tools()** - 获取所有工具
   - 查询每个服务器
   - 收集工具列表
   - 返回工具名称数组

3. **call_tool(name, **kwargs)** - 调用工具
   - 找到工具所属的服务器
   - 传递参数
   - 执行并返回结果

### 工具命名约定

所有工具名称使用 `<server>.<tool>` 格式:
- `navigation.navigate` → 导航工具的导航功能
- `weather.get_weather` → 天气工具的查询功能
- `music.play_music` → 音乐工具的播放功能

在脚本中为了简化展示,去掉了服务器前缀。

## 📈 进阶使用

### 添加自定义测试

你可以修改 `demo_mcp.py`,添加自己的测试用例:

```python
# 在脚本末尾添加
print("\n🧪 自定义测试:")
print("   - 测试其他城市天气")
result = mcp_client.call_tool("get_weather", city="杭州", date="今天")
print(f"   ✅ {result}")
```

### 批量测试

创建一个测试配置文件,批量执行:

```python
test_cases = [
    {"tool": "navigate", "params": {"origin": "A", "destination": "B"}},
    {"tool": "get_weather", "params": {"city": "上海"}},
    # 更多测试...
]

for test in test_cases:
    result = mcp_client.call_tool(test["tool"], **test["params"])
    print(f"✅ {test['tool']}: {result}")
```

### 集成到 CI/CD

在持续集成环境中运行:

```bash
# .github/workflows/test.yml
- name: Test MCP Integration
  run: python walle-prototype/demo_mcp.py
  env:
    API_KEY: ${{ secrets.API_KEY }}
    BASE_URL: ${{ secrets.BASE_URL }}
    MODEL: gpt-3.5-turbo
```

## 🔗 相关资源

### 项目文档
- [README.md](./README.md) - 项目总览
- [README_MCP.md](./README_MCP.md) - MCP 架构详解
- [README_TESTS.md](./README_TESTS.md) - 测试说明
- [../PRD.md](../PRD.md) - 产品需求文档

### 代码文件
- [demo_mcp.py](./demo_mcp.py) - 本示例脚本
- [mcp_client.py](./mcp_client.py) - MCP 客户端实现
- [mcp_servers/](./mcp_servers/) - MCP 服务器实现
- [voice_nav_mcp.py](./voice_nav_mcp.py) - 语音助手(下一步)

### 外部资源
- [MCP 官方文档](https://modelcontextprotocol.io)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [OpenAI API 文档](https://platform.openai.com/docs)

## 🎯 下一步

完成 `demo_mcp.py` 测试后,建议:

1. **运行语音助手**
   ```bash
   python voice_nav_mcp.py
   ```
   体验完整的语音交互功能

2. **阅读 MCP 架构文档**
   ```bash
   cat README_MCP.md
   ```
   深入了解 MCP 架构设计

3. **添加自定义工具**
   - 在 `mcp_servers/` 创建新服务器
   - 实现自己的工具
   - 重新运行 `demo_mcp.py` 验证

4. **查看测试代码**
   ```bash
   python test_demo_mcp.py
   ```
   了解如何编写单元测试

## 💡 提示与技巧

1. **首次运行** - 建议先不配置 API_KEY,只测试工具基础功能
2. **网络问题** - 如果访问 OpenAI 有困难,可以使用国内的 AI 服务商
3. **浏览器选择** - 建议使用 Chrome/Edge 以获得最佳体验
4. **调试模式** - 可以在代码中添加 `print()` 语句查看中间结果
5. **工具扩展** - MCP 架构设计让添加新工具非常简单,鼓励尝试

## 📝 反馈与贡献

如果你在使用过程中遇到问题或有改进建议:
- 提交 Issue: [GitHub Issues](https://github.com/liangchaoboy/WALL-E/issues)
- 提交 PR: [GitHub Pull Requests](https://github.com/liangchaoboy/WALL-E/pulls)

---

**祝你使用愉快! 🎉**
