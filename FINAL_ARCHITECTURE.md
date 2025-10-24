# 完整架构设计文档

## 🎯 项目架构

### 整体流程

```
┌─────────────────────────────────────────────────────────────┐
│                     Web 前端页面                             │
│  ┌──────────────────┐         ┌──────────────────┐         │
│  │   文字输入框      │         │   语音录音按钮    │         │
│  │ "从北京到上海"    │         │   🎤 点击录音     │         │
│  └────────┬─────────┘         └────────┬─────────┘         │
│           │                            │                    │
│           └────────────┬───────────────┘                    │
│                        ↓                                    │
│              POST /api/navigate                             │
│              { type, input/audio }                          │
└────────────────────────┼───────────────────────────────────┘
                         ↓ HTTP
┌─────────────────────────────────────────────────────────────┐
│                  Go Web 后端服务                             │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ 1️⃣ HTTP Handler - 接收请求                           │  │
│  │    - 文字输入 or 语音数据                              │  │
│  └────────────────────┬─────────────────────────────────┘  │
│                       ↓                                     │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ 2️⃣ STT 模块（自动降级）                               │  │
│  │  ┌─────────────────────────────────────────────┐     │  │
│  │  │ OpenAI Whisper API (优先)                   │     │  │
│  │  │  ✅ 高精度、支持中文                          │     │  │
│  │  └──────────────┬──────────────────────────────┘     │  │
│  │                 │ 失败 ↓                              │  │
│  │  ┌──────────────────────────────────────────────┐    │  │
│  │  │ 本地 STT（降级方案）                         │    │  │
│  │  │  • whisper.cpp                              │    │  │
│  │  │  • vosk                                      │    │  │
│  │  │  • 简单降级（提示用户）                       │    │  │
│  │  └──────────────────────────────────────────────┘    │  │
│  │                                                        │  │
│  │  结果: "从北京到上海"                                 │  │
│  └────────────────────┬───────────────────────────────── │  │
│                       ↓                                     │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ 3️⃣ AI 处理模块（多模型支持）                          │  │
│  │  ┌────────────────────────────────────────┐          │  │
│  │  │ 统一接口: ExtractNavigationIntent      │          │  │
│  │  └────────┬───────────────────────────────┘          │  │
│  │           │                                            │  │
│  │           ├─→ ChatGPT (OpenAI)                        │  │
│  │           │    - gpt-3.5-turbo                         │  │
│  │           │    - gpt-4                                 │  │
│  │           │                                            │  │
│  │           ├─→ Claude (Anthropic)                      │  │
│  │           │    - claude-3-5-sonnet                     │  │
│  │           │    - claude-3-opus                         │  │
│  │           │                                            │  │
│  │           └─→ DeepSeek                                │  │
│  │                - deepseek-chat                         │  │
│  │                                                        │  │
│  │  结果: { start: "北京", end: "上海" }                 │  │
│  └────────────────────┬───────────────────────────────────│  │
│                       ↓                                     │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ 4️⃣ MCP 工具模块                                       │  │
│  │    - GenerateBaiduMapURL()                            │  │
│  │    - GenerateAmapURL()                                │  │
│  │    - GenerateGoogleMapsURL()                          │  │
│  │                                                        │  │
│  │  结果: "http://api.map.baidu.com/direction?..."      │  │
│  └────────────────────┬───────────────────────────────────│  │
│                       ↓                                     │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ 5️⃣ 返回响应                                           │  │
│  │    { success: true, url: "...", start, end }          │  │
│  └────────────────────┬───────────────────────────────────│  │
└─────────────────────────┼────────────────────────────────────┘
                          ↓ HTTP Response
┌─────────────────────────────────────────────────────────────┐
│                     Web 前端页面                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ 6️⃣ 接收 URL 并跳转                                    │  │
│  │    window.location.href = response.url                │  │
│  │    或                                                  │  │
│  │    iframe.src = response.url                          │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                              │
│  地图显示：百度地图/高德地图从 A 到 B 的导航                │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 新的项目结构

```
qwall2/
├── main.go                          # HTTP 服务器入口 🆕
├── go.mod
├── go.sum
├── config.yaml                      # 配置文件 🆕
│
├── web/                             # Web 前端 🆕
│   ├── index.html                  # 主页面
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── app.js              # 前端逻辑
│   └── assets/
│       └── images/
│
├── internal/                        # 内部包 🆕
│   │
│   ├── server/                     # HTTP 服务器 🆕
│   │   ├── server.go              # 服务器初始化
│   │   ├── handlers.go            # HTTP 处理函数
│   │   └── middleware.go          # 中间件（CORS, 日志等）
│   │
│   ├── stt/                        # 语音转文字 🆕
│   │   ├── stt.go                 # STT 接口定义
│   │   ├── openai.go              # OpenAI Whisper
│   │   ├── local.go               # 本地 STT（降级）
│   │   └── stt_test.go            # 测试
│   │
│   ├── ai/                         # AI 处理模块 🆕
│   │   ├── ai.go                  # AI 接口定义
│   │   ├── chatgpt.go             # ChatGPT 实现
│   │   ├── claude.go              # Claude 实现
│   │   ├── deepseek.go            # DeepSeek 实现
│   │   └── ai_test.go             # 测试
│   │
│   └── config/                     # 配置管理 🆕
│       ├── config.go              # 配置加载
│       └── config_test.go
│
└── pkg/                            # 公共包（保留）
    ├── mapprovider/               # 地图提供商
    │   ├── provider.go           # URL 生成
    │   └── provider_test.go
    │
    └── parser/                    # 自然语言解析（保留作为备用）
        ├── parser.go
        └── parser_test.go
