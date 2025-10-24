# 🏗️ qwall2 系统架构文档

## 系统概述

qwall2 是一个基于 MCP（Model Context Protocol）理念的 AI 地图导航系统，通过 Go 后端和 Web 前端实现智能导航功能。

## 核心架构

### 系统层次结构

```
┌─────────────────────────────────────────────────────────┐
│                    用户层 (User Layer)                    │
│                                                           │
│  ┌──────────────┐              ┌──────────────┐          │
│  │  文字输入     │              │  语音输入     │          │
│  │  Text Input  │              │ Voice Input  │          │
│  └──────────────┘              └──────────────┘          │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                 Web 前端 (Web Frontend)                   │
│                                                           │
│  ┌──────────────────────────────────────────────────┐    │
│  │  index.html + CSS + JavaScript                    │    │
│  │  - 录音功能 (MediaRecorder)                       │    │
│  │  - API 调用 (Fetch)                               │    │
│  │  - 结果展示                                       │    │
│  └──────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
                          ↓ HTTP POST /api/navigate
┌─────────────────────────────────────────────────────────┐
│               Go HTTP 服务器 (Go Backend)                 │
│                   :8080                                   │
│                                                           │
│  ┌──────────────────────────────────────────────────┐    │
│  │  internal/server/server.go                        │    │
│  │  - 路由管理                                       │    │
│  │  - 请求处理                                       │    │
│  │  - 响应生成                                       │    │
│  └──────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
                          ↓
         ┌────────────────┴────────────────┐
         ↓                                  ↓
┌──────────────────────┐        ┌──────────────────────┐
│   STT 模块 (语音)     │        │   AI 处理模块         │
│  internal/stt/       │        │  internal/ai/        │
│                      │        │                      │
│  ┌────────────────┐  │        │  ┌────────────────┐  │
│  │ OpenAI Whisper │  │        │  │   ChatGPT      │  │
│  └────────────────┘  │        │  └────────────────┘  │
│         ↓ 失败       │        │  ┌────────────────┐  │
│  ┌────────────────┐  │        │  │    Claude      │  │
│  │  本地降级       │  │        │  └────────────────┘  │
│  │ whisper.cpp    │  │        │  ┌────────────────┐  │
│  │     vosk       │  │        │  │   DeepSeek     │  │
│  └────────────────┘  │        │  └────────────────┘  │
└──────────────────────┘        └──────────────────────┘
         ↓                                  ↓
         └────────────────┬────────────────┘
                          ↓
              ┌──────────────────────┐
              │  地图 URL 生成        │
              │  pkg/mapprovider/    │
              │                      │
              │  - 百度地图          │
              │  - 高德地图          │
              │  - Google Maps      │
              └──────────────────────┘
                          ↓
                   返回 URL 给前端
                          ↓
                   前端跳转到地图
```

## 模块详解

### 1. Web 前端模块

**位置**：`web/`

**组件**：
- `index.html`：主页面结构
- `static/css/style.css`：样式定义
- `static/js/app.js`：交互逻辑

**功能**：
- 📝 文字输入处理
- 🎤 语音录制（WebRTC MediaRecorder）
- 🔄 API 请求发送（Fetch API）
- 📊 结果展示
- 🎨 响应式 UI

**技术栈**：
- HTML5
- CSS3（渐变、阴影、动画）
- JavaScript（原生，无框架）
- WebRTC API

### 2. HTTP 服务器模块

**位置**：`internal/server/server.go`

**职责**：
- 🌐 HTTP 服务器管理
- 🔀 路由分发
- 📥 请求解析
- 📤 响应生成
- 🔄 CORS 处理

**API 端点**：

```go
GET  /                   // 主页
GET  /static/*          // 静态文件
POST /api/navigate      // 导航请求
GET  /api/health        // 健康检查
```

**核心流程**：

```go
handleNavigate(request) {
    1. 解析请求（文字 or 语音）
    2. if (语音) → STT 转录
    3. AI 提取意图 (起点/终点)
    4. 生成地图 URL
    5. 返回响应
}
```

### 3. STT 模块（语音转文字）

**位置**：`internal/stt/`

**文件结构**：
- `stt.go`：接口定义、自动降级客户端
- `openai.go`：OpenAI Whisper 实现
- `local.go`：本地降级实现

**降级策略**：

```
OpenAI Whisper (优先)
    ↓ 失败
whisper.cpp (本地模型)
    ↓ 失败
vosk (轻量级识别)
    ↓ 失败
简单提示 "[语音识别失败，请使用文字输入]"
```

**接口设计**：

