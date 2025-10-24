# 第三方 API 配置示例

本文档展示如何配置第三方兼容的 API 服务。

## 支持的第三方服务

qwall2 支持任何 OpenAI 兼容的 API 服务，包括：

- 🇨🇳 国内 API 代理服务
- 🔧 OneAPI 聚合服务
- 🏢 私有部署的模型服务
- 🌐 其他 OpenAI 兼容服务

---

## 配置方式

### 方式 1：环境变量（推荐）

```bash
# ChatGPT 使用第三方 API
export OPENAI_API_KEY="sk-your-key"
export OPENAI_BASE_URL="https://your-proxy.com/v1"

# Claude 使用第三方 API
export ANTHROPIC_API_KEY="sk-your-key"
export ANTHROPIC_BASE_URL="https://your-claude-proxy.com/v1"

# DeepSeek 使用第三方 API
export DEEPSEEK_API_KEY="sk-your-key"
export DEEPSEEK_BASE_URL="https://your-deepseek-proxy.com/v1"

# 启动服务
./start.sh
```

### 方式 2：修改 config.yaml

```yaml
ai:
  default_provider: "chatgpt"
  
  chatgpt:
    api_key: "sk-your-key"
    model: "gpt-3.5-turbo"
    base_url: "https://your-proxy.com/v1"  # 第三方 API 地址
  
  claude:
    api_key: "sk-your-key"
    model: "claude-3-5-sonnet-20241022"
    base_url: "https://your-claude-proxy.com/v1"
  
  deepseek:
    api_key: "sk-your-key"
    model: "deepseek-chat"
    base_url: "https://your-deepseek-proxy.com/v1"
```

---

## 常见第三方服务配置

### 1. 国内 API 代理服务

**示例服务商**：api2d、openai-sb、api-gpts 等

```bash
# 配置示例（请替换为实际的 API 地址和密钥）
export OPENAI_API_KEY="fk-xxxxx"  # 服务商提供的密钥
export OPENAI_BASE_URL="https://openai.api2d.net/v1"
```

**config.yaml**：
```yaml
ai:
  chatgpt:
    api_key: "fk-xxxxx"
    model: "gpt-3.5-turbo"
    base_url: "https://openai.api2d.net/v1"
```

### 2. OneAPI 聚合服务

**OneAPI** 是一个开源的 API 聚合网关，支持多种模型。

```bash
# 部署 OneAPI 后获取的配置
export OPENAI_API_KEY="sk-xxxxx"  # OneAPI 生成的密钥
export OPENAI_BASE_URL="https://your-oneapi-domain.com/v1"
```

**config.yaml**：
```yaml
ai:
  chatgpt:
    api_key: "sk-xxxxx"
    model: "gpt-3.5-turbo"
    base_url: "https://your-oneapi-domain.com/v1"
```

### 3. 私有部署模型服务

**场景**：使用 vLLM、FastChat、LocalAI 等部署的私有模型服务

```bash
# 私有服务器地址
export OPENAI_API_KEY="none"  # 如果不需要验证可设为任意值
export OPENAI_BASE_URL="http://your-private-server:8000/v1"
```

**config.yaml**：
```yaml
ai:
  chatgpt:
    api_key: "none"  # 私有服务可能不需要 key
    model: "your-custom-model"  # 私有模型名称
    base_url: "http://your-private-server:8000/v1"
```

### 4. Azure OpenAI

**Azure OpenAI** 需要特殊配置：

```bash
export OPENAI_API_KEY="your-azure-key"
export OPENAI_BASE_URL="https://your-resource.openai.azure.com/openai/deployments/your-deployment"
```

**注意**：Azure 的 API 路径与标准 OpenAI 不同，可能需要调整代码。

---

## 验证配置

### 测试连接

启动服务后，使用健康检查 API：

```bash
curl http://localhost:8080/api/health
```

**成功响应**：
```json
{
  "status": "ok",
  "stt": "Auto (OpenAI → Local)",
  "ai": ["chatgpt"]
}
```

### 测试导航

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

