# QWall2 运行示例

本文档提供完整的运行示例和演示。

---

## 🚀 快速运行

### 1. 编译项目

```bash
cd /Users/sanmu/eva/qwall2

# 方式 1: 使用 Makefile
make build

# 方式 2: 使用 Go 命令
go build -o qwall2-mcp main.go

# 方式 3: 使用构建脚本
./build.sh  # macOS/Linux
# 或
build.bat   # Windows
```

**预期输出：**
```
🔨 开始编译 qwall2-mcp...
📦 下载依赖...
⚙️  编译中...
✅ 编译成功！
📍 可执行文件：/Users/sanmu/eva/qwall2/qwall2-mcp
```

### 2. 验证编译结果

```bash
ls -lh qwall2-mcp
```

**预期输出：**
```
-rwxr-xr-x  1 user  staff   6.6M Oct 24 13:24 qwall2-mcp
```

### 3. 直接运行服务器

```bash
./qwall2-mcp
```

**预期输出：**
```
2025/10/24 13:24:00 🚀 MCP 地图导航服务器已启动
2025/10/24 13:24:00 📍 支持的地图：百度地图、高德地图
2025/10/24 13:24:00 🔧 可用工具：navigate_map, parse_navigation_intent
```

服务器现在正在运行，等待通过 stdio 接收 MCP 请求。

---

## 🧪 测试运行

### 运行所有测试

```bash
# 运行所有测试
go test ./... -v

# 只运行特定包的测试
go test ./pkg/parser -v
go test ./pkg/mapprovider -v

# 查看测试覆盖率
go test ./... -cover

# 生成覆盖率报告
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out
```

**预期输出：**
```
=== RUN   TestParseNavigationIntent
=== RUN   TestParseNavigationIntent/从A到B格式
=== RUN   TestParseNavigationIntent/从A去B格式
=== RUN   TestParseNavigationIntent/帮我从A到B格式
=== RUN   TestParseNavigationIntent/去B格式
=== RUN   TestParseNavigationIntent/到B导航格式
=== RUN   TestParseNavigationIntent/A到B导航格式
=== RUN   TestParseNavigationIntent/空字符串
=== RUN   TestParseNavigationIntent/无效输入
--- PASS: TestParseNavigationIntent (0.00s)
    --- PASS: TestParseNavigationIntent/从A到B格式 (0.00s)
    --- PASS: TestParseNavigationIntent/从A去B格式 (0.00s)
    --- PASS: TestParseNavigationIntent/帮我从A到B格式 (0.00s)
    --- PASS: TestParseNavigationIntent/去B格式 (0.00s)
    --- PASS: TestParseNavigationIntent/到B导航格式 (0.00s)
    --- PASS: TestParseNavigationIntent/A到B导航格式 (0.00s)
    --- PASS: TestParseNavigationIntent/空字符串 (0.00s)
    --- PASS: TestParseNavigationIntent/无效输入 (0.00s)
PASS
ok  	github.com/sanmu/qwall2/pkg/parser	0.976s
```

---

## 🎯 与 Claude Desktop 集成运行

### 步骤 1: 配置 Claude Desktop

编辑配置文件：

**macOS:**
```bash
code ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**添加配置：**
```json
{
  "mcpServers": {
    "map-navigation": {
      "command": "/Users/sanmu/eva/qwall2/qwall2-mcp"
    }
  }
}
```

### 步骤 2: 重启 Claude Desktop

完全退出并重新启动 Claude Desktop。

### 步骤 3: 测试对话

在 Claude Desktop 中尝试以下对话：

#### 示例 1: 基础导航

**用户输入：**
```
从北京到上海
```

**Claude 响应：**
```
我来帮您规划从北京到上海的路线。

[调用 parse_navigation_intent 工具]
🔍 导航意图解析结果：

起点：北京
终点：上海
置信度：90%

✅ 起点和终点已成功识别
💡 建议：可以使用 navigate_map 工具开始导航

[调用 navigate_map 工具]
✅ 成功打开 百度地图

📍 起点：北京
📍 终点：上海
🔗 导航链接：https://map.baidu.com/?da_src=shareurl&origin=北京&destination=上海&output=html&da_mode=transit

