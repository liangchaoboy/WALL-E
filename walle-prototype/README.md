# WALL-E 语音导航原型

1天快速开发版本,仅实现核心功能。

## 快速开始

1. 安装依赖:
   ```bash
   pip install -r requirements.txt
   ```

2. 配置 API Key:
   ```bash
   cp .env.example .env
   # 编辑 .env 填入你的 API Key、BASE_URL 和 MODEL
   # 支持 OpenAI、DeepSeek 等任意兼容 OpenAI 接口的服务
   ```

3. 运行:
   ```bash
   python voice_nav.py
   ```

4. 使用:
   - 对着麦克风说导航指令
   - 例如: "从上海到北京"
   - 说"退出"结束程序

## 系统要求

- Python 3.8+
- 麦克风
- 联网
- macOS/Linux/Windows

## 已知问题

- 需要第三方大模型 API (有成本)
- 语音识别需要网络
- 没有唤醒词
- 只能导航,不支持其他功能

## 功能清单

- ✅ 语音输入 (使用 Google 语音识别)
- ✅ AI 理解 (使用 ChatGPT 或兼容的第三方 API)
- ✅ 地图导航 (打开百度地图)
- ✅ 命令行交互
- ✅ 基本错误处理

## Demo 场景

```
$ python voice_nav.py
==================================================
🤖 WALL-E 语音导航原型
说话即可导航,说'退出'结束
==================================================

🎤 请说话...
📝 识别: 从上海七牛云到虹桥机场
🤖 AI: {'action': 'nav', 'from': '上海七牛云', 'to': '虹桥机场'}
🗺️  已打开: 上海七牛云 → 虹桥机场

🎤 请说话...
📝 识别: 退出
👋 再见!
```

## 配置说明

支持任意兼容 OpenAI API 格式的第三方大模型服务:

- `BASE_URL`: 第三方 API 接口地址
  - OpenAI: `https://api.openai.com/v1`
  - DeepSeek: `https://api.deepseek.com/v1`
  - 其他兼容服务的对应地址
- `API_KEY`: 对应的 API 密钥
- `MODEL`: 使用的模型名称 (如: `gpt-3.5-turbo`, `deepseek-chat`, 等)
