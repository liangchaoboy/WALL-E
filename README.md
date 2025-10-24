# 🚀 qwall2 - AI 智能地图导航系统

> 基于 Go + AI 的智能地图导航系统，支持文字和语音输入，自动解析并打开地图导航。

[![Go Version](https://img.shields.io/badge/Go-1.23.0-blue.svg)](https://golang.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production-success.svg)](STATUS.md)

## ✨ 核心特性

### 🎯 智能交互
- 🎤 **双模输入**：文字输入 + 语音录制
- 🤖 **多 AI 引擎**：ChatGPT、Claude、DeepSeek 自由切换
- 🧠 **智能解析**：自动提取起点和终点，无需固定格式

### 🔧 技术优势
- 🗣️ **智能 STT**：OpenAI Whisper 优先，失败自动降级到本地
- 🗺️ **多地图支持**：百度、高德、Google Maps
- 🌐 **独立部署**：Web 界面 + Go 后端，无需第三方依赖
- 📦 **开箱即用**：一键启动，配置简单

## 🏗️ 系统架构

```
┌─────────────────────────────────────┐
│      Web 前端 (浏览器)               │
│   文字输入  |  语音录制               │
└──────────────┬──────────────────────┘
               ↓ HTTP POST /api/navigate
┌──────────────────────────────────────┐
│     Go HTTP 服务器 (:8080)            │
└──────────────┬───────────────────────┘
               ↓
    ┌──────────┴──────────┐
    ↓                     ↓
┌─────────┐         ┌──────────┐
│ STT 模块 │         │ AI 模块   │
│ (语音)   │         │ (意图提取) │
└─────────┘         └──────────┘
    ↓                     ↓
Whisper API        ChatGPT/Claude
    ↓                     ↓
本地降级           DeepSeek
    └──────────┬──────────┘
               ↓
         地图 URL 生成
      (百度/高德/Google)
               ↓
         返回前端 → 跳转
```

## 🚀 快速开始

### 前置要求

- Go 1.23.0+
- OpenAI API Key（必需）

### 三步启动

**1️⃣ 配置 API Key**
```bash
export OPENAI_API_KEY="sk-your-openai-key"

# 可选：使用第三方兼容 API（国内代理、OneAPI 等）
export OPENAI_BASE_URL="https://your-proxy.com/v1"
```

**2️⃣ 启动服务**
```bash
./start.sh
```

**3️⃣ 访问界面**

打开浏览器：**http://localhost:8080**

> 💡 详细说明请查看 [QUICKSTART.md](QUICKSTART.md)

## ⚙️ 配置

编辑 `config.yaml`：

```yaml
server:
  port: 8080                    # 服务端口

stt:
  provider: "auto"              # STT 提供商
  enable_fallback: true         # 启用降级

ai:
  default_provider: "chatgpt"   # 默认 AI
  chatgpt:
    model: "gpt-3.5-turbo"      # ChatGPT 模型
    base_url: "..."             # 可自定义第三方 API

map:
  default_provider: "baidu"     # 默认地图
```

**🌐 支持第三方 API**：
- 国内 API 代理服务
- OneAPI 聚合服务
- 私有部署的模型服务
- 任何 OpenAI 兼容的 API

> 📝 完整配置说明请查看 [config.yaml](config.yaml)

## 📖 使用示例

### 文字输入

```
输入："从北京去上海"
结果：起点=北京，终点=上海 → 打开地图

输入："去天安门"
结果：起点=当前位置，终点=天安门 → 打开地图
```

### 语音输入

```
1. 点击"开始录音"
2. 说出："从西湖到灵隐寺"
3. 点击"停止录音"
4. 自动识别并导航
```

## 🔌 API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/navigate` | POST | 导航请求 |
| `/api/health` | GET | 健康检查 |

**导航请求示例**：
```bash
curl -X POST http://localhost:8080/api/navigate \
  -H "Content-Type: application/json" \
  -d '{
    "type": "text",
    "input": "从北京去上海",
    "ai_provider": "chatgpt",
    "map_provider": "baidu"
  }'
```

> 📚 完整 API 文档请查看 [ARCHITECTURE.md](ARCHITECTURE.md)

## 🌟 核心优势

### 智能降级机制

```
OpenAI Whisper API (优先)
    ↓ 失败
whisper.cpp (本地)
    ↓ 失败
vosk (轻量级)
    ↓ 失败
友好提示
```

### 多 AI 引擎

| AI 模型 | 特点 | 推荐场景 |
|---------|------|----------|
| ChatGPT | 快速经济 | 日常使用 |
| Claude | 智能准确 | 复杂场景 |
| DeepSeek | 中文优化 | 国内用户 |

### 自然语言理解

- ✅ 自动提取起点终点
- ✅ 支持口语化表达
- ✅ 智能默认当前位置

## 📁 项目结构

```
qwall2/
├── internal/              # 核心模块
│   ├── ai/               # AI 处理（ChatGPT/Claude/DeepSeek）
│   ├── stt/              # STT（Whisper + 本地降级）
│   ├── server/           # HTTP 服务器
│   └── config/           # 配置管理
├── pkg/
│   └── mapprovider/      # 地图服务（百度/高德/Google）
├── web/                  # Web 前端
│   ├── index.html
│   └── static/
├── main.go               # 程序入口
└── config.yaml           # 配置文件
```

## 🧪 测试

运行自动化测试：

```bash
./test.sh
```

测试覆盖：
- ✅ 服务器运行
- ✅ API 端点
- ✅ 静态文件
- ✅ 健康检查

## 🐛 故障排查

| 问题 | 解决方案 |
|------|----------|
| API Key 无效 | 检查并重新设置 `OPENAI_API_KEY` |
| 端口被占用 | 修改 `config.yaml` 中的端口号 |
| 语音识别失败 | 确认 API Key 和浏览器权限 |

> 💡 更多帮助请查看 [QUICKSTART.md](QUICKSTART.md)

## 📚 文档

- [QUICKSTART.md](QUICKSTART.md) - 快速开始指南
- [ARCHITECTURE.md](ARCHITECTURE.md) - 系统架构详解
- [DEMO.md](DEMO.md) - 演示和测试用例
- [STATUS.md](STATUS.md) - 项目状态报告

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

---

**快速开始**: `export OPENAI_API_KEY="sk-..." && ./start.sh`  
**访问地址**: http://localhost:8080
