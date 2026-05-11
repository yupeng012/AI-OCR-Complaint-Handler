#!/bin/bash
# quick-deploy.sh - 快速部署到 yupeng-ai.cn
# 在 VPS 服务器上运行此脚本

set -e

# ============ 配置区域 ============
DOMAIN="yupeng-ai.cn"
EMAIL="your-email@example.com"  # 修改为你的邮箱
GITHUB_REPO="https://github.com/YOUR_USERNAME/AI-OCR-Complaint-Handler.git"
# ==================================

echo "╔══════════════════════════════════════════════════╗"
echo "║  🚀 快速部署 AI Complaint Handler                ║"
echo "║     目标：https://$DOMAIN                        ║"
echo "╚══════════════════════════════════════════════════╝"

# 检查是否在服务器上
if [ ! -f "/etc/nginx/nginx.conf" ]; then
    echo "❌ 错误：必须在已安装 Nginx 的服务器上运行此脚本"
    echo ""
    echo "步骤："
    echo "1. 准备一台 Ubuntu 服务器（推荐 20.04+）"
    echo "2. 确保域名 $DOMAIN 已解析到服务器 IP"
    echo "3. 在此服务器上运行此脚本"
    exit 1
fi

echo ""
echo "✅ 环境检查通过"
echo ""

# 1. 安装依赖
echo "📦 [1/5] 安装系统依赖..."
sudo apt update -qq
sudo apt install -y python3-pip python3-venv nginx certbot python3-certbot-nginx git
echo "   ✅ 依赖安装完成"
echo ""

# 2. 克隆代码
echo "📁 [2/5] 获取应用代码..."
cd /var/www
if [ -d "AI-OCR-Complaint-Handler" ]; then
    echo "   ⚠️  应用已存在，更新代码..."
    cd AI-OCR-Complaint-Handler
    sudo -u ubuntu git pull || true
else
    echo "   📥 克隆仓库..."
    sudo git clone $GITHUB_REPO AI-OCR-Complaint-Handler
    cd AI-OCR-Complaint-Handler
fi
echo "   ✅ 代码准备完成"
echo ""

# 3. Python 环境
echo "🐍 [3/5] 配置 Python 环境..."
python3 -m venv venv
./venv/bin/pip install --upgrade pip -q
./venv/bin/pip install -r requirements.txt -q
echo "   ✅ Python 环境就绪"
echo ""

# 4. 系统服务
echo "⚙️  [4/5] 配置系统服务..."
sudo tee /etc/systemd/system/ai-complaint.service > /dev/null << 'EOF'
[Unit]
Description=AI Complaint Handler - Streamlit
After=network.target

[Service]
Type=exec
User=ubuntu
WorkingDirectory=/var/www/AI-OCR-Complaint-Handler
ExecStart=/var/www/AI-OCR-Complaint-Handler/venv/bin/python -m streamlit run app/unified_app.py --server.headless true --server.port 8501 --server.address 127.0.0.1
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable ai-complaint
sudo systemctl start ai-complaint
echo "   ✅ 服务已启动"
echo ""

# 5. Nginx + SSL
echo "🌐 [5/5] 配置 Nginx 和 SSL..."
sudo tee /etc/nginx/sites-available/$DOMAIN > /dev/null << EOF
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;

    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/$DOMAIN /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t -q
sudo systemctl reload nginx

# SSL 证书
echo "🔒 申请 SSL 证书..."
sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN --non-interactive --agree-tos --email $EMAIL
echo "   ✅ SSL 配置完成"
echo ""

# 验证
echo "══════════════════════════════════════════════════"
echo "  ✅ 部署成功！"
echo "══════════════════════════════════════════════════"
echo ""
echo "  🌐 访问地址："
echo "     https://$DOMAIN"
echo "     https://www.$DOMAIN"
echo ""
echo "  📊 服务状态："
APP_STATUS=$(sudo systemctl is-active ai-complaint)
NGINX_STATUS=$(sudo systemctl is-active nginx)
echo "     AI Complaint Handler: $APP_STATUS"
echo "     Nginx: $NGINX_STATUS"
echo ""
echo "  🔧 常用命令："
echo "     sudo systemctl status ai-complaint  # 查看状态"
echo "     sudo journalctl -u ai-complaint -f  # 查看日志"
echo "     sudo systemctl restart ai-complaint # 重启服务"
echo ""
echo "══════════════════════════════════════════════════"
