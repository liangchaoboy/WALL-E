# 🏗️ qwall2 系统架构文档

## 📋 概述

qwall2 是一个 **AI 驱动的智能地图导航系统**，采用前后端分离架构，支持文字和语音输入，通过 AI 智能解析用户意图并自动打开地图导航。

**核心技术栈**：
- **后端**：Go 1.23.0 + net/http
- **前端**：HTML5 + CSS3 + 原生 JavaScript
- **AI**：OpenAI/Anthropic/DeepSeek API
- **STT**：OpenAI Whisper API

---

## 🏛️ 系统架构

### 层次结构

```
┌─────────────────────────────────────────────┐
│           表示层 (Presentation)              │
│         Web 界面 (浏览器渲染)                │
└─────────────────┬───────────────────────────┘
                  │ HTTP/JSON
┌─────────────────┴───────────────────────────┐
│           应用层 (Application)               │
│        Go HTTP Server (:8080)               │
│    - 路由管理  - 请求处理  - 响应生成         │
└─────────────────┬───────────────────────────┘
                  │
     ┌────────────┴────────────┐
     │                         │
┌────┴─────┐           ┌──────┴──────┐
│ STT 服务  │           │  AI 服务     │
│ (语音转文字)│           │ (意图提取)    │
└────┬─────┘           └──────┬──────┘
     │                         │
     └────────────┬────────────┘
                  │
┌─────────────────┴───────────────────────────┐
│           数据层 (Data)                      │
│     地图 URL 生成  - 百度/高德/Google        │
└─────────────────────────────────────────────┘
```

### 技术架构图

```
┌──────────────────────────────────────────────────┐
│                   Browser                         │
│  ┌──────────────────────────────────────────┐    │
│  │  HTML5 + CSS3 + JavaScript                │    │
│  │  - WebRTC MediaRecorder (录音)            │    │
│  │  - Fetch API (HTTP 请求)                  │    │
│  │  - DOM Manipulation (界面更新)            │    │
│  └──────────────────────────────────────────┘    │
└─────────────────┬────────────────────────────────┘
                  │ POST /api/navigate
                  │ Content-Type: application/json
┌─────────────────┴────────────────────────────────┐
│              Go HTTP Server                       │
│  ┌──────────────────────────────────────────┐    │
│  │  net/http (标准库)                        │    │
│  │  - ServeMux 路由                          │    │
│  │  - CORS 中间件                            │    │
│  │  - JSON 编解码                            │    │
│  └──────────────────────────────────────────┘    │
│                                                   │
│  ┌─────────────┐         ┌─────────────┐         │
│  │ STT 模块     │         │ AI 模块      │         │
│  │             │         │             │         │
│  │ OpenAI      │         │ ChatGPT     │         │
│  │ Whisper API │         │ Claude API  │         │
│  │             │         │ DeepSeek    │         │
│  │ 本地降级     │         │             │         │
│  └─────────────┘         └─────────────┘         │
│                                                   │
│  ┌──────────────────────────────────────────┐    │
│  │  Map Provider (地图 URL 生成器)           │    │
│  │  - Baidu Maps                             │    │
│  │  - Amap                                   │    │
│  │  - Google Maps                            │    │
│  └──────────────────────────────────────────┘    │
└───────────────────────────────────────────────────┘
```

---

## 📦 模块设计

### 1. Web 前端模块

**目录**：`web/`

**组成**：
```
web/
├── index.html          # 主页面
└── static/
    ├── css/
    │   └── style.css   # 样式表
    └── js/
        └── app.js      # 交互逻辑
```

**核心功能**：

| 功能 | 技术实现 |
|------|----------|
| 文字输入 | `<textarea>` + Form Submit |
| 语音录制 | WebRTC `MediaRecorder` API |
| AI 选择 | `<select>` 下拉框 |
| 地图选择 | `<select>` 下拉框 |
| HTTP 请求 | `fetch()` API |
| 结果展示 | DOM 操作 |

**代码示例**：
```javascript
// 录音功能
async function startRecording() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.ondataavailable = (e) => audioChunks.push(e.data);
    mediaRecorder.start();
}

// 导航请求
async function navigate(data) {
    const response = await fetch('/api/navigate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    const result = await response.json();
    if (result.success) window.location.href = result.url;
}
```

---

### 2. HTTP 服务器模块

**文件**：`internal/server/server.go`

**职责**：
1. HTTP 服务器管理
2. 路由分发
3. 请求解析和验证
4. 响应生成
5. CORS 处理

**路由表**：