地图应用已在浏览器中打开，正在准备导航...
```

**浏览器效果：**
- 自动打开百度地图
- 显示从北京到上海的路线
- 可以选择不同的出行方式

#### 示例 2: 详细地点导航

**用户输入：**
```
帮我从北京天安门到上海东方明珠导航
```

**Claude 响应：**
```
好的，我来帮您规划从北京天安门到上海东方明珠的路线。

[自动解析并调用工具]

✅ 成功打开 百度地图

📍 起点：北京天安门
📍 终点：上海东方明珠
🔗 导航链接：https://map.baidu.com/?da_src=shareurl&origin=北京天安门&destination=上海东方明珠&output=html&da_mode=transit

地图已在浏览器中打开，您可以查看详细的导航路线。
```

#### 示例 3: 指定地图提供商

**用户输入：**
```
用高德地图从上海到杭州
```

**Claude 响应：**
```
好的，我用高德地图帮您规划从上海到杭州的路线。

[调用 navigate_map，使用 amap 参数]

✅ 成功打开 高德地图

📍 起点：上海
📍 终点：杭州
🔗 导航链接：https://www.amap.com/dir?from=上海&to=杭州

高德地图已在浏览器中打开。
```

#### 示例 4: 只有终点

**用户输入：**
```
去杭州西湖
```

**Claude 响应：**
```
我检测到您想去杭州西湖。

[调用 parse_navigation_intent]

⚠️ 只识别到终点，起点未指定
💡 建议：请补充起点信息，或使用当前位置作为起点

请问您的出发地是哪里呢？
```

**用户继续：**
```
从上海出发
```

**Claude 响应：**
```
好的，我来帮您规划从上海到杭州西湖的路线。

[调用 navigate_map]

✅ 成功打开 百度地图

📍 起点：上海
📍 终点：杭州西湖
🔗 导航链接：https://map.baidu.com/...

地图已打开，祝您旅途愉快！
```

---

## 🔧 开发模式运行

### 使用 go run 直接运行

```bash
go run main.go
```

**适用场景：**
- 开发调试
- 快速测试
- 不需要编译

### 使用 Makefile 运行

```bash
# 运行服务器
make run

# 运行测试
make test

# 查看覆盖率
make coverage

# 代码格式化
make fmt

# 代码检查
make vet

# 清理构建文件
make clean
```

---

## 📊 监控和日志

### 查看运行日志

服务器启动后会输出日志到 stderr：

```bash
./qwall2-mcp 2>&1 | tee server.log
```

**日志示例：**
```
2025/10/24 13:24:00 🚀 MCP 地图导航服务器已启动
2025/10/24 13:24:00 📍 支持的地图：百度地图、高德地图
2025/10/24 13:24:00 🔧 可用工具：navigate_map, parse_navigation_intent
```

### 调试模式

设置环境变量启用详细日志：

```bash
export MCP_LOG_LEVEL=debug
./qwall2-mcp
```

---

## 🎬 完整演示脚本

### 场景：商务出差导航

```bash
# 1. 编译项目
make build

# 2. 配置 Claude Desktop
# （手动编辑配置文件）

# 3. 启动 Claude Desktop

# 4. 在 Claude 中对话：
```

**对话流程：**

```
👤 用户: 明天要去上海浦东新区开会，从北京出发

🤖 Claude: 好的，我来帮您查看从北京到上海浦东新区的路线。

[调用工具]

✅ 成功打开 百度地图

📍 起点：北京
📍 终点：上海浦东新区
🔗 导航链接：https://map.baidu.com/...

根据地图显示，有以下出行方式供您选择：
- 高铁：约 4.5-5.5 小时
- 飞机：约 2-3 小时（不含往返机场时间）
- 自驾：约 12-14 小时

建议您选择高铁或飞机出行，更加便捷。

---

👤 用户: 用高德地图看看

🤖 Claude: 好的，我用高德地图重新帮您查看。

[调用 navigate_map，mapProvider: "amap"]

✅ 成功打开 高德地图

📍 起点：北京
📍 终点：上海浦东新区

