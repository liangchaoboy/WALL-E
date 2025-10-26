# WALL-E: AI 驱动的桌面操作系统代理

> 让 AI 操作你的电脑 - 基于 MCP 协议的智能桌面助手

---

## 📚 项目文档

本项目正在进行全面重构，聚焦于构建一个 AI 驱动的桌面操作系统代理。

**重要文档**:
- **[PROJECT_PROGRESS.md](./PROJECT_PROGRESS.md)** - 📊 项目进度说明 (已完成阶段一、二)
- **[PRD.md](./PRD.md)** - 完整的产品需求文档

---

## 🎯 项目愿景

打造一个智能的桌面操作代理系统，让用户通过自然语言（文字/语音）与计算机交互，实现各类日常操作的自动化。

### 核心特性

- 🎤 **语音控制**：通过"小七小七"唤醒词，语音控制电脑
- ⌨️ **文字输入**：桌面输入界面，支持快捷键唤醒
- 🧠 **智能理解**：基于 AI 的自然语言理解，无需记忆命令
- 🔌 **可扩展**：基于 MCP (Model Context Protocol) 插件化架构
- 🗺️ **多场景支持**：地图导航、天气查询、音乐播放、系统控制等

---

### 核心用例

#### 场景 1：地图导航
```
用户："小七小七，打开地图导航，从上海七牛云到虹桥机场"
系统：自动打开地图应用并进入导航状态
```

#### 场景 2：天气查询
```
用户："小七小七，查看明天上海的天气"
系统：展示上海明天的天气信息
```

#### 场景 3：音乐播放
```
用户："小七小七，播放周杰伦的晴天"
系统：打开音乐应用并播放指定歌曲
```

#### 场景 4：系统控制
```
用户："小七小七，音量调到50%"
系统：调整系统音量到50%
```

---

## 🏗️ 技术架构

### 核心技术栈

- **客户端**：Swift + SwiftUI (macOS 原生)
- **后端服务**：Go
- **AI 引擎**：ChatGPT / Claude / DeepSeek
- **语音识别**：阿里云 / OpenAI Whisper / 本地模型
- **工具协议**：MCP (Model Context Protocol)

### 系统架构

```
用户交互层 (语音/文字)
    ↓
核心处理层 (STT → AI理解 → MCP Client)
    ↓
MCP工具层 (地图/天气/音乐/浏览器/系统控制)
    ↓
系统能力层 (macOS API / 第三方服务)
```

---

## 📅 项目进度

项目采用分阶段实施策略:

- ✅ **阶段一: 基础原型** ([walle-prototype](./walle-prototype/)) - Python + MCP 概念验证 **已完成**
- ✅ **阶段二: 进阶实现** ([walle-prototype-vue](./walle-prototype-vue/)) - Vue + Go + FastGPT **已完成**
- 🔄 **阶段三: 桌面应用** - macOS 原生应用 **规划中**

**🎥 阶段二演示视频**: [观看演示](https://ticket-imgs.qnssl.com/fast-map-mcp2025-10-26%2020.12.47.mp4)

详细进度请查看 [PROJECT_PROGRESS.md](./PROJECT_PROGRESS.md)

---

## 📖 文档导航

### 项目文档
- **[PROJECT_PROGRESS.md](./PROJECT_PROGRESS.md)** - 📊 项目进度说明
- **[PRD.md](./PRD.md)** - 完整的产品需求文档
- **[CLAUDE.md](./CLAUDE.md)** - Claude AI 项目说明

### 阶段一: 基础原型 (Python)
- **目录**: [walle-prototype/](./walle-prototype/)
- **文档**: [README](./walle-prototype/README.md) | [MCP架构](./walle-prototype/README_MCP.md) | [测试文档](./walle-prototype/README_TESTS.md)
- **状态**: ✅ 已完成
- **技术**: Python + OpenAI API + MCP
- **功能**: 地图导航、天气查询、音乐播放

### 阶段二: 进阶实现 (Vue + Go)
- **目录**: [walle-prototype-vue/](./walle-prototype-vue/)
- **文档**: [README](./walle-prototype-vue/ReadMe.md) | [架构设计](./walle-prototype-vue/docs/架构设计文档.md)
- **演示**: [观看视频](https://ticket-imgs.qnssl.com/fast-map-mcp2025-10-26%2020.12.47.mp4)
- **状态**: ✅ 已完成
- **技术**: Vue.js 3 + Go + FastGPT + QWen + MCP
- **架构**: 前后端分离 + 云端 AI
- **功能**: 实时语音识别、智能对话、地图导航

### 阶段三: 桌面应用 (规划)
- **状态**: 🔄 规划中
- **技术**: Swift + SwiftUI + Go
- **目标**: macOS 原生应用 + 唤醒词检测

---

## 🤝 参与贡献

本项目正在积极开发中，欢迎参与贡献！

### 参与方式

1. 查看 [Issue #16](../../issues/16) 了解项目重构进展
2. 阅读 [PRD.md](./PRD.md) 了解详细需求
3. 提交 Issue 报告问题或建议
4. 提交 PR 贡献代码

---

## 📞 联系方式

- **Issue 讨论**：[GitHub Issues](../../issues)
- **项目主页**：[liangchaoboy/WALL-E](https://github.com/liangchaoboy/WALL-E)

---

## 📄 许可证

待定

---

**让 AI 成为你的桌面助手，从此告别繁琐的电脑操作！** ✨