```

---

## 🔧 模块详细设计

### 1. STT 模块 - 自动降级机制

```go
// internal/stt/stt.go

type Client interface {
    TranscribeAudio(ctx context.Context, audio io.Reader, format string) (*Result, error)
}

// 使用方式
sttClient := stt.NewClient(stt.Config{
    Provider: stt.ProviderAuto,  // 自动降级
    OpenAIKey: "sk-xxx",
    EnableFallback: true,         // 启用降级
})

result, err := sttClient.TranscribeAudio(ctx, audioReader, "webm")
// 优先使用 OpenAI Whisper
// 失败后自动降级到本地 STT
```

**降级策略：**
1. **优先**：OpenAI Whisper API（高精度）
2. **降级1**：whisper.cpp（本地，需安装）
3. **降级2**：vosk（本地，需安装）
4. **最终**：返回提示用户使用文字输入

### 2. AI 处理模块 - 多模型支持

```go
// internal/ai/ai.go

type Client interface {
    ExtractNavigationIntent(ctx context.Context, text string) (*NavigationIntent, error)
}

// 使用方式 - ChatGPT
aiClient := ai.NewClient(ai.Config{
    Provider: ai.ProviderChatGPT,
    APIKey: "sk-xxx",
    Model: "gpt-3.5-turbo",
})

// 使用方式 - Claude
aiClient := ai.NewClient(ai.Config{
    Provider: ai.ProviderClaude,
    APIKey: "sk-ant-xxx",
    Model: "claude-3-5-sonnet-20241022",
})

// 使用方式 - DeepSeek
aiClient := ai.NewClient(ai.Config{
    Provider: ai.ProviderDeepSeek,
    APIKey: "sk-xxx",
    Model: "deepseek-chat",
})