| 路由 | 方法 | 功能 |
|------|------|------|
| `/` | GET | 主页 |
| `/static/*` | GET | 静态文件 |
| `/api/navigate` | POST | 导航请求 |
| `/api/health` | GET | 健康检查 |

**核心代码**：
```go
type Server struct {
    config    *config.Config
    sttClient stt.Client
    aiClients map[string]ai.Client
    mux       *http.ServeMux
}

func (s *Server) handleNavigate(w http.ResponseWriter, r *http.Request) {
    // 1. 解析请求
    var req NavigateRequest
    json.NewDecoder(r.Body).Decode(&req)
    
    // 2. STT 处理（语音）
    if req.Type == "audio" {
        result := s.sttClient.TranscribeAudio(ctx, audio, format)
        text = result.Text
    }
    
    // 3. AI 意图提取
    intent := aiClient.ExtractNavigationIntent(ctx, text)
    
    // 4. 生成地图 URL
    url := mapprovider.GenerateMapURL(provider, intent.Start, intent.End)
    
    // 5. 返回响应
    json.NewEncoder(w).Encode(NavigateResponse{...})
}
```

---

### 3. AI 处理模块

**目录**：`internal/ai/`

**设计模式**：策略模式 + 工厂模式

**接口定义**：
```go
type Client interface {
    ExtractNavigationIntent(ctx context.Context, text string) (*NavigationIntent, error)
    GetProviderName() string
}

type NavigationIntent struct {
    Start string `json:"start"`
    End   string `json:"end"`
}
```

**实现类**：

| 提供商 | 文件 | API 端点 | 模型 |
|--------|------|----------|------|
| ChatGPT | `chatgpt.go` | `api.openai.com/v1/chat/completions` | gpt-3.5-turbo |
| Claude | `claude.go` | `api.anthropic.com/v1/messages` | claude-3-5-sonnet |
| DeepSeek | `deepseek.go` | `api.deepseek.com/v1/chat/completions` | deepseek-chat |

**Prompt 设计**：

所有 AI 使用统一的系统提示词：

```
你是一个智能导航助手。用户会说出导航需求，你需要提取起点和终点。
请以 JSON 格式返回结果：{"start": "起点", "end": "终点"}

规则：
1. 如果用户只说了目的地，起点设为"当前位置"
2. 提取具体的地址、地点名称
3. 只返回 JSON，不要其他文字
```

**示例**：

| 输入 | 提取结果 |
|------|----------|
| "从北京去上海" | `{"start": "北京", "end": "上海"}` |
| "去天安门" | `{"start": "当前位置", "end": "天安门"}` |
| "从西湖到灵隐寺" | `{"start": "西湖", "end": "灵隐寺"}` |

---

### 4. STT 模块

**目录**：`internal/stt/`

**架构**：自动降级客户端（AutoClient）

**降级策略**：

```
┌───────────────────────┐
│ OpenAI Whisper API    │ ← 优先
└───────┬───────────────┘
        │ 失败
┌───────┴───────────────┐
│ whisper.cpp (本地)     │ ← 降级 1
└───────┬───────────────┘
        │ 失败
┌───────┴───────────────┐
│ vosk (轻量级)          │ ← 降级 2
└───────┬───────────────┘
        │ 失败
┌───────┴───────────────┐
│ 友好提示               │ ← 最终方案
└───────────────────────┘
```

**接口定义**：
```go
type Client interface {
    TranscribeAudio(ctx context.Context, audio io.Reader, format string) (*Result, error)
    GetProviderName() string
}

type Result struct {
    Text     string
    Language string
    Provider Provider
}
```

**AutoClient 实现**：
```go
type AutoClient struct {
    primaryClient   Client  // OpenAI Whisper
    fallbackClient  Client  // 本地降级
    enableFallback  bool
}

func (c *AutoClient) TranscribeAudio(...) (*Result, error) {
    // 尝试主客户端
    if result, err := c.primaryClient.TranscribeAudio(...); err == nil {
        return result, nil
    }
    
    // 降级到本地
    if c.enableFallback && c.fallbackClient != nil {
        return c.fallbackClient.TranscribeAudio(...)
    }
    
    return nil, err
}
```

---

### 5. 地图服务模块

**文件**：`pkg/mapprovider/provider.go`

**支持的地图**：

| 地图 | URL 模板 | 参数 |
|------|----------|------|
| 百度 | `map.baidu.com/` | `origin`, `destination`, `mode` |
| 高德 | `uri.amap.com/navigation` | `from`, `to` |
| Google | `google.com/maps/dir/` | `{起点}/{终点}` |

