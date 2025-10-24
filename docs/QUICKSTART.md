# 🚀 快速开始指南

## 系统简介

qwall2 是一个 AI 驱动的智能地图导航系统，支持文字和语音输入，自动解析用户意图并打开地图导航。

## 核心特性

- 🎤 **双模输入**：支持文字和语音输入
- 🤖 **多 AI 模型**：ChatGPT、Claude、DeepSeek
- 🗣️ **智能 STT**：OpenAI Whisper + 本地降级
- 🗺️ **多地图服务**：百度、高德、Google Maps
- 🌐 **独立部署**：Web 界面 + Go 后端

## 5 分钟快速开始

### 1. 配置 API Key

```bash
# 必需：OpenAI API Key（用于 ChatGPT 和 Whisper STT）
export OPENAI_API_KEY="sk-your-openai-key-here"

# 可选：其他 AI 模型
export ANTHROPIC_API_KEY="sk-ant-your-key-here"
export DEEPSEEK_API_KEY="sk-your-key-here"

# 可选：自定义 API 接口地址（支持第三方兼容服务）
# OpenAI 兼容接口（如：国内代理、私有部署、OneAPI 等）
export OPENAI_BASE_URL="https://your-proxy.com/v1"
export OPENAI_MODEL="gpt-3.5-turbo"  # 自定义模型名称

# Claude 兼容接口
export ANTHROPIC_BASE_URL="https://your-claude-proxy.com/v1"
export ANTHROPIC_MODEL="claude-3-5-sonnet-20241022"  # 自定义模型名称

# DeepSeek 兼容接口
export DEEPSEEK_BASE_URL="https://your-deepseek-proxy.com/v1"
export DEEPSEEK_MODEL="deepseek-chat"  # 自定义模型名称

# Whisper STT 模型
export WHISPER_MODEL="whisper-1"  # 自定义 Whisper 模型名称
```

### 2. 启动服务

```bash
# 方式 1：使用启动脚本（推荐）
./start.sh

# 方式 2：直接运行
./qwall2-server --config config.yaml
```

### 3. 访问界面

打开浏览器访问：**http://localhost:8080**

### 4. 开始使用

#### 文字导航
1. 在输入框输入：`从北京去上海`
2. 选择 AI 模型：ChatGPT
3. 选择地图：百度地图
4. 点击"开始导航"

#### 语音导航
1. 切换到"语音输入"选项卡
2. 点击"开始录音"
3. 说出：`去天安门`
4. 点击"停止录音"

## 系统架构

```
Web 前端 (浏览器)
    ↓ HTTP POST
Go 服务器 (:8080)
    ↓
┌────────────┬─────────────┐
STT 模块    AI 处理模块
(语音→文字)  (提取起点终点)
    ↓            ↓
OpenAI Whisper   ChatGPT
    ↓            Claude
本地降级      DeepSeek
    └────────────┘
          ↓
    地图 URL 生成
    (百度/高德/Google)
          ↓
    返回前端 → 跳转
```

## API 接口

### POST /api/navigate

**请求示例**：
```json
{
  "type": "text",
  "input": "从北京去上海",
  "ai_provider": "chatgpt",
  "map_provider": "baidu"
}
```

**响应示例**：
```json
{
  "success": true,
  "url": "https://map.baidu.com/...",
  "start": "北京",
  "end": "上海"
}
```

### GET /api/health

**响应示例**：
```json
{
  "status": "ok",
  "stt": "Auto (OpenAI → Local)",
  "ai": ["chatgpt", "claude"]
}
```

## 配置说明

编辑 `config.yaml`：

```yaml
server:
  port: 8080              # HTTP 端口
  host: "0.0.0.0"         # 监听地址

stt:
  provider: "auto"         # STT 提供商（auto/openai/local）
  enable_fallback: true    # 启用降级

ai:
  default_provider: "chatgpt"  # 默认 AI 模型
  chatgpt:
    model: "gpt-3.5-turbo"               # 模型名称（可通过环境变量覆盖）
    base_url: "https://api.openai.com/v1"  # API 地址（可自定义为第三方）
  claude:
    model: "claude-3-5-sonnet-20241022"     # 模型名称
    base_url: "https://api.anthropic.com/v1"  # API 地址
  deepseek:
    model: "deepseek-chat"                   # 模型名称
    base_url: "https://api.deepseek.com/v1"  # API 地址

map:
  default_provider: "baidu"    # 默认地图服务
```

**🔧 环境变量覆盖示例**：
```bash
# 环境变量会覆盖 config.yaml 中的配置
export OPENAI_MODEL="gpt-4"  # 使用 GPT-4 模型
export ANTHROPIC_MODEL="claude-3-opus-20240229"  # 使用 Claude Opus
```

**🌐 第三方 API 服务示例**：
- 🇨🇳 国内 API 代理：`https://api.openai-proxy.com/v1`
- 🔧 OneAPI 服务：`https://your-oneapi.com/v1`
- 🏢 私有部署：`https://your-private-llm.com/v1`
- 🌐 其他兼容服务：任何 OpenAI 兼容的 API

**🎯 常见模型名称**：
- OpenAI: `gpt-3.5-turbo`, `gpt-4`, `gpt-4-turbo`
- Claude: `claude-3-5-sonnet-20241022`, `claude-3-opus-20240229`
- DeepSeek: `deepseek-chat`, `deepseek-coder`
- 第三方服务：根据服务商提供的模型名称

## 测试验证

运行自动化测试：

```bash
./test.sh
```

测试内容：
- ✅ 服务器运行状态
- ✅ 健康检查 API
- ✅ 导航 API
- ✅ 主页访问
- ✅ 静态文件

## 故障排查

### 问题：API Key 无效

**症状**：导航失败，提示 "invalid_api_key"

**解决**：
```bash
# 检查环境变量
echo $OPENAI_API_KEY

# 重新设置
export OPENAI_API_KEY="sk-correct-key"

# 重启服务器
./start.sh
```

### 问题：服务器无法启动

**症状**：端口 8080 被占用

**解决**：
```bash
# 查看占用进程
lsof -i :8080

# 修改端口（在 config.yaml 中）
server:
  port: 8081
```

### 问题：语音识别失败

**症状**：录音后无反应

**解决**：
1. 检查 OPENAI_API_KEY 是否设置
2. 检查浏览器麦克风权限
3. 使用 HTTPS（生产环境）或 localhost（开发环境）

## 下一步

- 📖 查看 [ARCHITECTURE.md](ARCHITECTURE.md) 了解系统架构
- 🎬 查看 [DEMO.md](DEMO.md) 了解详细演示
- 📊 查看 [STATUS.md](STATUS.md) 了解项目状态

## 常见使用场景

### 场景 1：日常导航
```
输入："去附近的星巴克"
结果：自动提取 起点=当前位置，终点=星巴克
```

### 场景 2：规划路线
```
输入："从家到公司怎么走"
结果：自动提取 起点=家，终点=公司
```

### 场景 3：旅游规划
```
输入："从北京到上海"
结果：自动提取 起点=北京，终点=上海
```

## 技术支持

- 提交 Issue：[GitHub Issues](https://github.com/sanmu/qwall2/issues)
- 查看文档：[../README.md](../README.md)
- 运行测试：`./test.sh`

## 许可证

MIT License
