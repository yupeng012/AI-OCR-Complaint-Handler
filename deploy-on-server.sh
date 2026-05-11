#!/bin/bash

# AI Complaint Handler Pro - 服务器一键部署脚本
# 使用方法：在有 Python 的 Linux 服务器上执行 ./deploy-on-server.sh

set -e

echo "╔══════════════════════════════════════════════════════════╗"
echo "║   AI Complaint Handler Pro - 服务器自动部署             ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装"
    echo "请执行：sudo apt install python3 python3-pip -y"
    exit 1
fi

echo "✓ Python3 已安装: $(python3 --version)"

# 安装依赖
echo ""
echo "📦 安装依赖..."
pip3 install --upgrade pip
pip3 install -r requirements_unified.txt

echo ""
echo "✓ 依赖安装完成"

# 创建必要目录
echo ""
echo "📁 创建目录结构..."
mkdir -p data styles utils app
touch data/tickets.json
echo "[]" > data/tickets.json
echo "✓ 目录创建完成"

# 启动服务
echo ""
echo "🚀 启动服务..."
echo "访问地址：http://$(hostname -I | awk '{print $1}'):8501"
echo ""
echo "按 Ctrl+C 停止服务"
echo ""

# 后台运行
streamlit run app/unified_app.py --server.headless true --server.port 8501 --server.address 0.0.0.0
