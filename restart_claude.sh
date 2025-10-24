#!/bin/bash

echo "🔄 正在强制重启 Claude Desktop..."
echo ""

# 1. 结束所有 Claude 相关进程
echo "1️⃣  结束 Claude 进程..."
killall Claude 2>/dev/null
sleep 1

# 2. 结束 qwall2-mcp 进程
echo "2️⃣  结束 qwall2-mcp 进程..."
pkill -f qwall2-mcp 2>/dev/null
sleep 1

# 3. 验证进程已结束
echo "3️⃣  验证进程状态..."
CLAUDE_PROC=$(ps aux | grep -i claude | grep -v grep | grep -v check_version)
MCP_PROC=$(ps aux | grep qwall2-mcp | grep -v grep)

if [ -z "$CLAUDE_PROC" ] && [ -z "$MCP_PROC" ]; then
    echo "   ✅ 所有进程已结束"
else
    echo "   ⚠️  仍有残留进程："
    [ ! -z "$CLAUDE_PROC" ] && echo "      - Claude: $CLAUDE_PROC"
    [ ! -z "$MCP_PROC" ] && echo "      - qwall2-mcp: $MCP_PROC"
fi

echo ""
echo "4️⃣  重新启动 Claude Desktop..."
open -a Claude

echo ""
echo "⏳ 等待 Claude 启动..."
sleep 3

echo ""
echo "5️⃣  检查新进程状态..."
/Users/sanmu/eva/qwall2/check_version.sh

echo ""
echo "=================================="
echo "✅ 重启完成！"
echo "📝 请在 Claude 中测试：从北京到上海"
echo "=================================="
