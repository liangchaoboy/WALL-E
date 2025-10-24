#!/bin/bash

# 构建脚本 - 用于编译 qwall2-mcp

set -e

echo "🔨 开始编译 qwall2-mcp..."

# 清理旧的构建文件
if [ -f "qwall2-mcp" ]; then
    echo "🧹 清理旧的构建文件..."
    rm -f qwall2-mcp
fi

# 下载依赖
echo "📦 下载依赖..."
go mod download

# 编译
echo "⚙️  编译中..."
go build -o qwall2-mcp -ldflags="-s -w" main.go

# 检查编译结果
if [ -f "qwall2-mcp" ]; then
    echo "✅ 编译成功！"
    echo "📍 可执行文件：$(pwd)/qwall2-mcp"
    echo ""
    echo "运行方式："
    echo "  ./qwall2-mcp"
    echo ""
    echo "或配置到 Claude Desktop："
    echo "  {\"command\": \"$(pwd)/qwall2-mcp\"}"
else
    echo "❌ 编译失败"
    exit 1
fi
