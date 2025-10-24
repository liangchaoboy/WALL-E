# 使用指南

## 快速开始

### 1. 编译项目

```bash
# 下载依赖
go mod download

# 编译
go build -o qwall2-mcp

# 或者直接运行
go run main.go
```

### 2. 配置 MCP 客户端

#### Claude Desktop 配置

编辑配置文件：

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

添加以下配置：

```json
{
  "mcpServers": {
    "map-navigation": {
      "command": "/path/to/qwall2/qwall2-mcp"
    }
  }
}
```

重启 Claude Desktop 后即可使用。

### 3. 使用示例

#### 示例 1: 直接指定起点和终点

**用户输入：**
```
帮我从北京天安门到上海东方明珠导航
```

**AI 处理：**
1. AI 调用 `parse_navigation_intent` 工具解析文本
2. 提取到：起点=北京天安门，终点=上海东方明珠
3. AI 调用 `navigate_map` 工具
4. 系统打开百度地图并进入导航状态

#### 示例 2: 只指定终点

**用户输入：**
```
去杭州西湖
```

**AI 处理：**
1. AI 调用 `parse_navigation_intent` 工具
2. 提取到：终点=杭州西湖，起点未指定
3. AI 询问用户起点或建议使用当前位置

#### 示例 3: 指定地图提供商

**用户输入：**
```
用高德地图从上海到杭州导航
```

**AI 处理：**
1. 解析出起点、终点和地图偏好
2. 调用 `navigate_map`，设置 `mapProvider: "amap"`
3. 打开高德地图导航

## 工具详解

### navigate_map

打开地图应用并开始导航。

**参数：**

| 参数名 | 类型 | 必需 | 说明 | 示例 |
|--------|------|------|------|------|
| start | string | 是 | 起点地址 | "北京天安门" |
| end | string | 是 | 终点地址 | "上海东方明珠" |
| mapProvider | string | 否 | 地图提供商 | "baidu" 或 "amap" |

**返回值：**

成功时返回导航信息，包括：
- 使用的地图提供商
- 起点和终点
- 导航链接
- 状态消息

**错误处理：**

- 起点或终点为空：返回错误提示
- 不支持的地图提供商：返回错误提示
- 浏览器打开失败：返回错误信息

### parse_navigation_intent

从自然语言中提取导航意图。

**参数：**

| 参数名 | 类型 | 必需 | 说明 | 示例 |
|--------|------|------|------|------|
| text | string | 是 | 用户输入文本 | "从北京到上海" |

**返回值：**

返回解析结果，包括：
- 起点（可能为空）
- 终点（可能为空）
- 置信度（0-1）
- 建议的后续操作

**支持的表达方式：**

- "从A到B"
- "从A去B"
- "A到B导航"
- "帮我从A到B"
- "去B"
- "到B"
- "前往B"

## 高级配置

### 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| DEFAULT_MAP_PROVIDER | 默认地图提供商 | baidu |
| MCP_SERVER_NAME | MCP 服务器名称 | map-navigation-mcp |

### 自定义地图提供商

如需添加其他地图服务（如谷歌地图、腾讯地图等），可编辑 `pkg/mapprovider/provider.go` 文件：

1. 添加新的 `MapProvider` 常量
2. 实现 URL 生成函数
3. 在 `GenerateNavigationURL` 中添加对应的 case

## 故障排除

### 问题 1: 浏览器没有打开

**可能原因：**
- 系统没有默认浏览器
- 浏览器设置了安全限制

**解决方案：**
- 检查系统默认浏览器设置
- 尝试手动复制 URL 到浏览器

### 问题 2: 解析不到起点终点

**可能原因：**
- 输入格式不符合预期
- 地名使用了不常见的表达

**解决方案：**
- 使用"从A到B"的标准格式
- 直接调用 `navigate_map` 工具并明确指定参数

### 问题 3: 地图显示不正确

**可能原因：**
- 地点名称不准确
- 地图服务暂时不可用

**解决方案：**
- 使用更具体的地址（如包含城市名）
- 尝试切换其他地图提供商

## 开发说明

### 项目结构

```
qwall2/
├── main.go                    # MCP 服务器入口
├── pkg/
│   ├── navigation/
│   │   └── navigation.go      # 导航功能实现
│   ├── parser/
│   │   └── parser.go          # 自然语言解析
│   └── mapprovider/
│       └── provider.go        # 地图提供商
├── go.mod                     # Go 模块定义
├── go.sum                     # 依赖锁定
└── README.md                  # 项目说明
```

### 运行测试

```bash
# 运行所有测试
go test ./...

# 查看测试覆盖率
go test -cover ./...

# 生成覆盖率报告
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out
```

### 调试模式

```bash
# 启用详细日志
MCP_LOG_LEVEL=debug ./qwall2-mcp

# 或者在代码中设置
export MCP_LOG_LEVEL=debug
go run main.go
```

## 贡献指南

欢迎提交 Issue 和 Pull Request！

### 提交 PR 前请确保：

1. 代码通过 `go fmt` 格式化
2. 通过 `go vet` 检查
3. 所有测试通过
4. 添加了必要的测试用例
5. 更新了相关文档

### 代码风格

- 遵循 Go 官方代码规范
- 使用有意义的变量和函数名
- 添加必要的注释
- 保持函数简洁（建议不超过 50 行）