高德地图已打开，您可以对比两个地图的路线规划。
```

---

## 🧩 模块测试示例

### 测试自然语言解析

```bash
cd /Users/sanmu/eva/qwall2
go test -v -run TestParseNavigationIntent ./pkg/parser
```

**测试各种输入：**
- "从北京到上海" ✅
- "从天安门去东方明珠" ✅
- "帮我从北京七牛云到上海七牛云" ✅
- "去杭州西湖" ✅
- "到上海浦东机场导航" ✅
- "北京到上海导航" ✅

### 测试地图 URL 生成

```bash
go test -v -run TestGenerateNavigationURL ./pkg/mapprovider
```

**验证生成的 URL：**
- 百度地图 URL ✅
- 高德地图 URL ✅
- 参数编码正确 ✅
- 错误处理完善 ✅

---

## 🔍 故障排查

### 问题 1: 服务器无法启动

**症状：**
```bash
./qwall2-mcp
-bash: ./qwall2-mcp: Permission denied
```

**解决方案：**
```bash
chmod +x qwall2-mcp
./qwall2-mcp
```

### 问题 2: 编译失败

**症状：**
```
go build: cannot find package
```

**解决方案：**
```bash
go mod tidy
go mod download
go build -o qwall2-mcp main.go
```

### 问题 3: Claude Desktop 无法识别

**检查步骤：**

1. 验证配置文件路径：
```bash
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

2. 验证可执行文件路径：
```bash
which qwall2-mcp
# 或
ls -la /Users/sanmu/eva/qwall2/qwall2-mcp
```

3. 测试手动运行：
```bash
/Users/sanmu/eva/qwall2/qwall2-mcp
```

4. 查看 Claude Desktop 日志：
```bash
tail -f ~/Library/Logs/Claude/mcp*.log
```

### 问题 4: 浏览器没有打开

**可能原因：**
- 系统没有默认浏览器
- 权限问题

**解决方案：**
```bash
# 手动复制 URL 到浏览器
# URL 会在响应中显示
```

---

## 📈 性能测试

### 启动时间测试

```bash
time ./qwall2-mcp &
# 预期：< 100ms
```

### 内存占用测试

```bash
ps aux | grep qwall2-mcp
# 预期：< 20MB
```

### 响应时间测试

通过 Claude Desktop 调用工具，观察响应时间：
- 解析意图：< 100ms
- 打开地图：< 500ms

---

## 🎓 高级用例

### 用例 1: 批量导航规划

```
👤 用户: 帮我规划一个行程：
1. 从北京到上海
2. 从上海到杭州
3. 从杭州到苏州

🤖 Claude: 好的，我来帮您逐一规划路线。

[依次调用 navigate_map 三次]

✅ 第一段：北京 → 上海 已打开
✅ 第二段：上海 → 杭州 已打开
✅ 第三段：杭州 → 苏州 已打开

所有路线已在地图中打开，您可以查看详细信息。
```

### 用例 2: 对比不同地图

```
👤 用户: 同时用百度和高德看看北京到上海的路线

🤖 Claude: 好的，我用两个地图分别帮您查看。

[调用 navigate_map，mapProvider: "baidu"]
✅ 百度地图已打开

[调用 navigate_map，mapProvider: "amap"]
✅ 高德地图已打开

两个地图都已打开，您可以对比路线规划。
```

---

## 📝 运行检查清单

在正式使用前，请确认：

- [x] Go 版本 >= 1.23.0
- [x] 项目已编译成功
- [x] 可执行文件有执行权限
- [x] Claude Desktop 配置正确
- [x] Claude Desktop 已重启
- [x] 测试对话成功
- [x] 浏览器能正常打开
- [x] 地图显示正常

---

## 🎉 成功运行的标志

当您看到以下效果时，说明系统运行成功：

1. ✅ 服务器启动日志显示
2. ✅ Claude Desktop 能识别工具
3. ✅ 对话时能正确解析意图
4. ✅ 浏览器自动打开地图
5. ✅ 地图显示正确的导航路线

---

## 📞 获取帮助

如遇问题，请查看：

1. [`USAGE.md`](USAGE.md) - 详细使用指南
2. [`CLAUDE_CONFIG.md`](CLAUDE_CONFIG.md) - Claude 配置
3. [`CODE_REVIEW_REPORT.md`](CODE_REVIEW_REPORT.md) - 代码审查报告
4. [`EXAMPLES.md`](EXAMPLES.md) - 更多示例

---

**祝您使用愉快！** 🎊
