#!/bin/bash

echo "=================================="
echo "检查 Claude Desktop MCP 版本状态"
echo "=================================="
echo ""

echo "1️⃣  程序编译时间："
ls -lh /Users/sanmu/eva/qwall2/qwall2-mcp | awk '{print $6, $7, $8}'

echo ""
echo "2️⃣  当前运行的进程："
PROCESS=$(ps aux | grep qwall2-mcp | grep -v grep)
if [ -z "$PROCESS" ]; then
    echo "   ❌ 没有运行中的 qwall2-mcp 进程"
    echo "   💡 需要启动 Claude Desktop"
else
    echo "$PROCESS" | awk '{print "   进程 PID:", $2, "启动时间:", $9}'
    
    # 提取启动时间
    START_TIME=$(echo "$PROCESS" | awk '{print $9}')
    echo ""
    echo "   ⚠️  如果启动时间早于编译时间，说明在用旧版本！"
fi

echo ""
echo "3️⃣  配置文件检查："
CONFIG_FILE=~/Library/Application\ Support/Claude/claude_desktop_config.json
if [ -f "$CONFIG_FILE" ]; then
    echo "   ✅ 配置文件存在"
    echo "   内容："
    cat "$CONFIG_FILE" | grep -A 3 "map-navigation"
else
    echo "   ❌ 配置文件不存在"
fi

echo ""
echo "=================================="
echo "🔧 如果启动时间早于编译时间，请："
echo "   1. 完全退出 Claude Desktop (Cmd + Q)"
echo "   2. 运行: killall Claude"
echo "   3. 重新打开 Claude Desktop"
echo "=================================="