**成功响应**：
```json
{
  "success": true,
  "url": "https://map.baidu.com/...",
  "start": "北京",
  "end": "上海"
}
```

---

## 故障排查

### 问题 1：连接超时

**原因**：base_url 配置错误或网络不通

**解决**：
```bash
# 测试 API 地址是否可访问
curl https://your-proxy.com/v1/models

# 检查配置
echo $OPENAI_BASE_URL
```

### 问题 2：认证失败

**原因**：API Key 无效或格式不对

**解决**：
```bash
# 确认 API Key 是否正确
echo $OPENAI_API_KEY

# 重新设置
export OPENAI_API_KEY="正确的密钥"
```

### 问题 3：模型不存在

**原因**：第三方服务不支持指定的模型名称

**解决**：
修改 `config.yaml` 中的 `model` 字段为服务商支持的模型名称。

```yaml
ai:
  chatgpt:
    model: "gpt-3.5-turbo"  # 改为服务商支持的模型名
```

---

## 安全建议

### 1. 保护 API Key

```bash
# 不要在代码中硬编码 API Key
# 使用环境变量
export OPENAI_API_KEY="sk-..."

# 不要提交到 Git
echo "*.env" >> .gitignore
```

### 2. 使用 HTTPS

```yaml
ai:
  chatgpt:
    base_url: "https://..."  # 使用 HTTPS，不要使用 HTTP
```

### 3. 限制访问

如果是私有部署，建议：
- 设置防火墙规则
- 启用 API Key 验证
- 使用 VPN 或内网访问

---

## 性能优化

### 1. 选择就近服务

选择地理位置接近的 API 服务可以降低延迟：

```yaml
ai:
  chatgpt:
    base_url: "https://asia-openai-proxy.com/v1"  # 亚洲节点
```

### 2. 配置超时时间

在代码中可以调整超时时间（需要修改源代码）：

```go
client := &http.Client{
    Timeout: 30 * time.Second,  // 调整为合适的超时时间
}
```

---

## 示例配置文件

完整的第三方 API 配置示例：

```yaml
server:
  port: 8080
  host: "0.0.0.0"

stt:
  provider: "auto"
  openai_key: "${OPENAI_API_KEY}"
  model: "whisper-1"
  enable_fallback: true

ai:
  default_provider: "chatgpt"
  
  # 使用国内代理
  chatgpt:
    api_key: "${OPENAI_API_KEY}"
    model: "gpt-3.5-turbo"
    base_url: "https://api2d.openai.com/v1"
  
  # 使用 OneAPI
  claude:
    api_key: "${ONEAPI_KEY}"
    model: "claude-3-5-sonnet-20241022"
    base_url: "https://oneapi.example.com/v1"
  
  # 使用原生服务
  deepseek:
    api_key: "${DEEPSEEK_API_KEY}"
    model: "deepseek-chat"
    base_url: "https://api.deepseek.com/v1"

map:
  default_provider: "baidu"
```

---

## 常见服务商参考

| 服务商 | 类型 | base_url 示例 |
|--------|------|---------------|
| OpenAI 官方 | 原生 | `https://api.openai.com/v1` |
| api2d | 代理 | `https://openai.api2d.net/v1` |
| OneAPI | 聚合 | `https://your-domain/v1` |
| vLLM | 私有 | `http://localhost:8000/v1` |
| FastChat | 私有 | `http://localhost:8000/v1` |

---

## 总结

通过配置 `base_url` 参数，qwall2 可以灵活使用各种第三方 API 服务：

✅ **灵活性**：支持任何 OpenAI 兼容的 API  
✅ **便捷性**：国内用户可使用代理服务  
✅ **私有化**：支持企业内部部署  
✅ **成本优化**：选择性价比高的服务商  

**开始使用**：
1. 选择合适的第三方服务
2. 获取 API Key 和 base_url
3. 配置环境变量或 config.yaml
4. 启动服务并测试

如有问题，请查看 [QUICKSTART.md](QUICKSTART.md) 或提交 Issue。
