# WALL-E Advanced - macOS 桌面语音助手

> 基于 Swift + Go + MCP 架构的 AI 驱动桌面操作系统代理

## 📋 项目概述

WALL-E Advanced 是 WALL-E 项目的第二阶段,在原型验证的基础上,构建完整的 macOS 原生桌面语音助手应用。

**核心特性**:
- 🎤 语音唤醒("小七小七") + 语音识别
- ⌨️ 文字输入界面(系统托盘 + 全局快捷键)
- 🤖 AI 智能理解(支持 ChatGPT/Claude/DeepSeek)
- 🔌 可扩展的 MCP 工具系统
- 🚀 原生性能,低内存占用

## 🏗️ 项目结构

```
walle-advanced/
├── macos-app/          # Swift macOS 应用
│   └── WALLE/
│       ├── App/        # 应用入口
│       ├── UI/         # SwiftUI 界面
│       └── Services/   # 服务层(语音输入、音频采集等)
├── core-service/       # Go 核心服务
│   ├── cmd/            # 主程序入口
│   ├── internal/       # 内部模块(STT、AI、MCP)
│   └── proto/          # gRPC 协议定义
├── mcp-tools/          # MCP 工具集
│   ├── map-navigation/     # 地图导航
│   ├── weather-query/      # 天气查询
│   ├── music-player/       # 音乐播放
│   ├── browser-control/    # 浏览器控制
│   ├── system-control/     # 系统控制
│   └── app-launcher/       # 应用启动
├── tests/              # 测试
└── docs/               # 文档
```

## 🛠️ 技术栈

| 模块 | 技术选择 |
|------|---------|
| macOS 应用 | Swift + SwiftUI |
| 核心服务 | Go 1.21+ + gRPC |
| MCP 工具 | TypeScript/Python/Go |
| 唤醒词 | Porcupine |
| STT | 阿里云/OpenAI Whisper |
| AI | ChatGPT/Claude/DeepSeek |
| 浏览器控制 | Playwright |

## 🚀 快速开始

### 环境要求

- macOS 13.0+
- Xcode 15.0+
- Go 1.21+
- Node.js 18+
- Python 3.8+

### 安装依赖

```bash
# 安装 Go 依赖
cd core-service
go mod download

# 安装 Node.js 依赖(各 MCP 工具)
cd ../mcp-tools/map-navigation
npm install

# 安装 Python 依赖
cd ../weather-query
pip install -r requirements.txt
```

### 运行

```bash
# 1. 启动 Go 核心服务
cd core-service
go run cmd/walle-core/main.go

# 2. 在 Xcode 中打开并运行 macOS 应用
open macos-app/WALLE.xcodeproj
```

## 📅 开发计划

详见 [Issue #48](https://github.com/liangchaoboy/WALL-E/issues/48) 中的完整实施计划。

### 阶段划分

| 阶段 | 时间 | 目标 |
|------|------|------|
| **阶段一: MVP** | 2-3周 | 地图导航功能验证 |
| **阶段二: 功能扩展** | 2-3周 | 天气、音乐等工具 |
| **阶段三: 高级能力** | 2-3周 | 浏览器/系统控制 |
| **阶段四: 优化发布** | 1-2周 | 性能优化、发布 |

## 🎯 当前状态

**阶段**: 准备阶段  
**下一步**: 启动阶段一 MVP 开发

### 任务组状态

#### 阶段一 (准备中)
- [ ] 任务组 A: macOS 应用框架
- [ ] 任务组 B: 语音输入模块
- [ ] 任务组 C: Go 核心服务
- [ ] 任务组 D: AI 理解引擎
- [ ] 任务组 E: MCP 客户端
- [ ] 任务组 F: 地图导航工具

## 📖 文档

- [PRD - 产品需求文档](../PRD.md)
- [架构设计文档](../docs/架构设计文档.md)
- [任务拆解与实施计划](../docs/任务拆解与实施计划.md)
- [Phase 2 详细计划](https://github.com/liangchaoboy/WALL-E/issues/48)

## 🤝 贡献

欢迎贡献代码、报告问题、提出建议!

### 团队分工

1. **macOS 开发工程师**: Swift 应用 + UI
2. **后端开发工程师**: Go 核心服务 + gRPC  
3. **MCP 工具开发工程师**: MCP Server 开发

## 📝 许可证

待定

---

**让 AI 成为你的桌面助手!** ✨