intent, err := aiClient.ExtractNavigationIntent(ctx, "从北京到上海")
// 返回: { Start: "北京", End: "上海" }
```

**支持的模型：**

| 提供商 | 模型 | 特点 |
|--------|------|------|
| ChatGPT | gpt-3.5-turbo | 快速、便宜 |
| ChatGPT | gpt-4 | 高精度 |
| Claude | claude-3-5-sonnet | 平衡 |
| Claude | claude-3-opus | 最强 |
| DeepSeek | deepseek-chat | 国产、便宜 |

### 3. HTTP API 设计

#### POST /api/navigate

**文字请求：**
```json
{
  "type": "text",
  "input": "从北京到上海",
  "ai_provider": "chatgpt",     // 可选: chatgpt, claude, deepseek
  "map_provider": "baidu"       // 可选: baidu, amap, google
}
```

**语音请求：**
```json
{
  "type": "audio",
  "audio": "data:audio/webm;base64,GkXfo...",
  "format": "webm",              // 音频格式
  "ai_provider": "claude",
  "map_provider": "amap"
}
```

**成功响应：**
```json
{
  "success": true,
  "url": "http://api.map.baidu.com/direction?...",
  "start": "北京",
  "end": "上海",
  "recognized_text": "从北京到上海",  // 如果是语音
  "stt_provider": "openai",          // 使用的 STT
  "ai_provider": "chatgpt",          // 使用的 AI
  "map_provider": "baidu"
}
```

**失败响应：**
```json
{
  "success": false,
  "error": "无法识别起点和终点",
  "error_type": "extraction_failed",
  "details": {
    "recognized_text": "今天天气真好",
    "stt_provider": "openai"
  }
}
```

---

## ⚙️ 配置文件

```yaml
# config.yaml

server:
  port: 8080
  host: "0.0.0.0"

# STT 配置
stt:
  provider: "auto"              # auto, openai, local
  openai_key: "${OPENAI_API_KEY}"
  model: "whisper-1"
  enable_fallback: true         # 启用降级
  local_model_path: "/usr/local/share/whisper/models"

# AI 配置
ai:
  default_provider: "chatgpt"   # chatgpt, claude, deepseek
  
  chatgpt:
    api_key: "${OPENAI_API_KEY}"
    model: "gpt-3.5-turbo"
    base_url: "https://api.openai.com/v1"
  
  claude:
    api_key: "${ANTHROPIC_API_KEY}"
    model: "claude-3-5-sonnet-20241022"
    base_url: "https://api.anthropic.com/v1"
  
  deepseek:
    api_key: "${DEEPSEEK_API_KEY}"
    model: "deepseek-chat"
    base_url: "https://api.deepseek.com/v1"

# 地图配置
map:
  default_provider: "baidu"     # baidu, amap, google
```

---

## 🚀 实现计划

### 阶段 1: 基础功能 ✅
- [x] STT 模块（OpenAI + 本地降级）
- [x] AI 模块（ChatGPT, Claude, DeepSeek）
- [ ] HTTP 服务器
- [ ] 简单 Web 页面
- [ ] 配置管理

### 阶段 2: 完整功能
- [ ] 语音录制前端
- [ ] 错误处理和重试
- [ ] 日志记录
- [ ] 单元测试

### 阶段 3: 优化
- [ ] UI/UX 改进
- [ ] 性能优化
- [ ] Docker 部署
- [ ] 文档完善

---

## 💡 使用示例

### 启动服务

```bash
# 设置环境变量
export OPENAI_API_KEY="sk-xxx"
export ANTHROPIC_API_KEY="sk-ant-xxx"

# 启动服务器
go run main.go

# 或使用配置文件
go run main.go -config config.yaml
```

### 访问 Web 页面

```
http://localhost:8080
```

### API 调用示例

```bash
# 文字输入
curl -X POST http://localhost:8080/api/navigate \
  -H "Content-Type: application/json" \
  -d '{
    "type": "text",
    "input": "从北京到上海",
    "ai_provider": "chatgpt"
  }'

# 返回
{
  "success": true,
  "url": "http://api.map.baidu.com/direction?...",
  "start": "北京",
  "end": "上海"
}
```

---

**下一步：开始实现 HTTP 服务器和 Web 前端？** 🤔
