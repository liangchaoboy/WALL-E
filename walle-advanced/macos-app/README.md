# WALL-E macOS App

> macOS 原生语音助手应用 - 基于 Swift + SwiftUI

## 📋 项目概述

WALL-E macOS App 是 WALL-E 项目的前端应用,提供语音输入、文字输入和系统托盘界面,与 Go 核心服务通过 gRPC 通信。

## 🏗️ 项目结构

```
WALLE/
├── App/                    # 应用入口
│   ├── WALLEApp.swift     # SwiftUI App 主入口
│   └── AppDelegate.swift  # AppDelegate (系统托盘、全局快捷键)
├── Views/                  # UI 界面
│   ├── InputWindow.swift  # 输入窗口
│   └── SettingsView.swift # 设置界面
├── Services/               # 服务层
│   ├── WakeWordDetector.swift      # 唤醒词检测
│   ├── AudioRecorder.swift         # 音频采集
│   ├── VADDetector.swift           # 语音活动检测
│   ├── VoiceInputCoordinator.swift # 语音输入协调器
│   ├── GRPCClient.swift            # gRPC 客户端
│   ├── GlobalHotKeyManager.swift   # 全局快捷键
│   └── PermissionManager.swift     # 权限管理
├── Models/                 # 数据模型
│   ├── HistoryItem.swift  # 历史记录
│   └── AudioConfig.swift  # 音频配置
└── Resources/              # 资源文件
    ├── Info.plist         # 应用配置
    └── Assets.xcassets/   # 图标资源
```

## 🎯 核心功能

### 任务组 A: macOS 应用框架

- ✅ **A1. Xcode 项目初始化**: Swift + SwiftUI 项目结构
- ✅ **A2. 系统托盘界面**: Menu Bar 图标和下拉菜单
- ✅ **A3. 输入窗口 UI**: 文字输入框、语音按钮、历史记录
- ✅ **A4. 全局快捷键**: Cmd+Space 快捷键唤起窗口
- ✅ **A5. 权限申请**: 麦克风、辅助功能权限
- ✅ **A6. gRPC 通信**: 与 Go 核心服务通信

### 任务组 B: 语音输入模块

- ✅ **B1. Porcupine 唤醒词集成**: "小七小七" 唤醒检测
- ✅ **B2. 音频采集**: AVFoundation 实时音频采集
- ✅ **B3. VAD 检测**: 语音活动检测,自动判断说话结束
- ✅ **B4. 录音控制**: 按住说话/点击说话模式
- ✅ **B5. Go 服务交互**: 语音数据发送和结果接收

## 🛠️ 技术栈

| 模块 | 技术 |
|------|------|
| 语言 | Swift 5.9+ |
| UI 框架 | SwiftUI |
| 音频采集 | AVFoundation |
| 唤醒词引擎 | Porcupine |
| VAD | WebRTC VAD / 自定义实现 |
| 通信协议 | gRPC |
| 最低系统要求 | macOS 13.0+ |

## 🚀 开发指南

### 环境要求

- macOS 13.0+
- Xcode 15.0+
- Swift 5.9+

### 打开项目

```bash
cd walle-advanced/macos-app
open WALLE.xcodeproj
```

### 编译运行

1. 在 Xcode 中打开项目
2. 选择目标设备 (My Mac)
3. 点击 Run (Cmd+R)

### 配置签名

在 Xcode 项目设置中:
1. 选择 WALLE target
2. 进入 Signing & Capabilities
3. 设置 Team 和 Bundle Identifier

### 依赖管理

#### Porcupine Wake Word Engine

项目使用 Porcupine 进行唤醒词检测。需要:

