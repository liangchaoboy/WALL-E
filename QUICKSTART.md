# 🚀 快速启动指南

## 5 分钟快速上手

### 步骤 1: 安装依赖

```bash
cd /Users/sanmu/eva/qwall2
go mod download
```

### 步骤 2: 编译项目

选择以下任意一种方式：

**方式 A: 使用 Makefile（推荐）**
```bash
make build
```

**方式 B: 使用构建脚本**
```bash
# macOS/Linux
chmod +x build.sh
./build.sh

# Windows
build.bat
```

**方式 C: 直接使用 Go**
```bash
go build -o qwall2-mcp main.go
```

### 步骤 3: 测试运行

```bash
# 运行测试确保一切正常
make test

# 或
go test ./...
```

### 步骤 4: 配置 Claude Desktop

1. 获取可执行文件的完整路径：
   ```bash
   pwd
   # 输出示例：/Users/sanmu/eva/qwall2
   ```

2. 编辑 Claude Desktop 配置文件：
   
   **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
   
   添加以下内容：
   ```json
   {
     "mcpServers": {
       "map-navigation": {
         "command": "/Users/sanmu/eva/qwall2/qwall2-mcp"
       }
     }
   }
   ```

3. 重启 Claude Desktop

### 步骤 5: 开始使用！

在 Claude Desktop 中尝试以下命令：

```
帮我从北京天安门到上海东方明珠导航
```

---

## 📚 完整文档

- **[README.md](README.md)** - 项目概述
- **[USAGE.md](USAGE.md)** - 详细使用指南
- **[API.md](API.md)** - API 文档
- **[EXAMPLES.md](EXAMPLES.md)** - 使用示例
- **[CLAUDE_CONFIG.md](CLAUDE_CONFIG.md)** - Claude Desktop 配置详解

---

## 🛠️ 常用命令

```bash
# 编译
make build

# 运行测试
make test

# 查看测试覆盖率
make coverage

# 代码格式化
make fmt

# 代码检查
make vet

# 清理构建文件
make clean

# 查看所有命令
make help
```

---

## ✨ 核心功能

### 1. 智能解析自然语言

支持多种表达方式：
- "从北京到上海"
- "帮我去杭州西湖"
- "北京到上海导航"

### 2. 多地图支持

- 🔵 **百度地图**（默认）
- 🟢 **高德地图**

### 3. 自动打开浏览器

一键打开地图应用，进入导航状态

---

## 🎯 使用示例

### 基础用法

```
用户: 从北京到上海
AI: [自动调用导航工具，打开地图]
```

### 指定地图

```
用户: 用高德地图从上海到杭州
AI: [使用高德地图导航]
```

### 只有终点

```
用户: 去杭州西湖
AI: 请问您的出发地是哪里？
```

---

## ❓ 故障排除

### 编译失败

```bash
# 确保 Go 版本 >= 1.21
go version

# 清理并重新下载依赖
go clean -modcache
go mod download
go mod tidy
```

### 无法运行

```bash
# macOS/Linux: 添加执行权限
chmod +x qwall2-mcp

# 查看是否有错误
./qwall2-mcp
```

### Claude Desktop 无法识别

1. 检查配置文件路径是否正确
2. 确认 JSON 格式正确（可以用 JSON 验证工具）
3. 完全重启 Claude Desktop
4. 查看 Claude Desktop 日志文件

---

## 🎓 进阶使用

### 环境变量配置

```json
{
  "mcpServers": {
    "map-navigation": {
      "command": "/Users/sanmu/eva/qwall2/qwall2-mcp",
      "env": {
        "DEFAULT_MAP_PROVIDER": "amap"
      }
    }
  }
}
```

### 直接运行（开发模式）

```bash
go run main.go
```

### 调试模式

```bash
# 查看详细日志
MCP_LOG_LEVEL=debug ./qwall2-mcp
```

---

## 📞 获取帮助

遇到问题？查看：

1. [USAGE.md](USAGE.md) - 详细使用说明
2. [EXAMPLES.md](EXAMPLES.md) - 更多示例
3. [API.md](API.md) - API 文档
4. [GitHub Issues](https://github.com/sanmu/qwall2/issues) - 提交问题

---

## 🎉 开始使用吧！

现在你已经准备好使用 QWall2 地图导航 MCP 服务器了！

试试向 Claude 说：
- "帮我从北京到上海导航"
- "去杭州西湖怎么走"
- "用高德地图从上海到苏州"

享受智能导航的便捷体验！🗺️