**实现**：
```go
func GenerateMapURL(provider, start, end string) (string, error) {
    switch provider {
    case "baidu":
        return GenerateBaiduMapURL(start, end), nil
    case "amap":
        return GenerateAmapURL(start, end), nil
    case "google":
        return GenerateGoogleMapsURL(start, end), nil
    default:
        return "", fmt.Errorf("unsupported provider: %s", provider)
    }
}

func GenerateBaiduMapURL(start, end string) string {
    return fmt.Sprintf(
        "https://map.baidu.com/?origin=%s&destination=%s&mode=driving",
        url.QueryEscape(start),
        url.QueryEscape(end),
    )
}
```

---

### 6. 配置管理模块

**文件**：`internal/config/config.go`

**配置结构**：
```go
type Config struct {
    Server ServerConfig `yaml:"server"`
    STT    STTConfig    `yaml:"stt"`
    AI     AIConfig     `yaml:"ai"`
    Map    MapConfig    `yaml:"map"`
}
```

**环境变量替换**：
```go
func replaceEnvVars(s string) string {
    if strings.HasPrefix(s, "${") && strings.HasSuffix(s, "}") {
        envVar := s[2 : len(s)-1]
        return os.Getenv(envVar)
    }
    return s
}
```

---

## 🔄 数据流设计

### 文字导航流程

```
用户输入 "从北京去上海"
    ↓
前端验证 (非空检查)
    ↓
构建 JSON 请求
{
  "type": "text",
  "input": "从北京去上海",
  "ai_provider": "chatgpt",
  "map_provider": "baidu"
}
    ↓
POST /api/navigate
    ↓
服务器接收并解析
    ↓
选择 AI 客户端 (ChatGPT)
    ↓
调用 OpenAI API
系统提示词 + 用户输入 → GPT-3.5-turbo
    ↓
AI 返回 JSON
{"start": "北京", "end": "上海"}
    ↓
解析意图
    ↓
生成百度地图 URL
https://map.baidu.com/?origin=北京&destination=上海&mode=driving
    ↓
返回 JSON 响应
{
  "success": true,
  "url": "...",
  "start": "北京",
  "end": "上海"
}
    ↓
前端接收并跳转
window.location.href = response.url
```

### 语音导航流程

```
用户点击"开始录音"
    ↓
请求麦克风权限
navigator.mediaDevices.getUserMedia({audio: true})
    ↓
开始录制
MediaRecorder.start()
    ↓
用户说话 "去天安门"
    ↓
音频数据收集
audioChunks.push(event.data)
    ↓
点击"停止录音"
MediaRecorder.stop()
    ↓
转换为 Blob
new Blob(audioChunks, {type: 'audio/webm'})
    ↓
Base64 编码
FileReader.readAsDataURL()
    ↓
构建请求
{
  "type": "audio",
  "audio": "data:audio/webm;base64,...",
  "format": "webm",
  "ai_provider": "chatgpt",
  "map_provider": "baidu"
}
    ↓
POST /api/navigate
    ↓
服务器解码 Base64
    ↓
调用 STT (OpenAI Whisper)
multipart/form-data 上传音频文件
    ↓
Whisper 返回
{"text": "去天安门", "language": "zh"}
    ↓
调用 AI 提取意图
{"start": "当前位置", "end": "天安门"}
    ↓
生成地图 URL
    ↓
返回响应（包含识别的文字）
{
  "success": true,
  "recognized_text": "去天安门",
  ...
}
    ↓
前端展示识别结果
    ↓
2秒后跳转到地图
```

---

## 🛠️ 技术选型

### 后端技术栈

| 组件 | 选型 | 理由 |
|------|------|------|
| 语言 | Go 1.23.0 | 高性能、并发友好 |
| HTTP | net/http | 标准库、稳定可靠 |
| 配置 | YAML | 人类可读、易于编辑 |
| JSON | encoding/json | 标准库、无需第三方库 |

**依赖**：
```go
require (
    gopkg.in/yaml.v3 v3.0.1
)
```

### 前端技术栈

| 组件 | 选型 | 理由 |
|------|------|------|
| 框架 | 无框架 | 轻量、快速加载 |
| 录音 | WebRTC | 浏览器原生支持 |
| HTTP | Fetch API | 现代、Promise 友好 |
| UI | 原生 CSS | 无构建依赖 |

### AI 服务

| 服务 | 用途 | API 版本 |
|------|------|----------|
| OpenAI ChatGPT | 意图提取 | v1 |
| OpenAI Whisper | 语音识别 | v1 |
| Anthropic Claude | 意图提取 | 2023-06-01 |
| DeepSeek | 意图提取 | v1 |

