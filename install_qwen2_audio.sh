#!/bin/bash

# Qwen2-Audio 安装脚本
# 用于安装 Qwen2-Audio 语音识别所需的依赖

echo "🎤 安装 Qwen2-Audio 语音识别依赖..."
echo ""

# 检查 Python 是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装，请先安装 Python3"
    echo "   macOS: brew install python3"
    echo "   Ubuntu: sudo apt install python3 python3-pip"
    exit 1
fi

echo "✅ Python3 已安装"

# 检查 pip 是否安装
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 未安装，请先安装 pip3"
    exit 1
fi

echo "✅ pip3 已安装"

# 安装依赖
echo ""
echo "📦 安装 Python 依赖包..."

pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip3 install transformers
pip3 install librosa
pip3 install soundfile
pip3 install accelerate

echo ""
echo "✅ 依赖安装完成！"
echo ""
echo "📝 使用说明："
echo "   1. 首次使用时会自动下载 Qwen2-Audio-1.5B 模型（约 3GB）"
echo "   2. 模型会缓存在 ~/.cache/huggingface/ 目录"
echo "   3. 支持 CPU 和 GPU 运行，GPU 性能更好"
echo "   4. 语音识别需要一定的计算资源，建议在性能较好的机器上使用"
echo ""
echo "🚀 现在可以启动 qwall2 系统，语音识别功能将自动使用 Qwen2-Audio"
echo ""
