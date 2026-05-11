# Deploying AI Complaint Handler Pro to https://yupeng-ai.cn

## Prerequisites
- Domain: yupeng-ai.cn
- Server with Python 3.9+ or Streamlit Cloud account
- Git repository (optional but recommended)

## Option 1: Deploy to Streamlit Cloud (Recommended - Free)

### Step 1: Prepare GitHub Repository
```bash
cd /Users/wtueeq/AI-OCR-Complaint-Handler
git init
git add .
git commit -m "Initial commit - AI Complaint Handler Pro"
git remote add origin https://github.com/YOUR_USERNAME/ai-complaint-handler.git
git push -u origin main
```

### Step 2: Connect to Streamlit Cloud
1. Go to https://streamlit.io/cloud
2. Sign in with GitHub
3. Click "New App"
4. Select repository: `ai-complaint-handler`
5. Main file path: `app/unified_app.py`
6. Python version: 3.9+
7. Click "Deploy!"

### Step 3: Configure Custom Domain
1. In Streamlit Cloud dashboard, go to Settings
2. Under "Custom Domain", enter: `yupeng-ai.cn`
3. Follow DNS configuration instructions:
   - Add CNAME record: `yupeng-ai.cn` → `your-app.streamlit.app`
   - Or add A record to your domain

### Step 4: DNS Configuration
At your domain provider (e.g., Cloudflare, GoDaddy):

**For CNAME (if supported):**
```
Type: CNAME
Name: @ or yupeng-ai.cn
Value: your-app.streamlit.app
TTL: Auto
```

**For A Record (alternative):**
```
Type: A
Name: @
Value: [Streamlit's IP - check dashboard]
TTL: Auto
```

## Option 2: Deploy to VPS/Server (Ubuntu/Debian)

### Step 1: Install Dependencies
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.9+
sudo apt install python3.9 python3.9-venv python3-pip -y

# Install Nginx
sudo apt install nginx -y

# Install Supervisor (for process management)
sudo apt install supervisor -y
```

### Step 2: Setup Application
```bash
# Create user
sudo useradd -m ai-app
sudo su - ai-app

# Clone repository
cd /home/ai-app
git clone https://github.com/YOUR_USERNAME/ai-complaint-handler.git
cd ai-complaint-handler

# Create virtual environment
python3.9 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements_unified.txt
```

### Step 3: Create Systemd Service
```bash
sudo nano /etc/systemd/system/ai-complaint.service
```

Add:
```ini
[Unit]
Description=AI Complaint Handler Pro
After=network.target

[Service]
Type=simple
User=ai-app
Group=ai-app
WorkingDirectory=/home/ai-app/ai-complaint-handler
ExecStart=/home/ai-app/ai-complaint-handler/venv/bin/streamlit run app/unified_app.py --server.headless true --server.port 8501 --server.address 0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable service:
```bash
sudo systemctl enable ai-complaint
sudo systemctl start ai-complaint
sudo systemctl status ai-complaint
```

### Step 4: Configure Nginx
```bash
sudo nano /etc/nginx/sites-available/ai-complaint
```

Add:
```nginx
server {
    listen 80;
    server_name yupeng-ai.cn www.yupeng-ai.cn;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/ai-complaint /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Step 5: SSL Certificate (Let's Encrypt)
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d yupeng-ai.cn -d www.yupeng-ai.cn
```

## Option 3: Deploy with Docker

### Step 1: Create Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements_unified.txt .
RUN pip install --no-cache-dir -r requirements_unified.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app/unified_app.py", "--server.headless", "true", "--server.port", "8501", "--server.address", "0.0.0.0"]
```

### Step 2: Build and Run
```bash
docker build -t ai-complaint-handler .
docker run -p 8501:8501 ai-complaint-handler
```

### Step 3: Deploy with Docker Compose
```yaml
# docker-compose.yml
version: '3'
services:
  ai-complaint:
    build: .
    ports:
      - "8501:8501"
    restart: always
    environment:
      - STREAMLIT_SERVER_HEADLESS=true
```

## Environment Variables (Optional)

Create `.streamlit/secrets.toml`:
```toml
[ocr]
paddle_enabled = false

[telegram]
bot_token = "YOUR_BOT_TOKEN"
chat_id = "YOUR_CHAT_ID"

[analytics]
enabled = true
```

## Testing Deployment

1. Access: `https://yupeng-ai.cn`
2. Upload test image
3. Verify OCR works
4. Check sentiment analysis
5. Test ticket generation
6. Verify export functionality

## Troubleshooting

### Import Errors
```bash
# Ensure proper path setup
export PYTHONPATH="/home/ai-app/ai-complaint-handler:$PYTHONPATH"
```

### Port Already in Use
```bash
# Change port in unified_app.py command
streamlit run app/unified_app.py --server.port 8502
```

### Static Files Not Loading
```bash
# Check file permissions
sudo chown -R ai-app:ai-app /home/ai-app/ai-complaint-handler
chmod -R 755 /home/ai-app/ai-complaint-handler
```

### Nginx 502 Error
```bash
# Check if app is running
sudo systemctl status ai-complaint

# Check Nginx logs
sudo tail -f /var/log/nginx/error.log

# Restart services
sudo systemctl restart ai-complaint
sudo systemctl restart nginx
```

## Performance Optimization

### Enable Caching
```bash
# In Nginx config
location /_stcore/static/ {
    proxy_cache_valid 200 1d;
    add_header Cache-Control "public, max-age=86400";
}
```

### Database (for production tickets)
Replace JSON file with SQLite/PostgreSQL:
```python
# In production, use:
import sqlite3
conn = sqlite3.connect('/path/to/tickets.db')
```

## Monitoring

### Logs
```bash
# Streamlit logs
sudo journalctl -u ai-complaint -f

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Health Check
```bash
curl -I https://yupeng-ai.cn
```

## Security

### Firewall (UFW)
```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### Fail2Ban
```bash
sudo apt install fail2ban -y
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

## Next Steps

1. ✅ Fix imports - DONE
2. Choose deployment option
3. Follow corresponding steps
4. Test at https://yupeng-ai.cn
5. Monitor and optimize

## Support

For issues:
- Streamlit docs: https://docs.streamlit.io
- Nginx docs: https://nginx.org/en/docs/
- Docker docs: https://docs.docker.com
