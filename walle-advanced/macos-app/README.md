# WALL-E macOS Application

macOS 原生桌面语音助手应用,基于 Swift + SwiftUI 构建。

## 功能特性

### 已实现 ✅

#### 任务组 A: macOS 应用框架
- ✅ A1: Xcode 项目初始化
  - Swift macOS App 项目结构
  - 最低系统要求: macOS 13.0+
  - SwiftUI 生命周期配置

- ✅ A2: 系统托盘界面
  - Menu Bar 图标集成
  - 下拉菜单(打开输入面板/设置/退出)
  - 点击托盘图标显示/隐藏输入窗口

- ✅ A3: 输入窗口 UI
  - 悬浮输入窗口(半透明、毛玻璃效果)
  - 文字输入框组件
  - "开始语音"按钮
  - 识别结果显示区域
  - 录音波形动画

- ✅ A4: 全局快捷键
  - Cmd+Space 全局快捷键监听
  - 快捷键触发显示输入窗口

- ✅ A5: 权限申请
  - 麦克风访问权限请求(Info.plist)
  - 辅助功能权限请求
  - 权限检查和引导流程

- ✅ A6: gRPC 客户端通信
  - gRPC 客户端接口定义
  - 与 Go 核心服务的连接框架
  - 错误处理机制

#### 任务组 B: 语音输入模块
- ✅ B1: Porcupine 唤醒词集成框架
  - 唤醒词检测接口("小七小七")
  - 唤醒词检测回调
  - 灵敏度参数配置

- ✅ B2: 音频采集
  - AVFoundation 麦克风音频采集
  - 音频格式配置(16kHz, 单声道, PCM)
  - 音频流缓冲管理
  - 音频设备切换处理

- ✅ B3: VAD (语音活动检测)
  - 实时语音活动检测实现
  - 静音阈值和检测窗口配置
  - 自动判断用户说话结束(静音 1.5 秒后)

- ✅ B4: 录音控制
  - "点击说话"模式实现
  - 录音状态 UI 反馈(动画、波形显示)
  - 录音文件临时存储

- ✅ B5: 与 Go 服务交互框架
  - 录音音频发送到 Go 核心服务(gRPC 接口)
  - 接收 STT 识别结果
  - 识别文字显示到输入框
  - 错误处理(网络异常、识别失败等)

## 技术栈

- **语言**: Swift 5.9+
- **UI 框架**: SwiftUI
- **唤醒词引擎**: Porcupine (框架已集成,需 API Key)
- **音频采集**: AVFoundation
- **VAD**: 自定义实现(基于音频振幅检测)
- **通信协议**: gRPC (Swift Client)

## 项目结构

```
macos-app/
├── WALLE.xcodeproj/          # Xcode 项目配置
├── Package.swift              # Swift Package Manager 配置
├── WALLE/
│   ├── App/
│   │   ├── WALLEApp.swift           # 应用入口
│   │   └── AppDelegate.swift        # 系统托盘和全局快捷键
│   ├── Views/
│   │   ├── InputWindowView.swift    # 输入窗口
│   │   ├── MenuBarView.swift        # 系统托盘菜单
│   │   └── SettingsView.swift       # 设置界面
│   ├── Services/
│   │   ├── WakeWordDetector.swift   # 唤醒词检测
│   │   ├── AudioRecorder.swift      # 音频采集
│   │   ├── VADDetector.swift        # 语音活动检测
│   │   └── GRPCClient.swift         # gRPC 客户端
│   ├── Models/
│   │   └── AudioConfig.swift        # 音频配置模型
│   └── Resources/
│       ├── Assets.xcassets/         # 图标资源
│       ├── Info.plist               # 权限配置
│       └── WALLE.entitlements       # App 权限声明
└── README.md                  # 本文件
```

## 环境要求

- macOS 13.0 或更高版本
- Xcode 15.0 或更高版本
- Swift 5.9 或更高版本

## 快速开始

### 1. 安装依赖

```bash
cd macos-app
swift package resolve
```

### 2. 打开 Xcode 项目

```bash
open WALLE.xcodeproj
```

### 3. 配置 Porcupine API Key

在 Xcode 中,找到 `WakeWordDetector.swift`,替换 Porcupine API Key:

