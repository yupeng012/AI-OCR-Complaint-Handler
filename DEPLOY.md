# Deploy AI Complaint Handler to yupeng-ai.cn

This guide will deploy your Streamlit app from localhost:8504 to https://yupeng-ai.cn

## Deployment Options

### Option 1: Streamlit Cloud (Recommended - Free & Easiest)

**Steps:**
1. Push code to GitHub
2. Connect to Streamlit Cloud
3. Configure domain

**Execute:**

```bash
# 1. Push to GitHub
cd /Users/wtueeq/AI-OCR-Complaint-Handler
./push-to-github.sh

# 2. Go to https://streamlit.io/cloud
# 3. Connect your GitHub repo
# 4. Add custom domain: yupeng-ai.cn
# 5. Configure DNS in your domain provider
```

---

### Option 2: Docker Deployment (Full Control)

**Prerequisites:**
- Docker installed on server
- Domain DNS configured
- SSL certificate (Let's Encrypt)

**Execute on server:**

```bash
# 1. Clone repository
git clone https://github.com/YOUR_USERNAME/AI-OCR-Complaint-Handler.git
cd AI-OCR-Complaint-Handler

# 2. Build Docker image
docker build -t ai-complaint-handler .

# 3. Run container
docker run -d -p 8501:8501 \
  --name ai-complaint \
  --restart unless-stopped \
  ai-complaint-handler

# 4. Setup Nginx reverse proxy
sudo cp nginx.conf /etc/nginx/sites-available/yupeng-ai.cn
sudo ln -s /etc/nginx/sites-available/yupeng-ai.cn /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# 5. Setup SSL with Let's Encrypt
sudo certbot --nginx -d yupeng-ai.cn
```

---

### Option 3: VPS Direct Deployment

**Execute on server (Ubuntu/Debian):**

```bash
# 1. Install dependencies
sudo apt update
sudo apt install -y python3-pip python3-venv nginx certbot

# 2. Clone and setup
cd /var/www
git clone https://github.com/YOUR_USERNAME/AI-OCR-Complaint-Handler.git
cd AI-OCR-Complaint-Handler

# 3. Create virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. Create systemd service
sudo tee /etc/systemd/system/ai-complaint.service > /dev/null << 'EOF'
[Unit]
Description=AI Complaint Handler
After=network.target

[Service]
Type=exec
User=www-data
WorkingDirectory=/var/www/AI-OCR-Complaint-Handler
ExecStart=/var/www/AI-OCR-Complaint-Handler/venv/bin/python -m streamlit run app/unified_app.py --server.headless true --server.port 8501 --server.address 127.0.0.1
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 5. Enable and start
sudo systemctl daemon-reload
sudo systemctl enable ai-complaint
sudo systemctl start ai-complaint

# 6. Configure Nginx
sudo cp deploy/nginx.conf /etc/nginx/sites-available/yupeng-ai.cn
sudo ln -s /etc/nginx/sites-available/yupeng-ai.cn /etc/nginx/sites-enabled/
sudo nginx -t

# 7. Setup SSL
sudo certbot --nginx -d yupeng-ai.cn

# 8. Reload Nginx
sudo systemctl reload nginx
```

---

## Quick Deploy Script

Run this script for automated deployment:

```bash
#!/bin/bash
# deploy-to-yupeng.sh

DOMAIN="yupeng-ai.cn"
EMAIL="your-email@example.com"

echo "🚀 Deploying AI Complaint Handler to $DOMAIN"

# Check if running on server
if [ ! -f "/etc/nginx/nginx.conf" ]; then
    echo "❌ This script must run on the server with Nginx installed"
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
sudo apt update
sudo apt install -y python3-pip python3-venv nginx certbot python3-certbot-nginx

# Setup app
echo "🔧 Setting up application..."
cd /var/www
git clone https://github.com/YOUR_USERNAME/AI-OCR-Complaint-Handler.git || true
cd AI-OCR-Complaint-Handler

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Systemd service
echo "⚙️  Configuring systemd..."
sudo tee /etc/systemd/system/ai-complaint.service > /dev/null << 'EOF'
[Unit]
Description=AI Complaint Handler
After=network.target

[Service]
Type=exec
User=www-data
WorkingDirectory=/var/www/AI-OCR-Complaint-Handler
ExecStart=/var/www/AI-OCR-Complaint-Handler/venv/bin/python -m streamlit run app/unified_app.py --server.headless true --server.port 8501 --server.address 127.0.0.1
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable ai-complaint
sudo systemctl start ai-complaint

# Nginx config
echo "🌐 Configuring Nginx..."
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

sudo ln -s /etc/nginx/sites-available/$DOMAIN /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# SSL certificate
echo "🔒 Setting up SSL..."
sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN --non-interactive --agree-tos --email $EMAIL

echo "✅ Deployment complete!"
echo "🌐 Visit: https://$DOMAIN"
```

---

## Verify Deployment

After deployment, verify:

```bash
# Check service status
sudo systemctl status ai-complaint

# Check Nginx
sudo nginx -t
sudo systemctl status nginx

# Test locally
curl http://127.0.0.1:8501

# Test domain
curl https://yupeng-ai.cn
```

---

## Environment Variables

Create `.env` file for production:

```bash
# Telegram Config
TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN
TELEGRAM_CHAT_ID=YOUR_CHAT_ID

# API Keys
OPENAI_API_KEY=sk-...
MINIMAX_API_KEY=...

# App Config
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=127.0.0.1
```

---

## Troubleshooting

### Port already in use
```bash
sudo lsof -i :8501
sudo kill -9 <PID>
```

### Nginx error
```bash
sudo nginx -t
sudo journalctl -u nginx -f
```

### App not starting
```bash
sudo journalctl -u ai-complaint -f
```

### SSL issues
```bash
sudo certbot certificates
sudo certbot renew
```
