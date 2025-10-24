# 🚀 qwall2 - AI 地图导航系统

基于 MCP 的 AI 智能地图导航系统，支持文字和语音输入，自动打开地图导航。

## ✨ 功能特性

- 🎤 **多模态输入**：支持文字输入和语音输入
- 🤖 **多 AI 支持**：支持 ChatGPT、Claude、DeepSeek 等多个大模型
- 🗣️ **智能 STT**：OpenAI Whisper 优先，失败后自动降级到本地处理
- 🗺️ **多地图服务**：支持百度地图、高德地图、Google Maps
- 🌐 **Web 界面**：简洁美观的 Web UI，响应式设计
- 📦 **独立部署**：无需依赖 Claude Desktop，独立运行

## 🏗️ 系统架构

```
用户（Web 页面）
    ↓ 文字/语音输入
Go HTTP 服务器 (:8080)
    ↓
STT 模块（如果是语音）
    ├─ OpenAI Whisper（优先）
    └─ 本地降级（whisper.cpp/vosk）
    ↓
AI 处理模块
    ├─ ChatGPT
    ├─ Claude
    └─ DeepSeek
    ↓ 提取起点终点
地图 URL 生成
    ↓
返回给前端 → 跳转到地图
```

## 📦 安装部署

### 1. 克隆项目

```bash
git clone https://github.com/sanmu/qwall2.git
cd qwall2
```

### 2. 配置环境变量

```bash
# 必需：OpenAI API Key（用于 ChatGPT 和 Whisper STT）
export OPENAI_API_KEY="sk-..."

# 可选：其他 AI 提供商
export ANTHROPIC_API_KEY="sk-ant-..."  # Claude
export DEEPSEEK_API_KEY="sk-..."       # DeepSeek
```

### 3. 编译项目

```bash
go build -o qwall2-server .
```

### 4. 启动服务

```bash
# 使用启动脚本（推荐）
./start.sh

# 或直接运行
./qwall2-server --config config.yaml
```

### 5. 访问 Web 界面

打开浏览器访问：`http://localhost:8080`

## ⚙️ 配置说明

编辑 `config.yaml` 文件：

```yaml
# HTTP 服务器配置
server:
  port: 8080
  host: "0.0.0.0"

# STT 配置
stt:
  provider: "auto"              # auto, openai, local
  openai_key: "${OPENAI_API_KEY}"
  enable_fallback: true         # 启用降级

# AI 配置
ai:
  default_provider: "chatgpt"   # chatgpt, claude, deepseek
  chatgpt:
    api_key: "${OPENAI_API_KEY}"
    model: "gpt-3.5-turbo"
  claude:
    api_key: "${ANTHROPIC_API_KEY}"
    model: "claude-3-5-sonnet-20241022"
  deepseek:
    api_key: "${DEEPSEEK_API_KEY}"
    model: "deepseek-chat"

# 地图配置
map:
  default_provider: "baidu"     # baidu, amap, google
```

## 📖 使用方法

### 文字输入

1. 在 Web 页面的输入框中输入导航需求
2. 选择 AI 提供商和地图服务
3. 点击"开始导航"按钮
4. 系统会自动提取起点和终点，跳转到地图页面

**示例**：
- "我要从北京去上海"
- "去天安门"
- "从西湖到灵隐寺"

### 语音输入

1. 点击"开始录音"按钮（或按住空格键）
2. 说出导航需求
3. 点击"停止录音"
4. 系统自动识别语音并导航

## 🔧 API 接口

### POST /api/navigate

导航请求接口

**请求**：
```json
{
  "type": "text",              // text 或 audio
  "input": "从北京去上海",      // 文字输入
  "ai_provider": "chatgpt",    // AI 提供商
  "map_provider": "baidu"      // 地图提供商
}
```

**响应**：
```json
{
  "success": true,
  "url": "https://map.baidu.com/...",
  "start": "北京",
  "end": "上海",
  "ai_provider": "ChatGPT",
  "map_provider": "baidu"
}
```

### GET /api/health

健康检查接口

**响应**：
```json
{
  "status": "ok",
  "stt": "Auto (OpenAI → Local)",
  "ai": ["chatgpt", "claude"]
}
```

## 🌟 特色功能

### 1. STT 自动降级

语音识别使用智能降级策略：

1. **优先**：OpenAI Whisper API（高质量）
2. **降级 1**：whisper.cpp（本地模型）
3. **降级 2**：vosk（轻量级本地识别）
4. **最终**：友好的错误提示

### 2. 多 AI 模型支持

统一接口设计，轻松切换：

- **ChatGPT**：OpenAI 的 GPT-3.5/GPT-4
- **Claude**：Anthropic 的 Claude 3.5
- **DeepSeek**：DeepSeek Chat

### 3. 智能意图提取

AI 会从自然语言中提取：
- 起点地址（如果未提供，默认为"当前位置"）
- 终点地址
- 自动过滤噪音，只保留关键信息

## 🛠️ 开发说明

### 项目结构

```
qwall2/
├── main.go                    # 程序入口
├── config.yaml                # 配置文件
├── internal/
│   ├── ai/                    # AI 处理模块
│   │   ├── ai.go              # 接口定义
│   │   ├── chatgpt.go         # ChatGPT 实现
│   │   ├── claude.go          # Claude 实现
│   │   └── deepseek.go        # DeepSeek 实现
│   ├── stt/                   # STT 模块
│   │   ├── stt.go             # 接口定义
│   │   ├── openai.go          # OpenAI Whisper
│   │   └── local.go           # 本地降级
│   ├── server/                # HTTP 服务器
│   │   └── server.go
│   └── config/                # 配置管理
│       └── config.go
├── pkg/
│   └── mapprovider/           # 地图服务
│       └── mapprovider.go
└── web/                       # Web 前端
    ├── index.html
    └── static/
        ├── css/style.css
        └── js/app.js
```

### 添加新的 AI 提供商

1. 在 `internal/ai/` 下创建新文件
2. 实现 `Client` 接口
3. 在 `ai.go` 中注册新提供商
4. 在 `config.yaml` 中添加配置

### 添加新的地图服务

1. 在 `pkg/mapprovider/mapprovider.go` 中添加新的生成函数
2. 在配置中添加新的地图选项

## 🐛 故障排查

### 问题：编译失败

```bash
# 更新依赖
go mod tidy
go mod download
```

### 问题：STT 失败

- 检查 OPENAI_API_KEY 是否正确
- 如果不使用语音，可以只用文字输入
- 本地降级需要安装 whisper.cpp 或 vosk

### 问题：AI 处理失败

- 确认 API Key 正确且有效
- 检查网络连接
- 查看服务器日志了解详细错误

## 📝 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📧 联系方式

如有问题，请提交 Issue。
