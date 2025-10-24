# Claude Desktop 配置示例

这是在 Claude Desktop 中配置 qwall2-mcp 服务器的示例。

## macOS 配置

配置文件位置: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "map-navigation": {
      "command": "/Users/YOUR_USERNAME/eva/qwall2/qwall2-mcp"
    }
  }
}
```

**注意**: 请将 `/Users/YOUR_USERNAME/eva/qwall2/qwall2-mcp` 替换为实际的完整路径。

## Windows 配置

配置文件位置: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "map-navigation": {
      "command": "C:\\Users\\YOUR_USERNAME\\eva\\qwall2\\qwall2-mcp.exe"
    }
  }
}
```

**注意**: 
- Windows 路径需要使用双反斜杠 `\\`
- 请将路径替换为实际的完整路径

## Linux 配置

配置文件位置: `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "map-navigation": {
      "command": "/home/YOUR_USERNAME/eva/qwall2/qwall2-mcp"
    }
  }
}
```

## 配置步骤

1. **编译项目**

   ```bash
   cd /path/to/qwall2
   go build -o qwall2-mcp main.go
   ```

2. **获取完整路径**

   在项目目录中运行：
   
   ```bash
   # macOS/Linux
   pwd
   
   # Windows (PowerShell)
   (Get-Location).Path
   ```

3. **编辑配置文件**

   打开 Claude Desktop 配置文件，添加上述配置（使用实际路径）

4. **重启 Claude Desktop**

   完全退出并重新启动 Claude Desktop

5. **验证配置**

   在 Claude Desktop 中尝试发送以下消息：
   
   ```
   帮我从北京天安门到上海东方明珠导航
   ```

   如果配置成功，Claude 将自动调用地图导航工具。

## 多服务器配置示例

如果你有多个 MCP 服务器，可以这样配置：

```json
{
  "mcpServers": {
    "map-navigation": {
      "command": "/path/to/qwall2/qwall2-mcp"
    },
    "other-server": {
      "command": "/path/to/other/server"
    }
  }
}
```

## 故障排除

### 服务器无法启动

1. 检查可执行文件路径是否正确
2. 确认文件有执行权限（macOS/Linux）：
   ```bash
   chmod +x qwall2-mcp
   ```
3. 尝试在终端直接运行，查看错误信息：
   ```bash
   ./qwall2-mcp
   ```

### Claude 无法识别工具

1. 确认已完全重启 Claude Desktop
2. 检查配置文件 JSON 格式是否正确
3. 查看 Claude Desktop 的日志文件

### 日志文件位置

- **macOS**: `~/Library/Logs/Claude/`
- **Windows**: `%APPDATA%\Claude\logs\`
- **Linux**: `~/.config/Claude/logs/`

## 环境变量配置（可选）

如果需要自定义配置，可以在启动命令中添加环境变量：

```json
{
  "mcpServers": {
    "map-navigation": {
      "command": "/path/to/qwall2/qwall2-mcp",
      "env": {
        "DEFAULT_MAP_PROVIDER": "amap",
        "MCP_LOG_LEVEL": "debug"
      }
    }
  }
}
```
