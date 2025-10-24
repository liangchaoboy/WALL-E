# 🎤 Qwen2-Audio 语音识别集成

## 📋 概述

qwall2 现在集成了 **Qwen2-Audio** 语音识别模型，提供高质量的本地语音识别功能，无需依赖外部 API 服务。

## 🚀 快速开始

### 1. 安装依赖

运行安装脚本：

```bash
./install_qwen2_audio.sh
```

### 2. 启动系统

```bash
./start.sh
```

### 3. 使用语音识别

访问 `http://localhost:8090`，切换到"语音输入"标签页，点击麦克风按钮开始录音。

## 🔧 技术细节

### 支持的模型

- **Qwen2-Audio-1.5B**: 轻量级模型，约 3GB，适合大多数设备
- **自动降级**: whisper.cpp → vosk → Qwen2-Audio → 友好提示

### 系统要求

- **Python 3.7+**
- **PyTorch** (CPU 或 GPU 版本)
- **Transformers** 库
- **Librosa** 音频处理库
- **至少 4GB 内存** (推荐 8GB+)

### 性能优化

- **GPU 加速**: 自动检测 CUDA，GPU 模式下性能更好
- **模型缓存**: 首次下载后模型缓存在本地
- **轻量级**: 使用 1.5B 参数模型，平衡性能和资源消耗

## 📊 功能特性

### ✅ 已实现

- [x] 自动模型下载和缓存
- [x] CPU/GPU 自动检测
- [x] 中文语音识别
- [x] 错误处理和降级
- [x] 临时文件管理
- [x] 多格式音频支持

### 🔄 降级策略

```
1. whisper.cpp (如果已安装)
   ↓ 失败
2. vosk (如果已安装)  
   ↓ 失败
3. Qwen2-Audio (如果依赖已安装)
   ↓ 失败
4. 友好提示用户使用文字输入
```

## 🛠️ 故障排查

### 常见问题

**Q: 语音识别失败，提示 "Python 未安装"**
```bash
# macOS
brew install python3

# Ubuntu/Debian
sudo apt install python3 python3-pip
```

**Q: 模型下载失败**
```bash
# 检查网络连接
ping huggingface.co

# 手动下载模型
python3 -c "from transformers import AutoModelForSpeechSeq2Seq; AutoModelForSpeechSeq2Seq.from_pretrained('Qwen/Qwen2-Audio-1.5B')"
```

**Q: 内存不足**
- 确保至少有 4GB 可用内存
- 关闭其他占用内存的应用程序
- 考虑使用更小的模型

**Q: GPU 不可用**
- 检查 CUDA 安装: `nvidia-smi`
- 安装 GPU 版本 PyTorch: `pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118`

### 性能调优

**CPU 模式优化**:
```python
# 在脚本中调整参数
torch_dtype = torch.float32  # 使用 float32 提高兼容性
max_new_tokens = 128         # 减少生成长度
```

**GPU 模式优化**:
```python
# 在脚本中调整参数  
torch_dtype = torch.float16  # 使用 float16 节省显存
device_map = "auto"         # 自动分配 GPU 内存
```

## 📈 性能对比

| 方案 | 准确率 | 速度 | 资源消耗 | 离线支持 |
|------|--------|------|----------|----------|
| OpenAI Whisper API | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ❌ |
| Qwen2-Audio-1.5B | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ✅ |
| whisper.cpp | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ |
| vosk | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ |

## 🔮 未来计划

- [ ] 支持更多语言
- [ ] 实时语音识别
- [ ] 模型量化优化
- [ ] 云端模型服务
- [ ] 语音命令识别

## 📚 参考资源

- [Qwen2-Audio 官方文档](https://huggingface.co/Qwen/Qwen2-Audio-1.5B)
- [Transformers 库文档](https://huggingface.co/docs/transformers)
- [PyTorch 安装指南](https://pytorch.org/get-started/locally/)

---

**注意**: Qwen2-Audio 是阿里云通义千问团队开发的开源语音识别模型，具有优秀的性能和中文支持。
