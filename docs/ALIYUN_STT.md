# 🎤 阿里云语音识别集成

## 📋 概述

qwall2 现在支持**阿里云实时语音识别**服务，提供高质量的在线语音识别功能，无需本地安装复杂依赖。

## 🚀 快速开始

### 1. 获取阿里云 API Key

1. 访问 [阿里云百炼平台](https://bailian.console.aliyun.com/)
2. 注册/登录阿里云账号
3. 开通语音识别服务
4. 获取 API Key

### 2. 配置环境变量

```bash
export ALIYUN_API_KEY="your_aliyun_api_key_here"
export ALIYUN_MODEL="paraformer-realtime-v2"  # 可选，默认值
```

### 3. 启动系统

```bash
./start.sh
```

### 4. 使用语音识别

访问 `http://localhost:8090`，切换到"语音输入"标签页，点击麦克风按钮开始录音。

## 🔧 支持的模型

根据[阿里云实时语音识别文档](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition)，支持以下模型：

### 推荐模型

| 模型 | 适用场景 | 支持语言 | 特点 |
|------|----------|----------|------|
| **paraformer-realtime-v2** | 长语音流式识别 | 中文 | 高准确率，支持标点符号 |
| **gummy-realtime-v1** | 多语言混合 | 中英日韩粤德法俄意西 | 多语言支持，低频词识别好 |
| **gummy-chat-v1** | 短语音交互 | 中文方言+多语言 | 情感识别，语气词过滤 |

### 模型选择建议

- **纯中文场景**: `paraformer-realtime-v2`
- **中英混合**: `gummy-realtime-v1` 或 `fun-asr-realtime`
- **中文方言**: `gummy-chat-v1`
- **多语言**: `gummy-realtime-v1`

## ⚙️ 配置选项

### 环境变量

```bash
# 必需
ALIYUN_API_KEY="your_api_key"

# 可选
ALIYUN_MODEL="paraformer-realtime-v2"  # 模型名称
```

### 配置文件 (config.yaml)

```yaml
stt:
  provider: "aliyun"                    # 使用阿里云
  aliyun_api_key: "${ALIYUN_API_KEY}"
  aliyun_model: "${ALIYUN_MODEL:-paraformer-realtime-v2}"
  enable_fallback: true                 # 启用降级
```

## 📊 功能特性

### ✅ 已实现

- [x] 实时语音识别
- [x] 多模型支持
- [x] 中文语音识别
- [x] 自动降级机制
- [x] 错误处理
- [x] 环境变量配置

### 🔄 降级策略

```
1. 阿里云语音识别 (如果 API Key 已配置)
   ↓ 失败
2. OpenAI Whisper (如果 API Key 已配置)
   ↓ 失败  
3. 本地 STT (whisper.cpp/vosk/qwen2-audio)
   ↓ 失败
4. 友好提示用户使用文字输入
```

## 🛠️ 故障排查

### 常见问题

**Q: 语音识别失败，提示 "阿里云 API Key 不能为空"**
```bash
# 检查环境变量
echo $ALIYUN_API_KEY

# 设置环境变量
export ALIYUN_API_KEY="your_api_key_here"
```

**Q: API 调用失败，状态码 401**
- 检查 API Key 是否正确
- 确认 API Key 有语音识别权限
- 检查账户余额是否充足

**Q: API 调用失败，状态码 429**
- 请求频率超限，请稍后重试
- 考虑使用不同的模型或调整请求频率

**Q: 识别结果为空**
- 检查音频质量
- 确认音频格式支持 (wav, mp3, pcm 等)
- 尝试使用不同的模型

### 性能优化

**音频质量优化**:
- 使用高质量麦克风
- 确保录音环境安静
- 采样率建议 16kHz
- 音频格式推荐 wav 或 pcm

**模型选择优化**:
- 纯中文: `paraformer-realtime-v2`
- 中英混合: `gummy-realtime-v1`
- 方言识别: `gummy-chat-v1`

## 📈 性能对比

| 方案 | 准确率 | 速度 | 成本 | 离线支持 | 多语言 |
|------|--------|------|------|----------|--------|
| 阿里云语音识别 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ❌ | ✅ |
| OpenAI Whisper | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ❌ | ✅ |
| Qwen2-Audio | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ | ⭐⭐ |
| whisper.cpp | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ | ✅ |

## 💰 费用说明

阿里云语音识别按调用次数计费，具体费用请参考：
- [阿里云语音识别定价](https://www.aliyun.com/price/product#/nls/detail)
- 建议先使用免费额度测试

## 🔮 未来计划

- [ ] 支持实时流式识别
- [ ] 支持更多音频格式
- [ ] 支持自定义热词
- [ ] 支持说话人分离
- [ ] 支持情感识别

## 📚 参考资源

- [阿里云实时语音识别文档](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition)
- [阿里云百炼平台](https://bailian.console.aliyun.com/)
- [DashScope API 文档](https://help.aliyun.com/zh/dashscope/)

---

**注意**: 阿里云语音识别是付费服务，使用前请确保账户有足够余额。