```go
type Client interface {
    TranscribeAudio(ctx, audio, format) (*Result, error)
    GetProviderName() string
}

type Result struct {
    Text     string   // 转换的文字
    Language string   // 识别的语言
    Provider Provider // 使用的提供商
}
```

### 4. AI 处理模块

**位置**：`internal/ai/`

**文件结构**：
- `ai.go`：接口定义、工厂方法
- `chatgpt.go`：ChatGPT 实现
- `claude.go`：Claude 实现
- `deepseek.go`：DeepSeek 实现

**统一接口**：

```go
type Client interface {
    ExtractNavigationIntent(ctx, text) (*NavigationIntent, error)
    GetProviderName() string
}

type NavigationIntent struct {
    Start string `json:"start"` // 起点
    End   string `json:"end"`   // 终点
}
```

**AI 提示词策略**：

所有 AI 客户端使用统一的提示词模板：

```
你是一个智能导航助手。用户会说出导航需求，你需要提取起点和终点。
请以 JSON 格式返回结果：{"start": "起点", "end": "终点"}

规则：
1. 如果用户只说了目的地，起点设为"当前位置"
2. 提取具体的地址、地点名称
3. 只返回 JSON，不要其他文字
```

**支持的模型**：

| 提供商 | 模型 | 特点 |
|--------|------|------|
| ChatGPT | gpt-3.5-turbo | 快速、经济 |
| Claude | claude-3-5-sonnet | 智能、准确 |
| DeepSeek | deepseek-chat | 中文优化 |

### 5. 配置管理模块

**位置**：`internal/config/config.go`

**配置文件**：`config.yaml`

**功能**：
- 📄 YAML 配置加载
- 🔐 环境变量替换
- ⚙️ 默认值提供

**配置结构**：

```yaml
server:        # HTTP 服务器配置
stt:           # STT 配置
ai:            # AI 配置（多提供商）
map:           # 地图配置
```

**环境变量支持**：

```yaml
openai_key: "${OPENAI_API_KEY}"  # 从环境变量读取
```

### 6. 地图服务模块

**位置**：`pkg/mapprovider/mapprovider.go`

**支持的地图**：

1. **百度地图**
   - URL: `https://map.baidu.com/`
   - 参数: `origin=起点&destination=终点&mode=driving`

2. **高德地图**
   - URL: `https://uri.amap.com/navigation`
   - 参数: `from=起点&to=终点`

3. **Google Maps**
   - URL: `https://www.google.com/maps/dir/`
   - 参数: `起点/终点`

**函数接口**：

```go
GenerateMapURL(provider, start, end string) (string, error)
GenerateBaiduMapURL(start, end string) string
GenerateAmapURL(start, end string) string
GenerateGoogleMapsURL(start, end string) string
```

## 数据流详解

### 文字输入流程

```
1. 用户在输入框输入："从北京去上海"
   ↓
2. 前端验证输入非空
   ↓
3. 构建请求：
   {
     "type": "text",
     "input": "从北京去上海",
     "ai_provider": "chatgpt",
     "map_provider": "baidu"
   }
   ↓
4. POST /api/navigate
   ↓
5. 服务器解析请求
   ↓
6. 调用 ChatGPT 客户端：
   ExtractNavigationIntent("从北京去上海")
   ↓
7. ChatGPT 返回：
   {
     "start": "北京",
     "end": "上海"
   }
   ↓
8. 生成百度地图 URL：
   "https://map.baidu.com/?origin=北京&destination=上海&mode=driving"
   ↓
9. 返回响应：
   {
     "success": true,
     "url": "...",
     "start": "北京",
     "end": "上海"
   }
   ↓
10. 前端接收响应，跳转到地图
```

### 语音输入流程

```
1. 用户点击"开始录音"
   ↓
2. 浏览器请求麦克风权限
   ↓
3. MediaRecorder 开始录制
   ↓
4. 用户说话："从西湖到灵隐寺"
   ↓
5. 用户点击"停止录音"
   ↓
6. MediaRecorder 停止，保存为 Blob
   ↓
7. 前端转换为 Base64
   ↓
8. 构建请求：
   {
     "type": "audio",
     "audio": "base64_data...",
     "format": "webm",
     "ai_provider": "chatgpt",
     "map_provider": "baidu"
   }
   ↓
9. POST /api/navigate
   ↓
10. 服务器解码 Base64 → 音频数据
    ↓
11. 调用 STT 客户端（OpenAI Whisper）：
    TranscribeAudio(audio, "webm")
    ↓
12. Whisper 返回：
    {
      "text": "从西湖到灵隐寺",
      "language": "zh"
    }
    ↓
13. 调用 AI 客户端：
    ExtractNavigationIntent("从西湖到灵隐寺")
    ↓
14. AI 返回：
    {
      "start": "西湖",
      "end": "灵隐寺"
    }
    ↓
15. 生成地图 URL
    ↓
16. 返回响应（包含识别的文字）
    ↓
17. 前端展示识别结果，然后跳转
```

