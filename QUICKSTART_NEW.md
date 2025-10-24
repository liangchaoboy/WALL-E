# AI 地图导航系统 - 快速开始

## 🚀 快速启动

### 1. 设置 API 密钥

```bash
# 设置环境变量
export OPENAI_API_KEY="sk-..."        # OpenAI (STT + ChatGPT)
export ANTHROPIC_API_KEY="sk-ant-..."  # Claude
export DEEPSEEK_API_KEY="sk-..."      # DeepSeek (可选)
```

### 2. 启动服务

```bash
# 方式 1: 使用启动脚本（推荐）
chmod +x start.sh
./start.sh

# 方式 2: 手动编译并启动
go build -o qwall2-server
./qwall2-server

# 方式 3: 直接运行
go run main.go
```

### 3. 访问 Web 界面

打开浏览器访问：**http://localhost:8080**

---

## 📖 使用说明

### 文字输入

1. 在文字输入框输入导航指令
2. 选择 AI 模型和地图服务（可选）
3. 点击"开始导航"

**示例：**
- "从北京到上海"
- "去杭州西湖"
- "用高德地图从广州到深圳"

### 语音输入

1. 切换到"语音输入"标签
2. 点击麦克风按钮开始录音
3. 说出导航指令
4. 再次点击停止录音
5. 系统自动识别并导航

**语音示例：**
- "从北京到上海"
- "我要去上海东方明珠"

---

## ⚙️ 配置说明

配置文件：`config.yaml`

```yaml
server:
  port: 8080              # HTTP 服务器端口
  host: "0.0.0.0"        # 监听地址

stt:
  provider: "auto"        # auto: 自动降级, openai: 仅OpenAI, local: 仅本地
  enable_fallback: true  # 启用降级（OpenAI失败后用本地）

ai:
  default_provider: "chatgpt"  # 默认 AI: chatgpt, claude, deepseek

map:
  default_provider: "baidu"    # 默认地图: baidu, amap, google
```

---

## 🔧 功能特性

### ✅ 已实现

1. **多种输入方式**
   - ✅ 文字输入
   - ✅ 语音输入（WebRTC录音）

2. **STT 自动降级**
   - ✅ OpenAI Whisper API（优先）
   - ✅ 本地 STT（降级）

3. **多 AI 模型支持**
   - ✅ ChatGPT (OpenAI)
   - ✅ Claude (Anthropic)
   - ✅ DeepSeek

4. **多地图服务**
   - ✅ 百度地图（国内）
   - ✅ 高德地图（国内）
   - ✅ Google Maps（国际）

5. **Web 界面**
   - ✅ 响应式设计
   - ✅ 实时反馈
   - ✅ 错误提示

---

## 📊 API 接口

### POST /api/navigate

**文字请求：**
```json
{
  "type": "text",
  "input": "从北京到上海",
  "ai_provider": "chatgpt",
  "map_provider": "baidu"
}
```

**语音请求：**
```json
{
  "type": "audio",
  "audio": "data:audio/webm;base64,...",
  "format": "webm",
  "ai_provider": "claude"
}
```

**成功响应：**
```json
{
  "success": true,
  "url": "http://api.map.baidu.com/direction?...",
  "start": "北京",
  "end": "上海",
  "recognized_text": "从北京到上海",
  "stt_provider": "openai",
  "ai_provider": "chatgpt",
  "map_provider": "baidu"
}
```

### GET /api/health

健康检查接口

```json
{
  "status": "ok",
  "ai": ["chatgpt", "claude", "deepseek"],
  "stt": "Auto (OpenAI → Local)"
}
```

---

## 🐛 故障排除

### 问题 1：语音识别失败

**原因：** OPENAI_API_KEY 未设置或无效

**解决：**
```bash
export OPENAI_API_KEY="sk-your-real-key"
./start.sh
```

### 问题 2：AI 提取失败

**原因：** 所有 AI 服务都不可用

**解决：** 至少配置一个 AI API Key

### 问题 3：麦克风无法访问

**原因：** 浏览器未授权麦克风权限

**解决：** 检查浏览器设置，允许网站访问麦克风

### 问题 4：端口 8080 被占用

**解决：** 修改 `config.yaml` 中的端口号

---

## 📝 开发说明

### 项目结构

```
qwall2/
├── main.go                    # 程序入口
├── config.yaml               # 配置文件
├── internal/                 # 内部包
│   ├── server/              # HTTP 服务器
│   ├── stt/                 # 语音转文字
│   ├── ai/                  # AI 处理
│   └── config/              # 配置管理
├── pkg/                      # 公共包
│   ├── mapprovider/         # 地图提供商
│   └── parser/              # 解析器（备用）
└── web/                      # Web 前端
    ├── index.html
    └── static/
        ├── css/
        └── js/
```

### 添加新的 AI 模型

1. 在 `internal/ai/` 创建新文件（如 `gemini.go`）
2. 实现 `Client` 接口
3. 在 `ai.go` 中注册新提供商
4. 更新配置文件

### 添加新的地图服务

1. 在 `pkg/mapprovider/provider.go` 添加新函数
2. 更新 `GenerateNavigationURL`
3. 添加测试用例

---

## 🎉 完成！

现在您可以：
1. 通过文字或语音输入导航指令
2. AI 自动提取起点和终点
3. 在浏览器中打开地图导航

**享受 AI 地图导航！** 🗺️
