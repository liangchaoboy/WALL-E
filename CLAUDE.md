# CLAUDE.md - WALL-E 项目说明

## 项目概述

WALL-E 是一个 AI 驱动的桌面操作系统代理,让用户通过自然语言(文字/语音)与计算机交互,实现各类日常操作的自动化。项目基于 MCP (Model Context Protocol) 协议构建,具备高度可扩展性。

## 核心价值

- **降低操作门槛**: 老人、儿童等不熟悉电脑的用户也能轻松使用
- **提升效率**: 通过语音快速完成多步骤操作
- **智能理解**: 自然语言交互,无需记忆命令
- **可扩展性**: 基于 MCP 插件化架构,持续增强能力

## 项目架构

### 整体架构分层

```
用户交互层 (语音/文字输入)
    ↓
核心处理层 (STT → AI理解 → MCP Client)
    ↓
MCP工具层 (地图/天气/音乐/浏览器/系统控制)
    ↓
系统能力层 (macOS API / 第三方服务)
```

### 技术栈

**当前原型阶段**:
- **语言**: Python 3.8+
- **语音识别**: Google Speech Recognition
- **AI 引擎**: OpenAI API (支持 ChatGPT, DeepSeek 等兼容服务)
- **工具协议**: MCP (Model Context Protocol)
- **音频处理**: SpeechRecognition, PyAudio

**规划中的完整版本**:
- **客户端**: Swift + SwiftUI (macOS 原生)
- **后端服务**: Go
- **AI 引擎**: ChatGPT / Claude / DeepSeek
- **语音识别**: 阿里云 / OpenAI Whisper / 本地模型
- **唤醒词检测**: Porcupine (本地检测)

## 项目结构

```
WALL-E/
├── README.md                          # 项目主文档
├── PRD.md                            # 完整产品需求文档
├── CLAUDE.md                         # 本文件 - Claude AI 项目说明
├── docs/                             # 设计文档
│   ├── 架构设计文档.md                # 详细技术架构
│   ├── 任务拆解与实施计划.md          # 实施计划
│   └── 1天快速原型计划.md             # 原型开发计划
└── walle-prototype/                  # 原型实现
    ├── README.md                     # 原型说明文档
    ├── requirements.txt              # Python 依赖
    ├── voice_nav.py                  # 基础版语音导航
    ├── voice_nav_mcp.py              # MCP 架构版语音助手
    ├── voice_nav_mcp_simple.py       # 简化版 MCP 语音助手
    ├── demo_mcp.py                   # MCP 功能演示脚本
    ├── mcp_client.py                 # MCP 客户端实现
    ├── mcp_client_simple.py          # 简化版 MCP 客户端
    ├── mcp_servers/                  # 完整 MCP Server 实现
    │   ├── navigation_server.py      # 地图导航服务
    │   ├── weather_server.py         # 天气查询服务
    │   └── music_server.py           # 音乐播放服务
    ├── mcp_servers_simple/           # 简化 MCP 工具实现
    │   ├── navigation_tools.py       # 导航工具
    │   ├── weather_tools.py          # 天气工具
    │   └── music_tools.py            # 音乐工具
    ├── test_*.py                     # 单元测试文件
    ├── README_MCP.md                 # MCP 架构详细文档
    ├── DEMO_MCP_USAGE.md             # MCP 演示使用说明
    └── README_TESTS.md               # 测试文档
```

## 核心功能模块

### 1. 语音输入系统
- 实时语音识别(基于 Google Speech Recognition)
- 规划支持唤醒词检测("小七小七")
- 语音活动检测(VAD) - 自动判断说话结束

### 2. 文字输入界面
- 命令行交互(原型阶段)
- 规划支持系统托盘 + 全局快捷键(Cmd+Space)
- 历史记录查看

### 3. AI 理解引擎
- 自然语言理解(NLU)
- 意图识别和参数提取
- 支持多种 LLM: ChatGPT, Claude, DeepSeek
- 基于 MCP 协议与工具通信

### 4. MCP 工具系统
- **地图导航工具**: 
  - `navigate(origin, destination)` - 路线导航
  - `search_location(query)` - 地点搜索
  
- **天气查询工具**:
  - `get_weather(city, date)` - 天气查询
  - `compare_weather(city1, city2)` - 天气对比
  
- **音乐播放工具**:
  - `play_music(song, artist)` - 播放音乐
  - `search_playlist(keyword)` - 搜索歌单

## 数据流

```
用户输入 (语音/文字)
    ↓
[语音识别/文本预处理] → 标准化文本
    ↓
[AI 理解] → 结构化意图 { tool, params }
    ↓
[MCP Client] → 工具选择和调用
    ↓
[MCP Server] → 工具执行
    ↓
[结果返回] → 用户反馈
```

## 开发指南

### 快速开始

1. **安装依赖**:
   ```bash
   cd walle-prototype
   pip install -r requirements.txt
   ```

2. **配置环境**:
   ```bash
   cp .env.example .env
   # 编辑 .env 文件,填入 API_KEY, BASE_URL, MODEL
   ```

3. **测试 MCP 功能**:
   ```bash
   python demo_mcp.py
   ```

4. **运行语音助手**:
   ```bash
   # 完整版 (需要 mcp 库)
   pip install "mcp>=1.0.0"
   python voice_nav_mcp.py
   
   # 简化版 (无需额外依赖)
   python voice_nav_mcp_simple.py
   ```

### 使用示例

