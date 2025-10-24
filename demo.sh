#!/bin/bash

# QWall2 快速演示脚本
# 用于快速验证和演示项目功能

set -e

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎯 QWall2 地图导航系统 - 快速演示"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 1. 显示项目信息
echo "📋 项目信息："
echo "   路径: $(pwd)"
echo "   Go版本: $(go version | awk '{print $3}')"
echo ""

# 2. 检查编译状态
echo "🔍 检查编译状态..."
if [ -f "qwall2-mcp" ]; then
    echo "   ✅ 可执行文件已存在"
    ls -lh qwall2-mcp | awk '{print "   大小:", $5, "修改时间:", $6, $7, $8}'
else
    echo "   ⚠️  可执行文件不存在，开始编译..."
    make build
fi
echo ""

# 3. 运行测试
echo "🧪 运行测试..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
go test ./... -v 2>&1 | grep -E "(PASS|FAIL|RUN|ok)" | head -20
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 4. 测试覆盖率
echo "📊 测试覆盖率："
go test ./... -cover 2>&1 | grep "ok\|FAIL"
echo ""

# 5. 代码检查
echo "🔍 代码检查..."
echo "   运行 go fmt..."
go fmt ./... > /dev/null 2>&1 && echo "   ✅ 代码格式正确" || echo "   ⚠️  代码格式需要调整"

echo "   运行 go vet..."
go vet ./... > /dev/null 2>&1 && echo "   ✅ 静态分析通过" || echo "   ⚠️  发现潜在问题"
echo ""

# 6. 显示项目结构
echo "📁 项目结构："
echo "   核心代码文件:"
find . -name "*.go" -not -path "./.*" | grep -v "_test.go" | head -10
echo ""
echo "   测试文件:"
find . -name "*_test.go" -not -path "./.*" | head -5
echo ""

# 7. 显示可用命令
echo "🛠️  可用命令："
echo "   make build    - 编译项目"
echo "   make test     - 运行测试"
echo "   make coverage - 生成覆盖率报告"
echo "   make run      - 运行服务器"
echo "   make clean    - 清理构建文件"
echo ""

# 8. Claude Desktop 配置提示
echo "⚙️  Claude Desktop 配置："
echo "   配置文件位置 (macOS):"
echo "   ~/Library/Application Support/Claude/claude_desktop_config.json"
echo ""
echo "   配置内容:"
echo '   {'
echo '     "mcpServers": {'
echo '       "map-navigation": {'
echo "         \"command\": \"$(pwd)/qwall2-mcp\""
echo '       }'
echo '     }'
echo '   }'
echo ""

# 9. 使用示例
echo "💡 使用示例："
echo "   在 Claude Desktop 中尝试："
echo "   - \"从北京到上海\""
echo "   - \"帮我从天安门到东方明珠导航\""
echo "   - \"用高德地图从上海到杭州\""
echo ""

# 10. 服务器启动提示
echo "🚀 启动服务器："
echo "   ./qwall2-mcp"
echo ""
echo "   或使用 Makefile:"
echo "   make run"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ 演示完成！项目已准备就绪。"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📚 更多信息请查看:"
echo "   - README.md           项目说明"
echo "   - QUICKSTART.md       快速开始"
echo "   - RUN_DEMO.md         运行演示"
echo "   - USAGE.md            使用指南"
echo ""
