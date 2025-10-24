# Claude Desktop 配置完整指南

本文档提供 Claude Desktop MCP 配置的详细步骤和问题解决方案。

---

## ✅ 已完成！配置文件已创建

配置文件位置：
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

配置内容：
```json
{
  "mcpServers": {
    "map-navigation": {
      "command": "/Users/sanmu/eva/qwall2/qwall2-mcp"
    }
  }
}
```

---

## 🚀 下一步操作

### 1. 验证配置文件

```bash
# 查看配置文件
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json

# 检查 JSON 格式是否正确
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json | python3 -m json.tool
```

### 2. 验证可执行文件

```bash
# 检查文件是否存在
ls -lh /Users/sanmu/eva/qwall2/qwall2-mcp

# 检查执行权限
ls -l /Users/sanmu/eva/qwall2/qwall2-mcp | grep "x"

# 如果没有执行权限，添加：
chmod +x /Users/sanmu/eva/qwall2/qwall2-mcp

# 测试运行（Ctrl+C 退出）
/Users/sanmu/eva/qwall2/qwall2-mcp
```

### 3. 重启 Claude Desktop

**重要！必须完全重启：**

1. **完全退出 Claude Desktop**
   - macOS: `Command + Q` （完全退出）
   - 或右键 Dock 图标 → 退出

2. **重新打开 Claude Desktop**
   - 从应用程序文件夹打开
   - 或使用 Spotlight 搜索

3. **等待启动完成**
   - 看到主界面后再开始使用

### 4. 测试 MCP 工具

在 Claude Desktop 中输入：

```
从北京到上海
```

**预期效果：**
- Claude 自动调用 MCP 工具
- 解析导航意图
- 打开浏览器显示地图

---

## 🔍 验证是否成功

### 方法 1: 查看 Claude 响应

如果配置成功，Claude 会：
1. 理解你的导航意图
2. 调用 `parse_navigation_intent` 工具
3. 调用 `navigate_map` 工具
4. 在浏览器中打开地图

### 方法 2: 查看日志

```bash
# 查看 Claude Desktop 日志
tail -f ~/Library/Logs/Claude/mcp*.log

# 如果没有日志文件，说明 MCP 服务器可能没有启动
```

### 方法 3: 直接询问

在 Claude 中输入：
```
你有哪些可用的工具？
```

如果看到 `map-navigation` 相关的工具，说明配置成功！

---

## ❌ 常见问题和解决方案

### 问题 1: 配置文件不存在

**症状：**
```bash
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json
# cat: ...: No such file or directory
```

**解决方案：**
```bash
# 创建配置文件
cat > ~/Library/Application\ Support/Claude/claude_desktop_config.json << 'EOF'
{
  "mcpServers": {
    "map-navigation": {
      "command": "/Users/sanmu/eva/qwall2/qwall2-mcp"
    }
  }
}
EOF
```

✅ **已解决！** 文件已创建。

---

### 问题 2: 可执行文件路径错误

**症状：**
Claude Desktop 无法启动 MCP 服务器

**检查方法：**
```bash
# 验证路径是否正确
ls -l /Users/sanmu/eva/qwall2/qwall2-mcp

# 如果文件不存在，重新编译
cd /Users/sanmu/eva/qwall2
make build
```

**确认路径：**
```bash
# 获取绝对路径
cd /Users/sanmu/eva/qwall2
pwd
# 输出：/Users/sanmu/eva/qwall2

# 完整路径应该是：
# /Users/sanmu/eva/qwall2/qwall2-mcp
```

---

### 问题 3: 没有执行权限

**症状：**
```
Permission denied
```

**解决方案：**
```bash
chmod +x /Users/sanmu/eva/qwall2/qwall2-mcp

# 验证权限
ls -l /Users/sanmu/eva/qwall2/qwall2-mcp
# 应该看到 -rwxr-xr-x（包含 x）
```

---

### 问题 4: JSON 格式错误

**症状：**
Claude Desktop 启动失败或无法识别配置

**检查方法：**
```bash
# 验证 JSON 格式
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json | python3 -m json.tool

# 或使用 jq（如果已安装）
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json | jq .
```

**正确格式：**
```json
{
  "mcpServers": {
    "map-navigation": {
      "command": "/Users/sanmu/eva/qwall2/qwall2-mcp"
    }
  }
}
```

**常见错误：**
- ❌ 缺少引号
- ❌ 多余的逗号
- ❌ 路径中的反斜杠
- ❌ 缺少花括号

---

### 问题 5: Claude Desktop 没有重启

