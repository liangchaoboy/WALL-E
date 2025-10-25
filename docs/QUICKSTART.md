# 🚀 QWall2 快速入门

> AI 地图导航系统 - 支持语音识别和智能导航

## ✨ 功能特色

- 🎤 **Chrome 语音识别** - 无需 API 密钥，使用浏览器原生功能
- 🤖 **多 AI 支持** - Claude、ChatGPT、DeepSeek、Mock 模式
- 🗺️ **多地图支持** - 百度地图、高德地图、Google Maps
- 🌐 **Web 界面** - 现代化响应式设计

## 🏃‍♂️ 快速开始

### 1. 启动服务

```bash
# 克隆项目
git clone <repository-url>
cd qwall2

# 启动服务
./start.sh
```

### 2. 访问应用

打开浏览器访问：`http://localhost:8090`

### 3. 使用语音导航

1. 点击 **"🎤 语音输入"** 标签
2. 点击 **"点击开始识别"** 按钮
3. 说出导航需求，如："从北京到上海"
4. 点击 **"🚀 开始导航"** 按钮

## ⚙️ 配置说明

### 环境变量（可选）

```bash
# Claude AI (推荐)
export ANTHROPIC_API_KEY="your-claude-api-key"
export ANTHROPIC_BASE_URL="https://api.anthropic.com/v1"

# ChatGPT
export OPENAI_API_KEY="your-openai-api-key"

# DeepSeek
export DEEPSEEK_API_KEY="your-deepseek-api-key"
```

### 配置文件

编辑 `config.yaml` 文件：

```yaml
# AI 配置
ai:
  default_provider: "mock"  # mock, claude, chatgpt, deepseek

# 地图配置  
map:
  default_provider: "baidu"  # baidu, amap, google
```

## 🎯 使用场景

### 语音导航示例

- **"从北京到上海"** → 生成北京到上海的导航链接
- **"去杭州西湖"** → 生成到杭州西湖的导航链接
- **"用高德地图从广州到深圳"** → 指定地图提供商的导航

### 支持的地图

- **百度地图** - 国内导航首选
- **高德地图** - 高精度导航
- **Google Maps** - 国际导航

## 🔧 故障排除

### 常见问题

1. **语音识别不工作**
   - 确保使用 Chrome 浏览器
   - 检查麦克风权限
   - 尝试刷新页面

2. **AI 服务不可用**
   - 系统会自动降级到 Mock 模式
   - 配置 API 密钥以获得更好的体验

3. **端口冲突**
   - 修改 `config.yaml` 中的端口号
   - 重启服务

### 日志查看

```bash
# 查看服务日志
tail -f logs/qwall2.log

# 检查服务状态
curl http://localhost:8090/api/health
```

## 📚 更多文档

- [系统架构](docs/ARCHITECTURE.md) - 技术架构详解
- [功能演示](docs/DEMO.md) - 完整功能展示
- [API 配置](docs/THIRD_PARTY_API.md) - 第三方 API 设置
- [项目状态](docs/STATUS.md) - 开发进度和计划

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License