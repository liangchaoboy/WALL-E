# QWall2 - AI 驱动的地图导航系统 (Go 版本)

基于 MCP (Model Context Protocol) 的智能地图导航系统，支持通过文字或语音指令自动打开百度地图或高德地图并进入导航状态。

## ✨ 功能特性

- 🗣️ **自然语言输入**：支持文字和语音输入（如："从北京到上海导航"）
- 🗺️ **多地图支持**：兼容百度地图和高德地图
- 🤖 **AI 智能解析**：自动提取起点和终点信息
- 🔌 **MCP 协议**：标准化的工具调用接口
- 🖥️ **跨平台**：支持 macOS、Windows、Linux
- ⚡ **高性能**：使用 Go 语言实现，启动快速，资源占用低

## 🚀 快速开始

### 前置要求

- Go 1.21 或更高版本
- Git

### 安装依赖

```bash
go mod download
```

### 编译项目

```bash
go build -o qwall2-mcp
```

### 运行 MCP 服务器

```bash
./qwall2-mcp
```

或直接运行：

```bash
go run main.go
```

## 📋 使用方法

### 1. 作为 MCP 服务器使用

在你的 MCP 客户端配置中添加（例如 Claude Desktop 的配置）：

**macOS/Linux:**
```json
{
  "mcpServers": {
    "map-navigation": {
      "command": "/path/to/qwall2/qwall2-mcp"
    }
  }
}
```

**Windows:**
```json
{
  "mcpServers": {
    "map-navigation": {
      "command": "C:\\path\\to\\qwall2\\qwall2-mcp.exe"
    }
  }
}
```

### 2. 可用工具

#### `navigate_map`

打开地图应用并开始导航。

**参数：**
- `start` (string): 起点地址或地点名称
- `end` (string): 终点地址或地点名称
- `mapProvider` (string, 可选): 地图提供商，支持 "baidu"（百度地图）或 "amap"（高德地图），默认为 "baidu"

**示例：**
```json
{
  "start": "北京天安门",
  "end": "上海东方明珠",
  "mapProvider": "baidu"
}
```

#### `parse_navigation_intent`

从自然语言中提取导航意图（起点和终点）。

**参数：**
- `text` (string): 用户输入的自然语言文本

**示例：**
```json
{
  "text": "帮我从北京七牛云到上海七牛云"
}
```

## 🛠️ 技术架构

```
用户输入（文字/语音）
    ↓
自然语言解析（提取起点/终点）
    ↓
MCP 工具调用
    ↓
生成地图 URL
    ↓
打开浏览器/地图应用
    ↓
进入导航状态
```

## 📦 项目结构

```
qwall2/
├── main.go                   # MCP 服务器入口
├── pkg/
│   ├── navigation/
│   │   └── navigation.go     # 地图导航工具
│   ├── parser/
│   │   └── parser.go         # 自然语言解析
│   └── mapprovider/
│       └── provider.go       # 地图提供商配置
├── go.mod
├── go.sum
└── README.md
```

## 🌐 支持的地图服务

### 百度地图
- Web 端：https://map.baidu.com
- 支持起终点导航
- URL 格式：`?origin=起点&destination=终点`

### 高德地图
- Web 端：https://www.amap.com
- 支持起终点导航
- URL 格式：`/dir?from=起点&to=终点`

## 🔧 环境变量配置

可以通过环境变量配置：

- `DEFAULT_MAP_PROVIDER`: 默认地图提供商（baidu 或 amap）
- `MCP_SERVER_NAME`: MCP 服务器名称（默认：map-navigation-mcp）

## 📝 示例对话

**用户：** "帮我从北京天安门到上海东方明珠导航"

**AI 处理流程：** 
1. 调用 `parse_navigation_intent` 解析文本
   - 提取起点：北京天安门
   - 提取终点：上海东方明珠
2. 调用 `navigate_map` 工具
   - 生成百度地图导航 URL
   - 在默认浏览器中打开
3. 返回成功消息

## 🧪 测试

运行测试：

```bash
go test ./...
```

运行带覆盖率的测试：

```bash
go test -cover ./...
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 📚 相关链接

- [MCP Protocol](https://modelcontextprotocol.io/)
- [mcp-go SDK](https://github.com/mark3labs/mcp-go)
- [百度地图 Web API](https://lbsyun.baidu.com/)
- [高德地图 Web API](https://lbs.amap.com/)
