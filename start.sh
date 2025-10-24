#!/bin/bash

# AI 地图导航系统启动脚本

echo "🚀 启动 AI 地图导航系统..."
echo ""

# 检查环境变量
check_env() {
    if [ -z "$OPENAI_API_KEY" ]; then
        echo "⚠️  警告: OPENAI_API_KEY 未设置"
        echo "   STT 和 ChatGPT 功能将不可用"
    else
        echo "✅ OpenAI API Key 已配置"
    fi
    
    if [ -z "$ANTHROPIC_API_KEY" ]; then
        echo "⚠️  警告: ANTHROPIC_API_KEY 未设置"
        echo "   Claude 功能将不可用"
    else
        echo "✅ Claude API Key 已配置"
    fi
    
    if [ -z "$DEEPSEEK_API_KEY" ]; then
        echo "⚠️  警告: DEEPSEEK_API_KEY 未设置"
        echo "   DeepSeek 功能将不可用"
    else
        echo "✅ DeepSeek API Key 已配置"
    fi
    echo ""
}

# 检查环境
check_env

# 编译项目
echo "🔨 编译项目..."
go build -o qwall2-server || {
    echo "❌ 编译失败"
    exit 1
}
echo "✅ 编译成功"
echo ""

# 启动服务器
echo "🌐 启动 Web 服务器..."
echo "   访问 http://localhost:8080"
echo ""
echo "按 Ctrl+C 停止服务器"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

./qwall2-server
