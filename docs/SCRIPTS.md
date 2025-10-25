# 📜 脚本使用说明

> qwall2 项目的所有脚本说明和使用指南

---

## 📚 目录

- [启动脚本](#启动脚本)
- [测试脚本](#测试脚本)
- [安装脚本](#安装脚本)
- [构建工具](#构建工具)

---

## 🚀 启动脚本

### start.sh

**功能**: 主启动脚本，用于启动 qwall2 Web 服务器

**使用方法**:
```bash
./start.sh
```

**功能说明**:
1. 检查所需的环境变量（API Keys）
2. 编译 Go 项目生成 `qwall2-server`
3. 启动 Web 服务器（默认端口 8090）

**环境变量检查**:
- `OPENAI_API_KEY` - OpenAI API（用于 ChatGPT 和 Whisper）
- `ANTHROPIC_API_KEY` - Claude API
- `DEEPSEEK_API_KEY` - DeepSeek API
- `ALIYUN_API_KEY` - 阿里云语音识别 API

**示例**:
```bash
# 基础启动（仅 OpenAI）
export OPENAI_API_KEY="sk-your-key"
./start.sh

# 完整配置（所有 AI 服务）
export OPENAI_API_KEY="sk-your-openai-key"
export ANTHROPIC_API_KEY="sk-ant-your-claude-key"
export DEEPSEEK_API_KEY="sk-your-deepseek-key"
export ALIYUN_API_KEY="your-aliyun-key"
./start.sh
```

**访问地址**: http://localhost:8090

---

### test_aliyun_stt.sh

**功能**: 阿里云语音识别测试脚本

**使用方法**:
```bash
./test_aliyun_stt.sh
```

**功能说明**:
1. 检查 `ALIYUN_API_KEY` 环境变量
2. 设置默认模型（如未设置）
3. 调用 `start.sh` 启动服务器

**必需环境变量**:
- `ALIYUN_API_KEY` - 阿里云 API Key（必需）

**可选环境变量**:
- `ALIYUN_MODEL` - 阿里云模型名称（默认: `paraformer-realtime-v2`）

**示例**:
```bash
# 使用默认模型
export ALIYUN_API_KEY="your-aliyun-key"
./test_aliyun_stt.sh

# 自定义模型
export ALIYUN_API_KEY="your-aliyun-key"
export ALIYUN_MODEL="paraformer-realtime-v2"
./test_aliyun_stt.sh
```

**获取 API Key**:
1. 访问 https://bailian.console.aliyun.com/
2. 注册/登录阿里云账号
3. 开通语音识别服务
4. 获取 API Key

---

## 🧪 测试脚本

### test.sh

**功能**: 系统自动化测试脚本

**使用方法**:
```bash
./test.sh
```

**前置条件**: 服务器必须正在运行（先执行 `./start.sh`）

**测试内容**:
1. ✅ 服务器状态检查
2. ✅ 健康检查 API (`/api/health`)
3. ✅ 文字导航 API (`/api/navigate`)
4. ✅ 主页访问测试
5. ✅ 静态文件访问测试（CSS、JS）

**示例**:
```bash
# 终端 1: 启动服务器
./start.sh

# 终端 2: 运行测试
./test.sh
```

**测试输出**:
```
🧪 qwall2 系统测试
=======================

1️⃣  检查服务器状态...
✅ 服务器正在运行

2️⃣  测试健康检查 API...
✅ 健康检查通过

3️⃣  测试文字导航 API...
✅ 文字导航测试通过

4️⃣  测试主页...
✅ 主页访问正常

5️⃣  测试静态文件...
✅ CSS 文件访问正常
✅ JS 文件访问正常

=======================
✅ 所有基础测试通过！
```

**注意事项**:
- 如果未配置真实的 API Key，AI 功能测试会失败（但不影响其他测试）
- 建议在正式使用前运行此脚本验证系统功能

---

## 📦 安装脚本

### install_qwen2_audio.sh

**功能**: Qwen2-Audio 语音识别依赖安装脚本

**使用方法**:
```bash
./install_qwen2_audio.sh
```

**功能说明**:
1. 检查 Python3 和 pip3 是否安装
2. 安装 PyTorch（CPU 版本）
3. 安装 Transformers、Librosa 等依赖

**前置条件**:
- Python 3.x
- pip3

**安装的依赖**:
- `torch` - PyTorch 框架
- `transformers` - Hugging Face Transformers
- `librosa` - 音频处理库
- `soundfile` - 音频文件读写
- `accelerate` - 模型加速

**安装 Python3** (如未安装):
```bash
# macOS
brew install python3

# Ubuntu/Debian
sudo apt install python3 python3-pip
```

**使用说明**:
1. 首次使用时会自动下载 Qwen2-Audio-1.5B 模型（约 3GB）
2. 模型会缓存在 `~/.cache/huggingface/` 目录
3. 支持 CPU 和 GPU 运行，GPU 性能更好
4. 语音识别需要一定的计算资源

---

## 🔧 构建工具

### Makefile

**功能**: 项目构建和管理工具

**使用方法**:
```bash
make [target]
```

**可用命令**:

| 命令 | 说明 | 示例 |
|------|------|------|
| `make build` | 编译项目生成 `qwall2-server` | `make build` |
| `make run` | 编译并直接运行服务器 | `make run` |
| `make server` | 使用 `start.sh` 启动（推荐） | `make server` |
| `make test` | 运行 Go 单元测试 | `make test` |
| `make coverage` | 生成测试覆盖率报告 | `make coverage` |
| `make clean` | 清理构建文件 | `make clean` |
| `make deps` | 安装 Go 依赖 | `make deps` |
| `make fmt` | 格式化 Go 代码 | `make fmt` |
| `make vet` | Go 代码静态检查 | `make vet` |
| `make install` | 安装到系统 | `make install` |
| `make help` | 显示帮助信息 | `make help` |

**常用示例**:
```bash
# 编译项目
make build

# 启动服务器（推荐方式）
make server

# 运行测试
make test

# 生成测试覆盖率报告
make coverage

# 清理构建文件
make clean

# 代码格式化和检查
make fmt
make vet
```

**开发工作流**:
```bash
# 1. 安装依赖
make deps

# 2. 格式化代码
make fmt

# 3. 静态检查
make vet

# 4. 运行测试
make test

# 5. 编译和启动
make server
```

---

### build.bat

**功能**: Windows 平台编译脚本

**使用方法**:
```cmd
build.bat
```

**功能说明**:
- 在 Windows 环境下编译 Go 项目
- 生成 `qwall2-server.exe`

**Windows 启动**:
```cmd
# 1. 设置环境变量
set OPENAI_API_KEY=sk-your-key

# 2. 编译
build.bat

# 3. 运行
qwall2-server.exe
```

---

## 📝 配置文件

### config.yaml

**功能**: 主配置文件

**说明**: 
- 配置服务器端口、AI 服务、STT 服务等
- 支持环境变量占位符（如 `${OPENAI_API_KEY}`）
- 不要将包含真实 API Key 的配置文件提交到 Git

**配置示例**: 参考 `config.yaml.example`

**使用方法**:
```bash
# 复制示例配置
cp config.yaml.example config.yaml

# 编辑配置文件
vim config.yaml

# 或者直接使用环境变量（推荐）
export OPENAI_API_KEY="sk-your-key"
./start.sh
```

---

## 🔗 相关文档

- 📖 [快速开始指南](QUICKSTART.md) - 新手入门
- 🏛️ [系统架构详解](ARCHITECTURE.md) - 技术架构
- 🌐 [第三方 API 配置](THIRD_PARTY_API.md) - API 配置说明
- 📚 [文档索引](DOCS.md) - 所有文档导航

---

## ❓ 常见问题

### 1. 脚本没有执行权限

```bash
# 添加执行权限
chmod +x start.sh test.sh test_aliyun_stt.sh install_qwen2_audio.sh
```

### 2. 端口被占用

```bash
# 修改 config.yaml 中的端口
server:
  port: 8091  # 修改为其他端口
```

### 3. API Key 未生效

```bash
# 检查环境变量
echo $OPENAI_API_KEY

# 重新设置并启动
export OPENAI_API_KEY="sk-your-key"
./start.sh
```

### 4. 编译失败

```bash
# 检查 Go 版本（需要 1.23.0+）
go version

# 重新安装依赖
make deps

# 清理后重新编译
make clean
make build
```

---

**完成时间**: 2025-10-25  
**维护者**: qwall2 团队