```
用户: "从上海到北京"
AI理解: {'tool': 'navigate', 'params': {'origin': '上海', 'destination': '北京'}}
执行: 已打开百度地图: 上海 → 北京

用户: "查看明天上海的天气"
AI理解: {'tool': 'get_weather', 'params': {'city': '上海', 'date': '明天'}}
执行: 上海明天天气: 多云, 温度 15-22°C, 降雨概率 20%

用户: "播放周杰伦的晴天"
AI理解: {'tool': 'play_music', 'params': {'song': '晴天', 'artist': '周杰伦'}}
执行: 已在 QQ 音乐播放: 晴天 - 周杰伦
```

### 添加新的 MCP 工具

1. **创建工具文件**: 在 `mcp_servers/` 或 `mcp_servers_simple/` 创建新的 Python 文件

2. **定义工具函数**:
   ```python
   from mcp.server import Server
   
   mcp = Server("tool-name")
   
   @mcp.tool()
   def my_tool(param1: str, param2: str = "default"):
       """工具描述"""
       # 实现逻辑
       return "执行结果"
   ```

3. **注册到 MCP Client**: 在 `mcp_client.py` 的 `create_mcp_client()` 中添加配置

4. **测试工具**: 运行 `demo_mcp.py` 验证工具可用

## 测试

### 运行测试

```bash
cd walle-prototype

# 运行所有测试
pytest

# 运行特定测试
pytest test_demo_mcp.py
pytest test_voice_nav.py
pytest test_mcp_client.py

# 查看覆盖率
pytest --cov=. --cov-report=html
```

### 测试覆盖

- **test_demo_mcp.py**: MCP 客户端和工具调用测试
- **test_voice_nav.py**: 语音导航基础功能测试
- **test_mcp_client.py**: MCP 客户端单元测试

## 实施阶段

### 阶段一: MVP (已完成)
- ✅ 语音输入 + 语音识别
- ✅ AI 理解引擎 (基于 OpenAI API)
- ✅ MCP 架构集成
- ✅ 地图导航工具
- ✅ 命令行交互界面

### 阶段二: 功能扩展 (进行中)
- ✅ 天气查询工具
- ✅ 音乐播放工具
- ✅ MCP 多工具支持
- ✅ 示例代码和文档
- 🔄 多轮对话支持
- 🔄 历史记录功能

### 阶段三: 高级能力 (规划中)
- ⏳ 浏览器控制工具
- ⏳ 系统控制工具
- ⏳ 工具链编排 (多步骤操作)
- ⏳ 安全确认机制

### 阶段四: macOS 原生版 (规划中)
- ⏳ Swift + SwiftUI 客户端
- ⏳ Go 后端服务
- ⏳ 本地唤醒词检测
- ⏳ 应用打包和分发

## 配置说明

### 环境变量

```bash
# .env 文件配置
API_KEY=your_api_key_here          # LLM API 密钥
BASE_URL=https://api.openai.com/v1 # API 基础地址
MODEL=gpt-3.5-turbo                # 使用的模型
```

### 支持的 LLM 服务

- OpenAI (ChatGPT): `https://api.openai.com/v1`
- DeepSeek: `https://api.deepseek.com/v1`
- 其他兼容 OpenAI API 格式的服务

## 性能要求

| 指标 | 当前原型 | 目标值 (完整版) |
|------|---------|----------------|
| 语音识别延迟 | ~2-3s | < 2s |
| AI 理解延迟 | ~2-4s | < 3s |
| 工具执行延迟 | ~1s | < 1s |
| 内存占用 | ~100MB | < 200MB (空闲) |

## 安全与隐私

### 当前实现
- 语音数据不持久化存储
- 支持用户自带 API Key
- 本地工具执行,无云端数据传输

### 规划中
- macOS Keychain 存储敏感信息
- 危险操作二次确认
- 完整的权限管理系统
- 日志脱敏处理

## 已知限制

### 原型阶段限制
- 需要第三方 LLM API (有成本)
- 语音识别需要网络连接
- 没有唤醒词检测
- 命令行界面,无图形界面
- 工具模拟执行,不是真实系统操作

### 后续改进
- 支持本地 LLM 模型
- 离线语音识别
- 本地唤醒词检测
- macOS 原生 GUI
- 真实系统集成

## 贡献指南

### 参与方式

1. **查看 Issues**: 了解当前开发进展和待解决问题
2. **阅读文档**: 
   - [PRD.md](./PRD.md) - 产品需求
   - [docs/架构设计文档.md](./docs/架构设计文档.md) - 技术设计
3. **提交 PR**: 
   - Fork 项目
   - 创建功能分支
   - 提交代码和测试
   - 发起 Pull Request

### 开发规范

- **代码风格**: 遵循 PEP 8 (Python)
- **提交信息**: 使用清晰的提交信息
- **测试**: 为新功能添加测试
- **文档**: 更新相关文档

## 相关资源

### 文档
- [README.md](./README.md) - 项目总览
- [PRD.md](./PRD.md) - 产品需求文档
- [walle-prototype/README.md](./walle-prototype/README.md) - 原型说明
- [walle-prototype/README_MCP.md](./walle-prototype/README_MCP.md) - MCP 架构文档
- [walle-prototype/DEMO_MCP_USAGE.md](./walle-prototype/DEMO_MCP_USAGE.md) - MCP 演示说明
- [docs/架构设计文档.md](./docs/架构设计文档.md) - 详细架构设计

### 技术参考
- [MCP 官方文档](https://modelcontextprotocol.io/)
- [OpenAI API 文档](https://platform.openai.com/docs)
- [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)

## 联系方式

- **GitHub Issues**: [liangchaoboy/WALL-E/issues](https://github.com/liangchaoboy/WALL-E/issues)
- **项目主页**: [liangchaoboy/WALL-E](https://github.com/liangchaoboy/WALL-E)

## 许可证

待定

---

**让 AI 成为你的桌面助手,从此告别繁琐的电脑操作!** ✨
