#!/bin/bash

# AI Complaint Handler Pro - 快速推送脚本
# 使用方法：./push-to-github.sh YOUR_USERNAME

set -e

if [ -z "$1" ]; then
    echo "❌ 请提供 GitHub 用户名"
    echo "用法：./push-to-github.sh YOUR_USERNAME"
    echo ""
    echo "示例：./push-to-github.com your-username"
    exit 1
fi

USERNAME=$1
REPO_URL="https://github.com/$USERNAME/ai-complaint-handler.git"

echo "╔══════════════════════════════════════════════════════════╗"
echo "║   AI Complaint Handler Pro - 推送到 GitHub              ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "📝 配置信息:"
echo "  GitHub 用户名：$USERNAME"
echo "  仓库地址：$REPO_URL"
echo ""

# 配置 Git 用户
echo "⚙️  配置 Git 用户..."
git config user.name "Yupeng"
git config user.email "wtueeq@example.com"
echo "✓ Git 用户配置完成"
echo ""

# 添加远程仓库
echo "🔗 添加远程仓库..."
if git remote | grep -q '^origin$'; then
    echo "  远程仓库已存在，更新中..."
    git remote set-url origin $REPO_URL
else
    git remote add origin $REPO_URL
    echo "✓ 远程仓库添加成功"
fi
echo ""

# 重命名分支
echo "🌿 重命名分支为 main..."
git branch -M main
echo "✓ 分支重命名完成"
echo ""

# 推送代码
echo "🚀 推送到 GitHub..."
echo "  如果提示输入密码，请使用 GitHub Personal Access Token"
echo "  获取方式：GitHub → Settings → Developer settings → Personal access tokens"
echo ""

git push -u origin main

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║   ✅ 推送成功！                                        ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "下一步:"
echo "1. 访问：https://streamlit.io/cloud"
echo "2. 登录 GitHub 账号"
echo "3. 点击 'New App'"
echo "4. 选择仓库：ai-complaint-handler"
echo "5. 主文件路径：app/unified_app.py"
echo "6. 点击 'Deploy!'"
echo ""
echo "部署完成后配置域名：yupeng-ai.cn"
echo ""
