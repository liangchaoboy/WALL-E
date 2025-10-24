#!/bin/bash

# qwall2 系统测试脚本
# 用于快速验证系统的各项功能

set -e

echo "🧪 qwall2 系统测试"
echo "======================="
echo ""

# 检查服务器是否运行
echo "1️⃣  检查服务器状态..."
if curl -s http://localhost:8080/api/health > /dev/null; then
    echo "✅ 服务器正在运行"
else
    echo "❌ 服务器未运行，请先启动服务器"
    echo "   运行: ./start.sh"
    exit 1
fi

echo ""

# 测试健康检查 API
echo "2️⃣  测试健康检查 API..."
HEALTH_RESPONSE=$(curl -s http://localhost:8080/api/health)
echo "   响应: $HEALTH_RESPONSE"
if echo "$HEALTH_RESPONSE" | grep -q '"status":"ok"'; then
    echo "✅ 健康检查通过"
else
    echo "❌ 健康检查失败"
    exit 1
fi

echo ""

# 测试文字导航 API
echo "3️⃣  测试文字导航 API..."
NAV_REQUEST='{
  "type": "text",
  "input": "从北京去上海",
  "ai_provider": "chatgpt",
  "map_provider": "baidu"
}'

echo "   请求: $NAV_REQUEST"

NAV_RESPONSE=$(curl -s -X POST http://localhost:8080/api/navigate \
  -H "Content-Type: application/json" \
  -d "$NAV_REQUEST")

echo "   响应: $NAV_RESPONSE"

# 注意：如果没有配置真实的 API Key，这里会失败
if echo "$NAV_RESPONSE" | grep -q '"success":true'; then
    echo "✅ 文字导航测试通过"
    
    # 提取 URL
    URL=$(echo "$NAV_RESPONSE" | grep -o '"url":"[^"]*"' | cut -d'"' -f4)
    echo "   生成的地图 URL: $URL"
    
elif echo "$NAV_RESPONSE" | grep -q 'error'; then
    echo "⚠️  导航失败（可能是 API Key 未配置）"
    ERROR=$(echo "$NAV_RESPONSE" | grep -o '"error":"[^"]*"' | cut -d'"' -f4)
    echo "   错误信息: $ERROR"
    echo ""
    echo "   提示：如需测试 AI 功能，请设置真实的 API Key："
    echo "   export OPENAI_API_KEY=\"sk-your-real-key\""
else
    echo "❌ 导航测试失败"
    exit 1
fi

echo ""

# 测试主页
echo "4️⃣  测试主页..."
if curl -s -I http://localhost:8080/ | grep -q "200 OK"; then
    echo "✅ 主页访问正常"
else
    echo "❌ 主页访问失败"
    exit 1
fi

echo ""

# 测试静态文件
echo "5️⃣  测试静态文件..."
if curl -s http://localhost:8080/static/css/style.css | grep -q "body"; then
    echo "✅ CSS 文件访问正常"
else
    echo "❌ CSS 文件访问失败"
    exit 1
fi

if curl -s http://localhost:8080/static/js/app.js | grep -q "function"; then
    echo "✅ JS 文件访问正常"
else
    echo "❌ JS 文件访问失败"
    exit 1
fi

echo ""
echo "======================="
echo "✅ 所有基础测试通过！"
echo ""
echo "📝 测试总结："
echo "   - 服务器运行正常"
echo "   - API 端点可访问"
echo "   - 静态文件正常"
echo ""
echo "🌐 访问地址："
echo "   http://localhost:8080"
echo ""
echo "💡 下一步："
echo "   1. 在浏览器中打开 http://localhost:8080"
echo "   2. 测试文字输入导航功能"
echo "   3. 测试语音输入导航功能（需要真实 API Key）"
echo ""