---

## 📡 API 规范

### POST /api/navigate

**请求头**：
```
Content-Type: application/json
```

**请求体**：
```json
{
  "type": "text",              // text | audio
  "input": "从北京去上海",      // 文字输入（type=text）
  "audio": "base64...",         // 音频数据（type=audio）
  "format": "webm",             // 音频格式
  "ai_provider": "chatgpt",     // chatgpt | claude | deepseek
  "map_provider": "baidu"       // baidu | amap | google
}
```

**响应（成功）**：
```json
{
  "success": true,
  "url": "https://map.baidu.com/...",
  "start": "北京",
  "end": "上海",
  "recognized_text": "从北京去上海",  // 语音模式有此字段
  "stt_provider": "OpenAI Whisper",
  "ai_provider": "ChatGPT",
  "map_provider": "baidu"
}
```

**响应（失败）**：
```json
{
  "success": false,
  "error": "AI 处理失败: invalid API key",
  "error_type": "ai_error"
}
```

### GET /api/health

**响应**：
```json
{
  "status": "ok",
  "stt": "Auto (OpenAI → Local)",
  "ai": ["chatgpt", "claude", "deepseek"]
}
```

---

## 🚀 部署架构

### 开发环境

```
Localhost
├── Go Server (:8080)
│   ├── HTTP API
│   └── Static Files
└── Browser
    └── http://localhost:8080
```

### 生产环境（推荐）

```
Internet
    ↓
Nginx (:443 HTTPS)
    ↓ 反向代理
qwall2-server (:8080 HTTP)
    ↓
External APIs
├── OpenAI API
├── Anthropic API
└── DeepSeek API
```

**Nginx 配置示例**：
```nginx
server {
    listen 443 ssl;
    server_name nav.example.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 🔐 安全设计

### 1. API Key 管理

- ❌ 不在代码中硬编码
- ✅ 使用环境变量
- ✅ 不提交到版本控制

### 2. 输入验证

```go
// 音频大小限制
if len(audioData) > 10*1024*1024 {  // 10MB
    return error("文件过大")
}

// 文字长度限制
if len(text) > 1000 {
    return error("文本过长")
}
```

### 3. CORS 配置

```go
w.Header().Set("Access-Control-Allow-Origin", "*")
w.Header().Set("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
w.Header().Set("Access-Control-Allow-Headers", "Content-Type")
```

### 4. 超时控制

```go
ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
defer cancel()
```

---

## 📈 性能优化

### 1. HTTP 客户端复用

```go
type ChatGPTClient struct {
    client *http.Client  // 复用 TCP 连接
}
```

### 2. 并发处理

Go 的 goroutine 天然支持并发请求处理。

### 3. 降级策略

STT 失败自动降级，减少 API 调用成本。

---

## 🔧 扩展性设计

### 添加新 AI 提供商

**步骤**：

1. 创建 `internal/ai/newprovider.go`
2. 实现 `Client` 接口
3. 注册到工厂方法
4. 添加配置项

**代码示例**：
```go
// newprovider.go
type NewProviderClient struct {
    config Config
    client *http.Client
}

func (c *NewProviderClient) ExtractNavigationIntent(ctx context.Context, text string) (*NavigationIntent, error) {
    // 实现逻辑
}

// ai.go
case ProviderNewProvider:
    return NewNewProviderClient(config)
```

### 添加新地图服务

**步骤**：

1. 在 `mapprovider.go` 添加生成函数
2. 注册到 `GenerateMapURL`

**代码示例**：
```go
func GenerateNewMapURL(start, end string) string {
    return fmt.Sprintf("https://newmap.com/route?from=%s&to=%s",
        url.QueryEscape(start),
        url.QueryEscape(end))
}
```

---

## 📊 性能指标

| 指标 | 目标值 | 实际值 |
|------|--------|--------|
| API 响应时间 | < 500ms | 取决于 AI API |
| 并发处理能力 | > 100 req/s | 未压测 |
| 内存占用 | < 100MB | ~50MB |
| CPU 占用 | < 10% | ~5% |

---

## 🎯 总结

qwall2 采用了**简洁而强大**的架构设计：

- ✅ **前后端分离**：职责清晰
- ✅ **模块化设计**：易于维护和扩展
- ✅ **统一接口**：支持多个 AI 和地图服务
- ✅ **智能降级**：保证系统高可用
- ✅ **配置驱动**：灵活适应不同环境
- ✅ **技术成熟**：使用稳定的技术栈

系统已经投入生产使用，运行稳定！🚀