```swift
// 需要在 https://picovoice.ai/ 注册获取免费 API Key
let porcupineAccessKey = "YOUR_API_KEY_HERE"
```

### 4. 配置 gRPC 服务器地址

在设置中配置 Go 核心服务的地址(默认: `localhost:50051`)

### 5. 编译和运行

在 Xcode 中按 `Cmd+R` 编译运行。

## 使用说明

### 唤醒应用

1. **唤醒词**: 说 "小七小七" (需要配置 Porcupine API Key)
2. **全局快捷键**: 按 `Cmd+Space`
3. **系统托盘**: 点击托盘图标

### 语音输入

1. 点击"开始语音"按钮
2. 开始说话,录音指示灯会亮起
3. 停止说话后,VAD 会自动检测静音并停止录音(1.5秒静音)
4. 等待语音识别结果显示

### 文字输入

1. 在输入框中直接输入命令
2. 按 `Enter` 或点击"发送"按钮提交

## 配置

### 权限设置

首次运行时,应用会请求以下权限:

1. **麦克风权限**: 用于语音录音和唤醒词检测
2. **辅助功能权限**: 用于全局快捷键(Cmd+Space)监听

### 应用设置

在设置面板中可配置:

- **通用设置**
  - gRPC 服务器地址
  - 唤醒后是否自动开始录音

- **语音设置**
  - 唤醒词灵敏度(0.0 - 1.0)
  - VAD 静音检测阈值(0.0 - 1.0)

## 开发说明

### 核心组件

#### 1. WakeWordDetector
负责唤醒词"小七小七"的检测。

**当前实现**: 基于音频振幅的简单检测(示例实现)  
**生产实现**: 需要集成 Porcupine SDK

#### 2. AudioRecorder
负责麦克风音频采集和录音。

- 采样率: 16kHz
- 声道: 单声道
- 格式: PCM Int16

#### 3. VADDetector
语音活动检测,自动判断用户说话结束。

- 静音阈值: 可配置(默认 0.01)
- 静音持续时间: 可配置(默认 1.5秒)

#### 4. GRPCClient
与 Go 核心服务通信。

- STT 请求: 发送音频数据,接收识别文本
- 命令请求: 发送文本命令,接收执行结果

### 扩展开发

#### 添加新的 UI 组件
在 `Views/` 目录下创建新的 SwiftUI 视图文件。

#### 添加新的服务
在 `Services/` 目录下创建新的服务类。

#### 集成真实的 Porcupine SDK

1. 安装 Porcupine CocoaPods:
```bash
pod init
# 编辑 Podfile,添加:
# pod 'Porcupine-iOS'
pod install
```

2. 替换 `WakeWordDetector.swift` 中的检测逻辑

## 测试

### 功能测试

- [x] 系统托盘图标正常显示
- [x] 点击托盘可弹出输入窗口
- [x] Cmd+Space 快捷键可唤起窗口
- [x] 文字输入框可正常输入
- [x] 麦克风权限申请流程完整
- [x] 语音录音功能正常
- [x] VAD 自动停止录音

### 待完成测试

- [ ] 唤醒词检测(需要 Porcupine API Key)
- [ ] gRPC 与 Go 服务通信(需要启动 Go 核心服务)
- [ ] 端到端语音识别流程

## 已知问题

1. **唤醒词检测**: 当前使用简单的音频振幅检测作为示例,需要集成真实的 Porcupine SDK
2. **gRPC 通信**: 当前为模拟实现,需要实际的 protobuf 定义和 gRPC 代码生成
3. **快捷键冲突**: Cmd+Space 可能与 Spotlight 冲突,可在设置中更改

## 下一步计划

- [ ] 集成真实的 Porcupine SDK
- [ ] 实现完整的 gRPC protobuf 定义
- [ ] 添加单元测试和 UI 测试
- [ ] 性能优化(内存占用、CPU 使用率)
- [ ] 添加日志系统
- [ ] 支持多语言(国际化)

## 相关文档

- [PRD - 产品需求文档](../../PRD.md)
- [架构设计文档](../../docs/架构设计文档.md)
- [Issue #52 - 任务详情](https://github.com/liangchaoboy/WALL-E/issues/52)

## 许可证

待定

---

**让 AI 成为你的桌面助手!** ✨
