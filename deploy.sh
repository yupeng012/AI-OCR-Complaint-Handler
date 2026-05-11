#!/bin/bash

# AI Complaint Handler Pro - Quick Deploy Script
# For deploying to yupeng-ai.cn

set -e

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║     AI Complaint Handler Pro - Deployment Script                ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

# Configuration
DOMAIN="yupeng-ai.cn"
APP_DIR="/home/ai-app/ai-complaint-handler"
PYTHON_VERSION="3.9"

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
  echo "⚠️  Please run as root (sudo ./deploy.sh)"
  exit 1
fi

echo "📋 Deployment Configuration:"
echo "  Domain: $DOMAIN"
echo "  App Directory: $APP_DIR"
echo "  Python Version: $PYTHON_VERSION"
echo ""

# Step 1: Install dependencies
echo "📦 Step 1/6: Installing system dependencies..."
apt update
apt install -y python3.9 python3.9-venv python3-pip nginx supervisor git curl

# Step 2: Create user
echo "👤 Step 2/6: Creating application user..."
if ! id "ai-app" &>/dev/null; then
    useradd -m -s /bin/bash ai-app
    echo "✓ User 'ai-app' created"
else
    echo "✓ User 'ai-app' already exists"
fi

# Step 3: Setup application
echo "🚀 Step 3/6: Setting up application..."
su - ai-app -c "
cd /home/ai-app
if [ ! -d 'ai-complaint-handler' ]; then
    git clone https://github.com/YOUR_USERNAME/ai-complaint-handler.git
else
    echo '✓ Application directory exists'
fi
cd ai-complaint-handler
python3.9 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements_unified.txt
"

# Step 4: Configure systemd service
echo "⚙️  Step 4/6: Configuring systemd service..."
cat > /etc/systemd/system/ai-complaint.service << EOF
[Unit]
Description=AI Complaint Handler Pro
After=network.target

[Service]
Type=simple
User=ai-app
Group=ai-app
WorkingDirectory=$APP_DIR
ExecStart=$APP_DIR/venv/bin/streamlit run app/unified_app.py --server.headless true --server.port 8501 --server.address 0.0.0.0
Restart=always
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable ai-complaint
systemctl start ai-complaint

# Step 5: Configure Nginx
echo "🌐 Step 5/6: Configuring Nginx..."
cp nginx.conf /etc/nginx/sites-available/ai-complaint
ln -sf /etc/nginx/sites-available/ai-complaint /etc/nginx/sites-enabled/ai-complaint
rm -f /etc/nginx/sites-enabled/default

# Test Nginx config
if nginx -t; then
    systemctl reload nginx
    echo "✓ Nginx configured successfully"
else
    echo "✗ Nginx configuration test failed"
    exit 1
fi

# Step 6: SSL Certificate (optional)
echo "🔒 Step 6/6: SSL Certificate setup..."
if command -v certbot &> /dev/null; then
    echo "Certbot found. Setting up SSL..."
    certbot --nginx -d $DOMAIN -d www.$DOMAIN --non-interactive --agree-tos --email your-email@example.com
else
    echo "⚠️  Certbot not found. Install with: apt install certbot python3-certbot-nginx"
    echo "   Then run: certbot --nginx -d $DOMAIN -d www.$DOMAIN"
fi

# Final checks
echo ""
echo "══════════════════════════════════════════════════════════════════"
echo "✅ Deployment Complete!"
echo "══════════════════════════════════════════════════════════════════"
echo ""
echo "Service Status:"
systemctl status ai-complaint --no-pager
echo ""
echo "Application URLs:"
echo "  Local:   http://localhost:8501"
echo "  Public:  http://$DOMAIN"
echo "  HTTPS:   https://$DOMAIN (after SSL setup)"
echo ""
echo "Useful Commands:"
echo "  Status:     systemctl status ai-complaint"
echo "  Start:      systemctl start ai-complaint"
echo "  Stop:       systemctl stop ai-complaint"
echo "  Restart:    systemctl restart ai-complaint"
echo "  Logs:       journalctl -u ai-complaint -f"
echo "  Nginx:      nginx -t && systemctl reload nginx"
echo ""
echo "Next Steps:"
echo "  1. Configure DNS records for $DOMAIN"
echo "  2. Setup SSL certificate (if not done)"
echo "  3. Test application at https://$DOMAIN"
echo "  4. Monitor logs: journalctl -u ai-complaint -f"
echo ""
