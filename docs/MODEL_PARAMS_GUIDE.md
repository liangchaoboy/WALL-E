# 🔧 模型参数完整配置指南

## 📋 概述

qwall2 现在支持通过环境变量灵活配置所有 AI 模型和 STT 服务的参数，包括：

- ✅ API Key（API 密钥）
- ✅ Base URL（API 接口地址）
- ✅ Model Name（模型名称）

这三个参数组合使用，可以支持任何兼容的第三方 API 服务。

---

## 🎯 完整参数列表

### ChatGPT / OpenAI

| 参数 | 环境变量 | 配置文件字段 | 默认值 |
|------|----------|--------------|--------|
| API Key | `OPENAI_API_KEY` | `ai.chatgpt.api_key` | 必需 |
| Base URL | `OPENAI_BASE_URL` | `ai.chatgpt.base_url` | `https://api.openai.com/v1` |
| Model | `OPENAI_MODEL` | `ai.chatgpt.model` | `gpt-3.5-turbo` |

**示例**：
```bash
export OPENAI_API_KEY="sk-your-key"
export OPENAI_BASE_URL="https://api.openai.com/v1"
export OPENAI_MODEL="gpt-4"
```

### Claude / Anthropic

| 参数 | 环境变量 | 配置文件字段 | 默认值 |
|------|----------|--------------|--------|
| API Key | `ANTHROPIC_API_KEY` | `ai.claude.api_key` | 必需 |
| Base URL | `ANTHROPIC_BASE_URL` | `ai.claude.base_url` | `https://api.anthropic.com/v1` |
| Model | `ANTHROPIC_MODEL` | `ai.claude.model` | `claude-3-5-sonnet-20241022` |

**示例**：
```bash
export ANTHROPIC_API_KEY="sk-ant-your-key"
export ANTHROPIC_BASE_URL="https://api.anthropic.com/v1"
export ANTHROPIC_MODEL="claude-3-opus-20240229"
```

### DeepSeek

| 参数 | 环境变量 | 配置文件字段 | 默认值 |
|------|----------|--------------|--------|
| API Key | `DEEPSEEK_API_KEY` | `ai.deepseek.api_key` | 必需 |
| Base URL | `DEEPSEEK_BASE_URL` | `ai.deepseek.base_url` | `https://api.deepseek.com/v1` |
| Model | `DEEPSEEK_MODEL` | `ai.deepseek.model` | `deepseek-chat` |

**示例**：
```bash
export DEEPSEEK_API_KEY="sk-your-key"
export DEEPSEEK_BASE_URL="https://api.deepseek.com/v1"
export DEEPSEEK_MODEL="deepseek-coder"
```

### Whisper STT

| 参数 | 环境变量 | 配置文件字段 | 默认值 |
|------|----------|--------------|--------|
| API Key | `OPENAI_API_KEY` | `stt.openai_key` | 必需 |
| Model | `WHISPER_MODEL` | `stt.model` | `whisper-1` |

**示例**：
```bash
export OPENAI_API_KEY="sk-your-key"
export WHISPER_MODEL="whisper-1"
```

---

## 🚀 使用场景

### 场景 1：使用官方 OpenAI 服务

```bash
# 最简配置
export OPENAI_API_KEY="sk-your-official-openai-key"
./start.sh
```

### 场景 2：使用国内 API 代理

```bash
# 使用国内代理服务
export OPENAI_API_KEY="fk-proxy-key"
export OPENAI_BASE_URL="https://api2d.openai.com/v1"
export OPENAI_MODEL="gpt-3.5-turbo"
./start.sh
```

### 场景 3：使用 OneAPI 聚合服务

```bash
# OneAPI 可能使用不同的模型名称
export OPENAI_API_KEY="sk-oneapi-generated-key"
export OPENAI_BASE_URL="https://oneapi.example.com/v1"
export OPENAI_MODEL="gpt-3.5-turbo"  # 或 OneAPI 中配置的别名
./start.sh
```

### 场景 4：使用私有部署的模型

```bash
# 使用 vLLM 部署的私有模型
export OPENAI_API_KEY="none"  # 私有服务可能不需要
export OPENAI_BASE_URL="http://localhost:8000/v1"
export OPENAI_MODEL="llama-2-13b-chat"  # 私有模型名称
./start.sh
```

### 场景 5：同时使用多个 AI 服务

```bash
# ChatGPT 使用代理
export OPENAI_API_KEY="fk-proxy-key"
export OPENAI_BASE_URL="https://proxy.com/v1"
export OPENAI_MODEL="gpt-3.5-turbo"

# Claude 使用官方服务
export ANTHROPIC_API_KEY="sk-ant-official-key"
export ANTHROPIC_MODEL="claude-3-5-sonnet-20241022"

# DeepSeek 使用官方服务
export DEEPSEEK_API_KEY="sk-deepseek-key"
export DEEPSEEK_MODEL="deepseek-chat"

./start.sh
```

---

## ⚙️ 配置文件方式

### config.yaml 完整示例

