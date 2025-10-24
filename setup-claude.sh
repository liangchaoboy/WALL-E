#!/bin/bash

# Claude Desktop 一键配置脚本
# 自动创建 MCP 配置文件

set -e

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎯 Claude Desktop MCP 配置工具"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 获取当前项目路径
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
EXEC_PATH="$PROJECT_DIR/qwall2-mcp"
CONFIG_DIR="$HOME/Library/Application Support/Claude"
CONFIG_FILE="$CONFIG_DIR/claude_desktop_config.json"

echo "📁 项目路径: $PROJECT_DIR"
echo "🔧 可执行文件: $EXEC_PATH"
echo "📝 配置文件: $CONFIG_FILE"
echo ""

# 检查可执行文件
echo "1️⃣  检查可执行文件..."
if [ -f "$EXEC_PATH" ]; then
    echo "   ✅ 可执行文件存在"
    ls -lh "$EXEC_PATH" | awk '{print "   大小:", $5}'
    
    # 检查执行权限
    if [ -x "$EXEC_PATH" ]; then
        echo "   ✅ 有执行权限"
    else
        echo "   ⚠️  添加执行权限..."
        chmod +x "$EXEC_PATH"
        echo "   ✅ 权限已添加"
    fi
else
    echo "   ❌ 可执行文件不存在"
    echo "   💡 请先编译项目: make build"
    exit 1
fi
echo ""

# 检查配置目录
echo "2️⃣  检查配置目录..."
if [ -d "$CONFIG_DIR" ]; then
    echo "   ✅ Claude 配置目录存在"
else
    echo "   ⚠️  Claude 配置目录不存在"
    echo "   💡 请确认 Claude Desktop 已安装"
    exit 1
fi
echo ""

# 备份现有配置
echo "3️⃣  检查现有配置..."
if [ -f "$CONFIG_FILE" ]; then
    echo "   ⚠️  配置文件已存在"
    
    # 显示现有配置
    echo "   📄 当前配置:"
    cat "$CONFIG_FILE" | sed 's/^/      /'
    echo ""
    
    # 询问是否备份
    read -p "   是否备份现有配置？(y/n) " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        BACKUP_FILE="$CONFIG_FILE.backup.$(date +%Y%m%d_%H%M%S)"
        cp "$CONFIG_FILE" "$BACKUP_FILE"
        echo "   ✅ 已备份到: $BACKUP_FILE"
    fi
    
    # 询问是否覆盖
    read -p "   是否覆盖配置？(y/n) " -n 1 -r
    echo ""
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "   ⏭️  跳过配置创建"
        echo ""
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "💡 提示: 你可以手动添加以下内容到配置文件:"
        echo ""
        echo '  "map-navigation": {'
        echo "    \"command\": \"$EXEC_PATH\""
        echo '  }'
        echo ""
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        exit 0
    fi
fi
echo ""

# 创建配置文件
echo "4️⃣  创建 MCP 配置..."

cat > "$CONFIG_FILE" << EOF
{
  "mcpServers": {
    "map-navigation": {
      "command": "$EXEC_PATH"
    }
  }
}
EOF

if [ $? -eq 0 ]; then
    echo "   ✅ 配置文件已创建"
else
    echo "   ❌ 配置文件创建失败"
    exit 1
fi
echo ""

# 验证配置
echo "5️⃣  验证配置..."
if python3 -m json.tool "$CONFIG_FILE" > /dev/null 2>&1; then
    echo "   ✅ JSON 格式正确"
else
    echo "   ❌ JSON 格式错误"
    echo "   📄 请检查配置文件"
    exit 1
fi
echo ""

# 显示配置内容
echo "6️⃣  配置内容:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
cat "$CONFIG_FILE" | python3 -m json.tool 2>/dev/null | sed 's/^/   /'
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 完成提示
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ 配置完成！"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📋 下一步操作:"
echo ""
echo "1. 完全退出 Claude Desktop"
echo "   方法: Command + Q (不是最小化!)"
echo ""
echo "2. 重新打开 Claude Desktop"
echo "   方法: 在应用程序中打开 Claude"
echo ""
echo "3. 测试对话"
echo "   输入: 从北京到上海"
echo ""
echo "4. 期望结果"
echo "   - Claude 自动调用导航工具"
echo "   - 浏览器打开百度地图"
echo "   - 显示导航路线"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📚 更多帮助: cat CLAUDE_SETUP.md"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