**症状：**
配置后工具不可用

**解决方案：**
```bash
# 完全退出 Claude Desktop
# 方法 1: 使用快捷键
Command + Q

# 方法 2: 终端强制退出
killall Claude

# 然后重新打开
open -a Claude
```

⚠️ **注意：** 必须是完全退出，而不是最小化！

---

### 问题 6: 多个 MCP 服务器配置

**如果已有其他 MCP 服务器：**

```json
{
  "mcpServers": {
    "existing-server": {
      "command": "/path/to/existing/server"
    },
    "map-navigation": {
      "command": "/Users/sanmu/eva/qwall2/qwall2-mcp"
    }
  }
}
```

**注意：** 不要覆盖现有配置！

---

## 🛠️ 手动配置步骤

如果自动创建失败，可以手动配置：

### 步骤 1: 打开配置文件

```bash
# 使用默认编辑器
open -e ~/Library/Application\ Support/Claude/claude_desktop_config.json

# 或使用 VS Code
code ~/Library/Application\ Support/Claude/claude_desktop_config.json

# 或使用 vim
vim ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

### 步骤 2: 输入配置

复制以下内容：

```json
{
  "mcpServers": {
    "map-navigation": {
      "command": "/Users/sanmu/eva/qwall2/qwall2-mcp"
    }
  }
}
```

### 步骤 3: 保存文件

- VS Code: `Command + S`
- vim: `:wq`
- TextEdit: `Command + S`

### 步骤 4: 验证

```bash
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

---

## 🧪 测试配置

### 完整测试流程

1. **确认文件存在**
   ```bash
   ls -la ~/Library/Application\ Support/Claude/claude_desktop_config.json
   ```

2. **确认内容正确**
   ```bash
   cat ~/Library/Application\ Support/Claude/claude_desktop_config.json
   ```

3. **确认可执行文件**
   ```bash
   ls -lh /Users/sanmu/eva/qwall2/qwall2-mcp
   /Users/sanmu/eva/qwall2/qwall2-mcp
   # 应该看到启动日志
   ```

4. **重启 Claude Desktop**
   ```bash
   killall Claude
   open -a Claude
   ```

5. **测试对话**
   ```
   从北京到上海
   ```

---

## 📋 快速检查清单

配置前检查：

- [ ] Claude Desktop 已安装
- [ ] qwall2-mcp 已编译
- [ ] 可执行文件有执行权限
- [ ] 知道项目的完整路径

配置后检查：

- [ ] 配置文件已创建
- [ ] JSON 格式正确
- [ ] 路径指向正确的文件
- [ ] Claude Desktop 已完全重启
- [ ] 测试对话成功

---

## 🎯 成功标志

当你看到以下情况时，说明配置成功：

1. ✅ Claude 能理解导航请求
2. ✅ 浏览器自动打开地图
3. ✅ 地图显示正确的路线
4. ✅ Claude 返回导航链接

**测试对话：**
```
用户: 从北京到上海

Claude: 我来帮您规划从北京到上海的路线。
[调用工具]
✅ 成功打开 百度地图
📍 起点：北京
📍 终点：上海
🔗 导航链接：https://...
```

---

## 📚 相关文档

- [`RUN_DEMO.md`](RUN_DEMO.md) - 运行演示
- [`QUICKSTART.md`](QUICKSTART.md) - 快速开始
- [`USAGE.md`](USAGE.md) - 使用指南
- [`QUICK_REFERENCE.md`](QUICK_REFERENCE.md) - 快速参考

---

## 🆘 获取帮助

如果仍然无法配置成功：

1. **检查 Claude Desktop 版本**
   - 确保是最新版本
   - 支持 MCP 协议的版本

2. **查看详细日志**
   ```bash
   tail -f ~/Library/Logs/Claude/*.log
   ```

3. **验证系统环境**
   ```bash
   # 检查 Go 版本
   go version
   
   # 检查文件权限
   ls -la ~/Library/Application\ Support/Claude/
   ```

4. **重新编译项目**
   ```bash
   cd /Users/sanmu/eva/qwall2
   make clean
   make build
   ```

---

## ✅ 当前状态

**配置文件：** ✅ 已创建  
**位置：** `~/Library/Application Support/Claude/claude_desktop_config.json`  
**内容：** ✅ 正确  
**可执行文件：** ✅ 存在 (6.6M)  

**下一步：** 重启 Claude Desktop 并测试！

---

**更新时间：** 2025-10-24  
**状态：** 🟢 配置完成，等待测试
