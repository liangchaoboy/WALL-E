# WALL-E 语音导航原型

1天快速开发版本,现已支持 MCP (Model Context Protocol) 架构!

## 🎯 版本说明

- **voice_nav.py** - 原始简化版本 (单一导航功能)
- **voice_nav_mcp.py** - MCP 架构版本 (支持多种工具,可扩展) ⭐ 推荐

## 🚀 快速开始

### 基础版本 (voice_nav.py)

1. 安装依赖:
   ```bash
   pip install -r requirements.txt
   ```

2. 配置 API Key:
   ```bash
   cp .env.example .env
   # 编辑 .env 填入你的 API Key、BASE_URL 和 MODEL
   # 支持 OpenAI、DeepSeek 等任意兼容 OpenAI 接口的服务
   ```

3. 运行:
   ```bash
   python voice_nav.py
   ```

4. 使用:
   - 对着麦克风说导航指令
   - 例如: "从上海到北京"
   - 说"退出"结束程序

### MCP 版本 (推荐使用) ⭐

#### 方式一: 简化版 (无需额外依赖)

1. 完成基础设置

2. 测试 MCP 功能:
   ```bash
   python mcp_client_simple.py
   ```

3. 运行简化版语音助手:
   ```bash
   python voice_nav_mcp_simple.py
   ```

#### 方式二: 完整 MCP 协议版 (需要安装 mcp 库)

1. 安装 MCP 库:
   ```bash
   pip install "mcp>=1.0.0"
   ```

2. 测试 MCP 功能:
   ```bash
   python demo_mcp.py
   ```
   
   📖 **详细使用说明**: 查看 [DEMO_MCP_USAGE.md](./DEMO_MCP_USAGE.md) 了解 `demo_mcp.py` 的完整使用指南

3. 运行 MCP 版语音助手:
   ```bash
   python voice_nav_mcp.py
   ```

#### 使用示例:
- 支持导航: "从上海到北京"
- 支持天气: "查看明天上海的天气"
- 支持音乐: "播放周杰伦的晴天"
- 说"退出"结束程序

## 系统要求

- Python 3.8+
- 麦克风
- 联网
- macOS/Linux/Windows

## 已知问题

- 需要第三方大模型 API (有成本)
- 语音识别需要网络
- 没有唤醒词
- 只能导航,不支持其他功能

## 功能清单

### 基础版本 (voice_nav.py)
- ✅ 语音输入 (使用 Google 语音识别)
- ✅ AI 理解 (使用 ChatGPT 或兼容的第三方 API)
- ✅ 地图导航 (打开百度地图)
- ✅ 命令行交互
- ✅ 基本错误处理

### MCP 版本 ⭐
- ✅ **MCP 架构集成** - 可扩展的工具系统
- ✅ **导航工具** - 地图导航、地点搜索 (2个工具)
- ✅ **天气工具** - 天气查询、天气对比 (2个工具)
- ✅ **音乐工具** - 音乐播放、歌单搜索 (2个工具)
- ✅ **插件化设计** - 轻松添加新功能
- ✅ **统一接口** - 标准化的工具调用
- ✅ **简化实现** - 提供无需外部依赖的版本

## Demo 场景

```
$ python voice_nav.py
==================================================
🤖 WALL-E 语音导航原型
说话即可导航,说'退出'结束
==================================================

🎤 请说话...
📝 识别: 从上海七牛云到虹桥机场
🤖 AI: {'action': 'nav', 'from': '上海七牛云', 'to': '虹桥机场'}
🗺️  已打开: 上海七牛云 → 虹桥机场

🎤 请说话...
📝 识别: 退出
👋 再见!
```

## 配置说明

支持任意兼容 OpenAI API 格式的第三方大模型服务:

- `BASE_URL`: 第三方 API 接口地址
  - OpenAI: `https://api.openai.com/v1`
  - DeepSeek: `https://api.deepseek.com/v1`
  - 其他兼容服务的对应地址
- `API_KEY`: 对应的 API 密钥
- `MODEL`: 使用的模型名称 (如: `gpt-3.5-turbo`, `deepseek-chat`, 等)
- `LOG_LEVEL`: 日志级别 (可选,默认为 `INFO`)
  - `DEBUG`: 详细的调试信息,包括所有函数调用和参数
  - `INFO`: 关键操作信息,如程序启动、工具调用等 (推荐)
  - `WARNING`: 警告信息,如识别失败、超时等
  - `ERROR`: 错误信息,如异常和失败
  - `CRITICAL`: 严重错误

### 日志配置示例

在 `.env` 文件中添加:
```bash
# API 配置
API_KEY=your_api_key_here
BASE_URL=https://api.openai.com/v1
MODEL=gpt-3.5-turbo

# 日志级别 (可选,默认 INFO)
LOG_LEVEL=INFO
```

### 日志输出示例

```
2025-10-26 13:00:00 - WALL-E.VoiceNav - INFO - WALL-E 语音助手启动
2025-10-26 13:00:01 - WALL-E.MCPClient - INFO - 创建 MCP 客户端...
2025-10-26 13:00:01 - WALL-E.MCPClient - INFO - 成功注册 MCP Server: navigation
2025-10-26 13:00:01 - WALL-E.MCPClient - INFO - 成功注册 MCP Server: weather
2025-10-26 13:00:01 - WALL-E.MCPClient - INFO - 成功注册 MCP Server: music
2025-10-26 13:00:02 - WALL-E.VoiceNav - INFO - 已加载 6 个 MCP 工具
2025-10-26 13:00:02 - WALL-E.VoiceNav - INFO - 进入主循环,等待用户输入...
2025-10-26 13:00:03 - WALL-E.VoiceNav - INFO - 开始监听语音输入...
2025-10-26 13:00:05 - WALL-E.VoiceNav - INFO - 语音识别成功: 从上海到北京
2025-10-26 13:00:05 - WALL-E.VoiceNav - INFO - 开始 AI 理解用户输入: 从上海到北京
2025-10-26 13:00:06 - WALL-E.VoiceNav - INFO - AI 理解结果: tool=navigate, params={'origin': '上海', 'destination': '北京'}
2025-10-26 13:00:06 - WALL-E.VoiceNav - INFO - 执行 MCP 工具: navigate, 参数: {'origin': '上海', 'destination': '北京'}
2025-10-26 13:00:06 - WALL-E.VoiceNav - INFO - 工具执行成功: 已打开百度地图: 上海 → 北京
```

使用 DEBUG 级别可以看到更详细的信息:
```bash
LOG_LEVEL=DEBUG python voice_nav_mcp.py
```

## 📖 更多文档

- **[DEMO_MCP_USAGE.md](./DEMO_MCP_USAGE.md)** - demo_mcp.py 详细使用说明 ⭐ 新手必读
- **[README_MCP.md](./README_MCP.md)** - MCP 架构详细文档
- **[README_TESTS.md](./README_TESTS.md)** - 测试说明文档
- **[../PRD.md](../PRD.md)** - 完整产品需求文档
- **[../docs/架构设计文档.md](../docs/架构设计文档.md)** - 技术架构设计
- **[../docs/1天快速原型计划.md](../docs/1天快速原型计划.md)** - 原型开发计划
