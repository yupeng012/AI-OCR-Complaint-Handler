#!/bin/bash
# deploy-to-yupeng.sh
# One-click deployment script for AI Complaint Handler to yupeng-ai.cn

set -e

DOMAIN="yupeng-ai.cn"
EMAIL="your-email@example.com"  # Replace with your email
GITHUB_REPO="https://github.com/YOUR_USERNAME/AI-OCR-Complaint-Handler.git"

echo "╔══════════════════════════════════════════════════════════╗"
echo "║  🚀 Deploying AI Complaint Handler to $DOMAIN            ║"
echo "╚══════════════════════════════════════════════════════════╝"

# Check if running on server with nginx
if [ ! -f "/etc/nginx/nginx.conf" ]; then
    echo "❌ This script must run on the server with Nginx installed"
    echo ""
    echo "Options:"
    echo "  1. Run this script on your VPS/server"
    echo "  2. Or use Streamlit Cloud (easier): https://streamlit.io/cloud"
    exit 1
fi

# Install dependencies
echo "📦 Step 1/6: Installing dependencies..."
sudo apt update
sudo apt install -y python3-pip python3-venv nginx certbot python3-certbot-nginx

# Setup app directory
echo "📁 Step 2/6: Setting up application..."
cd /var/www
if [ -d "AI-OCR-Complaint-Handler" ]; then
    echo "  ⚠️  App directory exists, updating..."
    cd AI-OCR-Complaint-Handler
    git pull || true
else
    echo "  📥 Cloning repository..."
    git clone $GITHUB_REPO AI-OCR-Complaint-Handler
    cd AI-OCR-Complaint-Handler
fi

# Python virtual environment
echo "🐍 Step 3/6: Setting up Python environment..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Create systemd service
echo "⚙️  Step 4/6: Configuring systemd service..."
sudo tee /etc/systemd/system/ai-complaint.service > /dev/null << 'EOF'
[Unit]
Description=AI Complaint Handler - Streamlit App
After=network.target

[Service]
Type=exec
User=www-data
WorkingDirectory=/var/www/AI-OCR-Complaint-Handler
ExecStart=/var/www/AI-OCR-Complaint-Handler/venv/bin/python -m streamlit run app/unified_app.py --server.headless true --server.port 8501 --server.address 127.0.0.1
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=ai-complaint

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable ai-complaint

# Nginx configuration
echo "🌐 Step 5/6: Configuring Nginx..."
sudo tee /etc/nginx/sites-available/$DOMAIN > /dev/null << EOF
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Static files (optional)
    location /static/ {
        alias /var/www/AI-OCR-Complaint-Handler/static/;
        expires 30d;
    }
}
EOF

# Enable site
if [ ! -L "/etc/nginx/sites-enabled/$DOMAIN" ]; then
    sudo ln -s /etc/nginx/sites-available/$DOMAIN /etc/nginx/sites-enabled/
fi

# Remove default if exists
sudo rm -f /etc/nginx/sites-enabled/default

# Test nginx config
sudo nginx -t

# SSL Certificate
echo "🔒 Step 6/6: Setting up SSL certificate..."
echo "  📧 Using email: $EMAIL"
sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN --non-interactive --agree-tos --email $EMAIL

# Start services
echo "🚀 Starting services..."
sudo systemctl start ai-complaint
sudo systemctl reload nginx

# Verify deployment
echo ""
echo "══════════════════════════════════════════════════════════"
echo "  ✅ Deployment Complete!"
echo "══════════════════════════════════════════════════════════"
echo ""
echo "  🌐 Your app is now live at:"
echo "     https://$DOMAIN"
echo "     https://www.$DOMAIN"
echo ""
echo "  📊 Service Status:"
echo "     App:      $(sudo systemctl is-active ai-complaint)"
echo "     Nginx:    $(sudo systemctl is-active nginx)"
echo ""
echo "  🔧 Useful commands:"
echo "     sudo systemctl status ai-complaint  # Check app status"
echo "     sudo journalctl -u ai-complaint -f  # View app logs"
echo "     sudo nginx -t                        # Test nginx config"
echo "     sudo certbot certificates            # View SSL certs"
echo ""
echo "  📝 Next steps:"
echo "     1. Update Telegram config in app if needed"
echo "     2. Test the app at https://$DOMAIN"
echo "     3. Share with your team!"
echo ""
echo "══════════════════════════════════════════════════════════"