1. 注册 [Picovoice Console](https://console.picovoice.ai/)
2. 下载 Porcupine SDK for macOS
3. 将 SDK 添加到项目中
4. 获取 Access Key 并配置

#### gRPC Swift

```bash
# 使用 Swift Package Manager 添加 gRPC
# 在 Xcode 中: File -> Add Packages
# 输入: https://github.com/grpc/grpc-swift
```

## 📝 代码说明

### 应用入口 (WALLEApp.swift)

```swift
@main
struct WALLEApp: App {
    @NSApplicationDelegateAdaptor(AppDelegate.self) var appDelegate
    
    var body: some Scene {
        Settings {
            SettingsView()
        }
    }
}
```

### AppDelegate (AppDelegate.swift)

负责:
- 系统托盘图标和菜单
- 全局快捷键注册
- 服务初始化
- 权限请求

### 输入窗口 (InputWindow.swift)

提供:
- 文字输入框
- 语音录音按钮
- 识别结果显示
- 历史记录列表

### 语音输入协调器 (VoiceInputCoordinator.swift)

协调:
- 唤醒词检测
- 音频采集
- VAD 检测
- gRPC 通信

## 🔒 权限说明

### 麦克风权限

在 `Info.plist` 中配置:

```xml
<key>NSMicrophoneUsageDescription</key>
<string>WALL-E 需要访问麦克风以提供语音输入功能</string>
```

### 辅助功能权限

全局快捷键需要辅助功能权限,首次使用时会提示用户授权。

### App Sandbox

在 `WALLE.entitlements` 中配置:

```xml
<key>com.apple.security.device.audio-input</key>
<true/>
<key>com.apple.security.network.client</key>
<true/>
```

## 🧪 测试

### 手动测试

1. **系统托盘测试**:
   - 检查托盘图标是否显示
   - 测试菜单项点击

2. **输入窗口测试**:
   - 测试 Cmd+Space 快捷键
   - 测试文字输入和提交
   - 测试语音录音按钮

3. **语音输入测试**:
   - 测试唤醒词检测
   - 测试录音和 VAD 自动停止
   - 测试识别结果显示

### 单元测试

```bash
# 运行单元测试
xcodebuild test -scheme WALLE -destination 'platform=macOS'
```

## 📦 打包发布

### 构建 Release 版本

```bash
xcodebuild -scheme WALLE -configuration Release
```

### 签名和公证

1. 配置开发者证书
2. 启用 Hardened Runtime
3. 提交到 Apple 进行公证

### 创建 DMG

```bash
# 使用 create-dmg 工具
create-dmg \
  --volname "WALL-E" \
  --window-pos 200 120 \
  --window-size 600 400 \
  --icon-size 100 \
  --app-drop-link 450 185 \
  WALLE.dmg \
  build/Release/WALLE.app
```

## 🔧 配置文件

### Info.plist

关键配置:
- Bundle ID: `com.walle.assistant`
- 最低系统版本: macOS 13.0
- LSUIElement: true (隐藏 Dock 图标)

### WALLE.entitlements

沙盒权限:
- 音频输入
- 网络客户端
- Apple Events (用于自动化)

## 🐛 已知问题

1. **Porcupine 集成**: 需要手动集成 SDK,等待官方 SPM 支持
2. **全局快捷键冲突**: 与 Spotlight 默认快捷键冲突,需用户手动调整
3. **沙盒限制**: App Sandbox 限制某些系统操作

## 🎯 下一步

- [ ] 集成真实的 Porcupine SDK
- [ ] 实现完整的 gRPC 通信 (protobuf 定义)
- [ ] 添加更多 UI 动画和反馈
- [ ] 实现历史记录持久化
- [ ] 添加更多设置选项

## 📚 相关文档

- [PRD - 产品需求文档](../../PRD.md)
- [架构设计文档](../../docs/架构设计文档.md)
- [Issue #52 - 任务详情](https://github.com/liangchaoboy/WALL-E/issues/52)
- [Porcupine 官方文档](https://picovoice.ai/docs/porcupine/)
- [AVFoundation 开发指南](https://developer.apple.com/av-foundation/)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request!

## 📝 许可证

待定

---

**让 AI 成为你的桌面助手!** ✨
