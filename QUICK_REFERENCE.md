# ⚡ qwall2 快速参考卡

> 所有你需要的命令和文档，一张卡片搞定！

---

## 🚀 快速启动（3 步）

```bash
# 1. 配置 API Key
export OPENAI_API_KEY="sk-your-key"

# 2. 启动服务
./start.sh

# 3. 打开浏览器
# http://localhost:8080
```

---

## 📁 项目结构

```
qwall2/
├── docs/              📚 所有文档
├── internal/          💻 Go 核心代码
├── web/               🌐 Web 前端
├── start.sh           🚀 启动脚本
├── test.sh            🧪 测试脚本
└── README.md          📖 项目概览
```

---

## 🛠️ 常用命令

```bash
# 启动服务
./start.sh

# 运行测试
./test.sh

# 使用 Makefile
make build     # 编译
make server    # 启动（使用 start.sh）
make test      # 测试
make clean     # 清理
make help      # 帮助

# 编译
go build -o qwall2-server main.go

# 直接运行
./qwall2-server
```

---

## 📚 文档快速查找

| 需求 | 文档 | 时间 |
|------|------|------|
| **快速上手** | [docs/QUICKSTART.md](docs/QUICKSTART.md) | 10 分钟 |
| **项目概览** | [README.md](README.md) | 5 分钟 |
| **系统架构** | [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | 30 分钟 |
| **功能演示** | [docs/DEMO.md](docs/DEMO.md) | 20 分钟 |
| **第三方 API** | [docs/THIRD_PARTY_API.md](docs/THIRD_PARTY_API.md) | 15 分钟 |
| **模型配置** | [docs/MODEL_PARAMS_GUIDE.md](docs/MODEL_PARAMS_GUIDE.md) | 20 分钟 |
| **文档导航** | [docs/DOCS.md](docs/DOCS.md) | 5 分钟 |

---

## ⚙️ 环境变量配置

### 必需配置
```bash
export OPENAI_API_KEY="sk-your-openai-key"
```

### 可选配置（多 AI 模型）
```bash
export ANTHROPIC_API_KEY="sk-ant-your-key"
export DEEPSEEK_API_KEY="sk-your-key"
```

### 可选配置（第三方 API）
```bash
export OPENAI_BASE_URL="https://your-proxy.com/v1"
export OPENAI_MODEL="gpt-3.5-turbo"
```

完整配置请查看：[docs/QUICKSTART.md](docs/QUICKSTART.md#配置-api-key)

---

## 🌐 API 接口

### 导航接口
```bash
POST http://localhost:8080/api/navigate
Content-Type: application/json

{
  "type": "text",
  "input": "从北京去上海",
  "ai_provider": "chatgpt",
  "map_provider": "baidu"
}
```

### 健康检查
```bash
GET http://localhost:8080/api/health
```

---

## 🐛 常见问题

### 服务器无法启动
```bash
# 检查端口占用
lsof -i :8080

# 修改端口（在 config.yaml）
server:
  port: 8081
```

### API Key 错误
```bash
# 检查环境变量
echo $OPENAI_API_KEY

# 重新设置
export OPENAI_API_KEY="sk-correct-key"
./start.sh
```

### 语音识别失败
- 检查 OPENAI_API_KEY 是否正确
- 检查浏览器麦克风权限
- 确认使用 HTTPS 或 localhost

---

## 🎯 核心特性

- ✅ **双模输入**：文字 + 语音
- ✅ **多 AI 引擎**：ChatGPT / Claude / DeepSeek
- ✅ **智能 STT**：Whisper + 本地降级
- ✅ **多地图**：百度 / 高德 / Google
- ✅ **第三方 API**：支持国内代理、OneAPI、私有部署

---

## 📊 项目状态

- **版本**：v2.0 Web 服务器架构
- **Go 版本**：1.23.0+
- **架构**：Go 后端 + Web 前端
- **部署**：独立部署，无需第三方依赖

详细状态：[docs/STATUS.md](docs/STATUS.md)

---

## 🔗 快速链接

- **GitHub**：https://github.com/sanmu/qwall2
- **Issues**：https://github.com/sanmu/qwall2/issues
- **文档索引**：[docs/DOCS.md](docs/DOCS.md)

---

## 💡 使用技巧

### 技巧 1：使用 .env 文件
```bash
# 创建 .env 文件
cat > .env << EOF
OPENAI_API_KEY=sk-your-key
OPENAI_MODEL=gpt-4
EOF

# 加载环境变量
source .env
./start.sh
```

### 技巧 2：快速切换模型
```bash
# 使用 GPT-4
export OPENAI_MODEL="gpt-4" && ./start.sh

# 使用 Claude Opus
export ANTHROPIC_MODEL="claude-3-opus-20240229" && ./start.sh
```

### 技巧 3：使用国内代理
```bash
export OPENAI_BASE_URL="https://api.openai-proxy.com/v1"
export OPENAI_API_KEY="your-proxy-key"
./start.sh
```

---

## 📞 获取帮助

1. **查看文档**：[docs/DOCS.md](docs/DOCS.md)
2. **故障排查**：[docs/QUICKSTART.md](docs/QUICKSTART.md#故障排查)
3. **提交 Issue**：[GitHub Issues](https://github.com/sanmu/qwall2/issues)

---

**快速启动**：`export OPENAI_API_KEY="sk-..." && ./start.sh`  
**访问地址**：http://localhost:8080

---

**祝您使用愉快！** ✨
