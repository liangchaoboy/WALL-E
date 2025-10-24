#!/bin/bash

# 阿里云语音识别测试脚本

echo "🎤 阿里云语音识别测试"
echo ""

# 检查环境变量
if [ -z "$ALIYUN_API_KEY" ]; then
    echo "❌ 错误: ALIYUN_API_KEY 环境变量未设置"
    echo ""
    echo "请设置阿里云 API Key:"
    echo "export ALIYUN_API_KEY=\"your_api_key_here\""
    echo ""
    echo "获取 API Key 的方法:"
    echo "1. 访问 https://bailian.console.aliyun.com/"
    echo "2. 注册/登录阿里云账号"
    echo "3. 开通语音识别服务"
    echo "4. 获取 API Key"
    exit 1
fi

echo "✅ ALIYUN_API_KEY 已设置"

# 检查可选环境变量
if [ -z "$ALIYUN_MODEL" ]; then
    echo "ℹ️  ALIYUN_MODEL 未设置，将使用默认值: paraformer-realtime-v2"
    export ALIYUN_MODEL="paraformer-realtime-v2"
else
    echo "✅ ALIYUN_MODEL: $ALIYUN_MODEL"
fi

echo ""
echo "🚀 启动 qwall2 系统..."
echo ""

# 启动系统
./start.sh