## 错误处理机制

### 1. STT 降级

```go
AutoClient.TranscribeAudio() {
    // 尝试 OpenAI Whisper
    result, err := primaryClient.TranscribeAudio()
    if err == nil {
        return result  // 成功
    }
    
    // 降级到本地
    if enableFallback {
        return fallbackClient.TranscribeAudio()
    }
    
    return error
}
```

### 2. AI 调用失败

```go
// 返回详细错误信息
{
  "success": false,
  "error": "AI 处理失败: API key 无效",
  "error_type": "ai_error"
}
```

### 3. 网络错误

```go
// 设置超时
ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
defer cancel()
```

## 安全性考虑

### 1. API Key 管理

- ✅ 使用环境变量存储
- ✅ 不在代码中硬编码
- ✅ 不提交到版本控制

### 2. 输入验证

```go
// 验证音频大小
if len(audioData) > 10*1024*1024 {  // 10MB
    return error("音频文件过大")
}

// 验证文字长度
if len(text) > 1000 {
    return error("文字输入过长")
}
```

### 3. CORS 配置

```go
w.Header().Set("Access-Control-Allow-Origin", "*")
w.Header().Set("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
w.Header().Set("Access-Control-Allow-Headers", "Content-Type")
```

## 性能优化

### 1. HTTP 客户端复用

```go
type ChatGPTClient struct {
    client *http.Client  // 复用连接
}
```

### 2. 上下文超时

```go
ctx, cancel := context.WithTimeout(ctx, 30*time.Second)
defer cancel()
```

### 3. 降级策略

- STT 失败 → 本地处理
- 减少 API 调用成本

## 可扩展性

### 1. 添加新 AI 提供商

```go
// 1. 创建 internal/ai/newai.go
type NewAIClient struct { ... }

func (c *NewAIClient) ExtractNavigationIntent() { ... }

// 2. 在 ai.go 中注册
case ProviderNewAI:
    return NewNewAIClient(config)
```

### 2. 添加新地图服务

```go
// 在 mapprovider.go 中添加
func GenerateNewMapURL(start, end string) string {
    // 实现 URL 生成逻辑
}
```

### 3. 添加新 STT 提供商

```go
// 创建 internal/stt/newstt.go
type NewSTTClient struct { ... }

func (c *NewSTTClient) TranscribeAudio() { ... }
```

## 部署架构

### 开发环境

```
localhost:8080
├── Go 服务器
├── 静态文件（web/）
└── API 端点
```

### 生产环境建议

```
                   Internet
                      ↓
              ┌───────────────┐
              │  Nginx (443)  │  HTTPS
              └───────────────┘
                      ↓
              ┌───────────────┐
              │  qwall2 (8080)│  HTTP
              └───────────────┘
                      ↓
       ┌──────────────┴──────────────┐
       ↓                              ↓
┌─────────────┐              ┌─────────────┐
│   AI APIs   │              │   STT API   │
│ ChatGPT     │              │  Whisper    │
│ Claude      │              └─────────────┘
│ DeepSeek    │
└─────────────┘
```

## 技术栈总结

### 后端
- **语言**：Go 1.23.0
- **HTTP**：net/http（标准库）
- **配置**：gopkg.in/yaml.v3
- **依赖**：minimal（仅 YAML）

### 前端
- **HTML5**：结构
- **CSS3**：样式
- **JavaScript**：原生（无框架）
- **API**：WebRTC MediaRecorder、Fetch

### 外部服务
- **AI**：OpenAI、Anthropic、DeepSeek
- **STT**：OpenAI Whisper
- **地图**：百度、高德、Google

## 总结

qwall2 系统采用了模块化、可扩展的架构设计：

1. ✅ **清晰的层次结构**：前端 → 后端 → 服务层
2. ✅ **统一的接口设计**：AI、STT 都有统一接口
3. ✅ **智能的降级机制**：保证系统可用性
4. ✅ **灵活的配置管理**：支持多环境部署
5. ✅ **良好的错误处理**：详细的错误信息
6. ✅ **高可扩展性**：易于添加新功能

系统已经完全实现并可以投入使用！🚀