```yaml
server:
  port: 8080
  host: "0.0.0.0"

# STT 配置
stt:
  provider: "auto"
  openai_key: "${OPENAI_API_KEY}"
  model: "${WHISPER_MODEL:-whisper-1}"  # 支持环境变量，默认 whisper-1
  enable_fallback: true

# AI 配置
ai:
  default_provider: "chatgpt"
  
  chatgpt:
    api_key: "${OPENAI_API_KEY}"
    model: "${OPENAI_MODEL:-gpt-3.5-turbo}"  # 支持环境变量
    base_url: "${OPENAI_BASE_URL:-https://api.openai.com/v1}"
  
  claude:
    api_key: "${ANTHROPIC_API_KEY}"
    model: "${ANTHROPIC_MODEL:-claude-3-5-sonnet-20241022}"
    base_url: "${ANTHROPIC_BASE_URL:-https://api.anthropic.com/v1}"
  
  deepseek:
    api_key: "${DEEPSEEK_API_KEY}"
    model: "${DEEPSEEK_MODEL:-deepseek-chat}"
    base_url: "${DEEPSEEK_BASE_URL:-https://api.deepseek.com/v1}"

# 地图配置
map:
  default_provider: "baidu"
```

### 配置优先级

```
环境变量 > config.yaml 中的值 > 默认值
```

**示例**：
```yaml
# config.yaml
model: "${OPENAI_MODEL:-gpt-3.5-turbo}"
```

- 如果设置了 `OPENAI_MODEL="gpt-4"`，使用 `gpt-4`
- 如果未设置 `OPENAI_MODEL`，使用默认值 `gpt-3.5-turbo`

---

## 📊 常见模型名称参考

### OpenAI 系列

| 模型名称 | 说明 | 适用场景 |
|---------|------|----------|
| `gpt-3.5-turbo` | 最快、最便宜 | 日常使用 |
| `gpt-4` | 更智能 | 复杂任务 |
| `gpt-4-turbo` | GPT-4 加速版 | 需要速度的复杂任务 |
| `gpt-4o` | 最新多模态模型 | 最新功能 |

### Claude 系列

| 模型名称 | 说明 | 适用场景 |
|---------|------|----------|
| `claude-3-5-sonnet-20241022` | 最新 Sonnet | 推荐使用 |
| `claude-3-opus-20240229` | 最强大 | 极复杂任务 |
| `claude-3-haiku-20240307` | 最快 | 快速响应 |

### DeepSeek 系列

| 模型名称 | 说明 | 适用场景 |
|---------|------|----------|
| `deepseek-chat` | 通用聊天 | 日常对话 |
| `deepseek-coder` | 代码专用 | 编程任务 |

### 国产模型（通过第三方 API）

| 模型 | 可能的名称 |
|------|-----------|
| 通义千问 | `qwen-turbo`, `qwen-plus`, `qwen-max` |
| 智谱 GLM | `glm-4`, `glm-3-turbo` |
| 文心一言 | `ernie-bot`, `ernie-bot-turbo` |
| 讯飞星火 | `spark-v3`, `spark-v2` |

---

## 🔍 故障排查

### 问题 1：模型不存在错误

**错误信息**：
```
Error: model 'xxx' not found
```

**原因**：配置的模型名称在服务商不存在

**解决**：
1. 检查服务商支持的模型列表
2. 修改 `OPENAI_MODEL` 为正确的名称

```bash
# 查看可用模型（如果服务商支持）
curl https://your-api.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"

# 修改为正确的模型
export OPENAI_MODEL="correct-model-name"
```

### 问题 2：环境变量未生效

**症状**：设置了环境变量但系统仍使用默认值

**解决**：
```bash
# 确认环境变量已设置
echo $OPENAI_MODEL

# 重新设置并验证
export OPENAI_MODEL="gpt-4"
echo $OPENAI_MODEL

# 重启服务
./start.sh
```

### 问题 3：第三方服务模型名称不同

**场景**：OneAPI 中配置了自定义的模型别名

**解决**：
```bash
# OneAPI 配置示例
# 在 OneAPI 中：gpt-4 → 映射到 → azure-gpt-4

# qwall2 配置
export OPENAI_MODEL="gpt-4"  # 使用 OneAPI 中的别名
export OPENAI_BASE_URL="https://oneapi.example.com/v1"
```

---

## 💡 最佳实践

### 1. 使用 .env 文件管理环境变量

创建 `.env` 文件：
```bash
# .env
OPENAI_API_KEY=sk-your-key
OPENAI_BASE_URL=https://proxy.com/v1
OPENAI_MODEL=gpt-3.5-turbo

ANTHROPIC_API_KEY=sk-ant-key
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
```

加载并启动：
```bash
# 加载环境变量
set -a
source .env
set +a

# 启动服务
./start.sh
```

### 2. 不同环境使用不同配置

**开发环境**：
```bash
# dev.env
OPENAI_MODEL=gpt-3.5-turbo  # 使用便宜的模型
OPENAI_BASE_URL=https://proxy.com/v1  # 使用代理
```

**生产环境**：
```bash
# prod.env
OPENAI_MODEL=gpt-4  # 使用更好的模型
OPENAI_BASE_URL=https://api.openai.com/v1  # 使用官方服务
```

### 3. 安全管理 API Key

```bash
# 不要在代码中硬编码
# 不要提交到 Git

# .gitignore
*.env
.env.*
```

---

## 📚 相关文档

- [QUICKSTART.md](QUICKSTART.md) - 快速开始
- [THIRD_PARTY_API.md](THIRD_PARTY_API.md) - 第三方 API 详细配置
- [README.md](README.md) - 项目概览
- [config.yaml](config.yaml) - 配置文件示例

---

## 🎉 总结

qwall2 现在提供了完整的三参数配置体系：

1. **API Key** - 身份验证
2. **Base URL** - API 服务地址
3. **Model Name** - 具体模型名称

这三个参数的组合可以支持：
- ✅ 官方 OpenAI/Claude/DeepSeek 服务
- ✅ 国内 API 代理服务
- ✅ OneAPI 等聚合服务
- ✅ 私有部署的任何兼容模型

**灵活、强大、易用！** 🚀
