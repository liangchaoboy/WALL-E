# 📚 QWall2 文档索引

> AI 地图导航系统完整文档

## 🚀 快速开始

- [**快速入门**](QUICKSTART.md) - 5分钟快速上手，必读！
- [**功能演示**](DEMO.md) - 完整功能展示和截图

## 🏗️ 技术文档

- [**系统架构**](ARCHITECTURE.md) - 技术架构详解
- [**第三方 API 配置**](THIRD_PARTY_API.md) - AI 和地图 API 设置
- [**项目状态**](STATUS.md) - 开发进度和计划

## 📖 使用指南

### 基础功能

1. **语音识别** - Chrome 浏览器原生语音识别
2. **AI 处理** - 多 AI 提供商支持
3. **地图导航** - 多地图提供商支持

### 配置选项

- **AI 提供商**: Mock、Claude、ChatGPT、DeepSeek
- **地图提供商**: 百度地图、高德地图、Google Maps
- **语音识别**: Chrome Web Speech API

## 🔧 开发文档

### 项目结构

```
qwall2/
├── docs/           # 文档目录
├── internal/       # 核心模块
├── web/           # Web 前端
├── pkg/           # 公共包
└── config.yaml    # 配置文件
```

### 核心模块

- `internal/ai/` - AI 处理模块
- `internal/server/` - HTTP 服务器
- `internal/config/` - 配置管理
- `internal/stt/` - 语音识别
- `pkg/mapprovider/` - 地图提供商
- `pkg/navigation/` - 导航逻辑

## 📞 支持

如有问题，请查看：

1. [快速入门](QUICKSTART.md) - 常见问题解答
2. [项目状态](STATUS.md) - 已知问题和计划
3. GitHub Issues - 提交问题报告

---

**💡 建议阅读顺序：快速入门 → 功能演示 → 系统架构**