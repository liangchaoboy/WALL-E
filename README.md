# 🗺️ QWall2 - AI 地图导航系统

> 基于 Chrome 语音识别和 AI 的智能地图导航助手

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Go Version](https://img.shields.io/badge/Go-1.21+-blue.svg)](https://golang.org/)
[![Chrome Support](https://img.shields.io/badge/Chrome-Supported-green.svg)](https://www.google.com/chrome/)

## ✨ 核心功能

- 🎤 **Chrome 语音识别** - 无需 API 密钥，使用浏览器原生功能
- 🤖 **多 AI 支持** - Claude、ChatGPT、DeepSeek、Mock 模式
- 🗺️ **多地图支持** - 百度地图、高德地图、Google Maps
- 🌐 **现代化 Web 界面** - 响应式设计，支持移动端
- ⚡ **智能降级** - 自动选择可用的 AI 服务

## 🚀 快速开始

### 1. 启动服务

```bash
git clone <repository-url>
cd qwall2
./start.sh
```

### 2. 访问应用

打开浏览器访问：`http://localhost:8090`

### 3. 语音导航

1. 点击 **"🎤 语音输入"** 标签
2. 点击 **"点击开始识别"** 按钮
3. 说出导航需求："从北京到上海"
4. 点击 **"🚀 开始导航"** 按钮

## 🎯 使用示例

### 语音导航

| 语音输入 | 导航结果 |
|---------|---------|
| "从北京到上海" | 北京 → 上海 |
| "去杭州西湖" | 当前位置 → 杭州西湖 |
| "用高德地图从广州到深圳" | 广州 → 深圳 (高德地图) |

### 支持的地图

- **百度地图** 🇨🇳 - 国内导航首选
- **高德地图** 🇨🇳 - 高精度导航  
- **Google Maps** 🌍 - 国际导航

## ⚙️ 配置

### 环境变量（可选）

```bash
# Claude AI (推荐)
export ANTHROPIC_API_KEY="your-claude-api-key"

# ChatGPT
export OPENAI_API_KEY="your-openai-api-key"

# DeepSeek  
export DEEPSEEK_API_KEY="your-deepseek-api-key"
```

### 配置文件

编辑 `config.yaml`：

```yaml
ai:
  default_provider: "mock"  # mock, claude, chatgpt, deepseek

map:
  default_provider: "baidu"  # baidu, amap, google
```

## 🏗️ 技术架构

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Chrome 浏览器   │    │   Go Web 服务器   │    │   AI 服务       │
│                 │    │                 │    │                 │
│ • Web Speech API │◄──►│ • HTTP API      │◄──►│ • Claude        │
│ • 语音识别        │    │ • 路由处理        │    │ • ChatGPT       │
│ • 用户界面        │    │ • 配置管理        │    │ • DeepSeek      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   地图服务       │
                       │                 │
                       │ • 百度地图       │
                       │ • 高德地图       │
                       │ • Google Maps   │
                       └─────────────────┘
```

## 📁 项目结构

```
qwall2/
├── docs/                    # 📚 文档
│   ├── QUICKSTART.md       # 快速入门
│   ├── ARCHITECTURE.md     # 系统架构
│   ├── DEMO.md             # 功能演示
│   ├── STATUS.md           # 项目状态
│   └── THIRD_PARTY_API.md  # API 配置
├── internal/               # 🔧 核心模块
│   ├── ai/                 # AI 处理
│   ├── server/             # HTTP 服务器
│   ├── config/             # 配置管理
│   └── stt/                # 语音识别
├── web/                    # 🌐 Web 前端
│   ├── index.html
│   └── static/
├── pkg/                    # 📦 公共包
│   ├── mapprovider/        # 地图提供商
│   ├── navigation/         # 导航逻辑
│   └── parser/             # 文本解析
├── config.yaml             # ⚙️ 配置文件
├── start.sh                # 🚀 启动脚本
├── Makefile                # 🔨 构建工具
└── README.md               # 📖 项目说明
```

## 🔧 开发

### 构建

```bash
make build
```

### 测试

```bash
make test
```

### 运行

```bash
make run
```

## 📚 文档

- [快速入门](docs/QUICKSTART.md) - 5分钟快速上手
- [系统架构](docs/ARCHITECTURE.md) - 技术架构详解
- [功能演示](docs/DEMO.md) - 完整功能展示
- [API 配置](docs/THIRD_PARTY_API.md) - 第三方 API 设置
- [项目状态](docs/STATUS.md) - 开发进度和计划

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- Chrome Web Speech API
- Claude AI
- 百度地图、高德地图、Google Maps
- Go 语言社区

---

**⭐ 如果这个项目对你有帮助，请给它一个 Star！**