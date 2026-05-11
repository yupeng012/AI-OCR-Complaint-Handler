# 🚀 快速部署指南 - AI Complaint Handler Pro

## 部署到 https://yupeng-ai.cn

### 方案选择

#### 方案 A: Streamlit Cloud (最简单，免费推荐)
- ✅ 免费托管
- ✅ 自动 HTTPS
- ✅ 无需服务器维护
- ⏱️ 5 分钟完成

#### 方案 B: VPS 服务器部署 (完全控制)
- ✅ 完全控制
- ✅ 可自定义配置
- ✅ 数据本地存储
- 💰 需要服务器

#### 方案 C: Docker 部署 (推荐生产环境)
- ✅ 环境隔离
- ✅ 易于扩展
- ✅ 版本控制
- 🐳 需要 Docker

---

## 方案 A: Streamlit Cloud 部署 (推荐新手)

### 步骤 1: 准备 GitHub 仓库
```bash
cd /Users/wtueeq/AI-OCR-Complaint-Handler
git init
git add .
git commit -m "AI Complaint Handler Pro v2.0"
git remote add origin https://github.com/YOUR_USERNAME/ai-complaint-handler.git
git push -u origin main
```

### 步骤 2: 部署到 Streamlit Cloud
1. 访问 https://streamlit.io/cloud
2. 用 GitHub 账号登录
3. 点击 "New App"
4. 选择仓库：`ai-complaint-handler`
5. 主文件路径：`app/unified_app.py`
6. Python 版本：3.9+
7. 点击 "Deploy!"

### 步骤 3: 配置自定义域名
1. 在 Streamlit 后台 → Settings → Custom Domain
2. 输入：`yupeng-ai.cn`
3. 复制 CNAME 值
4. 在域名服务商添加记录：
   ```
   类型：CNAME
   名称：@ 或 yupeng-ai.cn
   值：[从 Streamlit 复制的值]
   ```

### 步骤 4: 验证部署
- 访问：https://yupeng-ai.cn
- 等待 DNS 传播（最多 24 小时）
- 测试所有功能

---

## 方案 B: VPS 服务器部署

### 前置要求
- Ubuntu/Debian 服务器
- 域名：yupeng-ai.cn
- SSH 访问权限

### 快速部署（一键脚本）
```bash
# 1. 上传代码到服务器
scp -r /Users/wtueeq/AI-OCR-Complaint-Handler user@server:/tmp/

# 2. 登录服务器
ssh user@server

# 3. 移动到目录
cd /tmp/AI-OCR-Complaint-Handler

# 4. 运行部署脚本
sudo ./deploy.sh
```

### 手动部署步骤

#### 1. 安装依赖
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3.9 python3.9-venv python3-pip nginx -y
```

#### 2. 创建应用用户
```bash
sudo useradd -m -s /bin/bash ai-app
```

#### 3. 设置应用
```bash
sudo su - ai-app
cd /home/ai-app
git clone https://github.com/YOUR_USERNAME/ai-complaint-handler.git
cd ai-complaint-handler
python3.9 -m venv venv
source venv/bin/activate
pip install -r requirements_unified.txt
exit
```

#### 4. 创建 Systemd 服务
```bash
sudo nano /etc/systemd/system/ai-complaint.service
```

添加内容：
```ini
[Unit]
Description=AI Complaint Handler Pro
After=network.target

[Service]
Type=simple
User=ai-app
WorkingDirectory=/home/ai-app/ai-complaint-handler
ExecStart=/home/ai-app/ai-complaint-handler/venv/bin/streamlit run app/unified_app.py --server.headless true --server.port 8501 --server.address 0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
```

启用服务：
```bash
sudo systemctl daemon-reload
sudo systemctl enable ai-complaint
sudo systemctl start ai-complaint
```

#### 5. 配置 Nginx
```bash
sudo cp nginx.conf /etc/nginx/sites-available/ai-complaint
sudo ln -sf /etc/nginx/sites-available/ai-complaint /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl reload nginx
```

#### 6. 安装 SSL 证书
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d yupeng-ai.cn -d www.yupeng-ai.cn
```

---

## 方案 C: Docker 部署

### 步骤 1: 构建镜像
```bash
cd /Users/wtueeq/AI-OCR-Complaint-Handler
docker build -t ai-complaint-handler .
```

### 步骤 2: 运行容器
```bash
docker run -d \
  -p 8501:8501 \
  --name ai-complaint \
  --restart always \
  -v $(pwd)/data:/app/data \
  ai-complaint-handler
```

### 步骤 3: Docker Compose (推荐)
```bash
docker-compose up -d
```

### 步骤 4: Nginx 反向代理
使用上面的 `nginx.conf` 配置

---

## 验证部署

### 1. 检查服务状态
```bash
# Systemd 服务
sudo systemctl status ai-complaint

# Docker 容器
docker ps | grep ai-complaint

# 端口监听
sudo netstat -tlnp | grep 8501
```

### 2. 测试访问
```bash
# 本地测试
curl http://localhost:8501

# 远程测试
curl https://yupeng-ai.cn

# 健康检查
curl http://localhost:8501/_stcore/health
```

### 3. 查看日志
```bash
# 应用日志
sudo journalctl -u ai-complaint -f

# Nginx 日志
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Docker 日志
docker logs -f ai-complaint
```

---

## 常见问题

### 1. 导入错误
```bash
# 确保在正确的目录运行
cd /home/ai-app/ai-complaint-handler
source venv/bin/activate
python -m streamlit run app/unified_app.py
```

### 2. 端口被占用
```bash
# 更改端口
streamlit run app/unified_app.py --server.port 8502
```

### 3. Nginx 502 错误
```bash
# 检查后端是否运行
sudo systemctl status ai-complaint

# 重启服务
sudo systemctl restart ai-complaint
sudo systemctl restart nginx
```

### 4. SSL 证书问题
```bash
# 重新申请证书
sudo certbot certonly --force-renewal -d yupeng-ai.cn

# 检查证书路径
sudo ls -la /etc/letsencrypt/live/yupeng-ai.cn/
```

---

## 性能优化

### 1. 启用缓存
在 Nginx 配置中添加：
```nginx
location /_stcore/static/ {
    proxy_cache_valid 200 1d;
    add_header Cache-Control "public, max-age=86400";
}
```

### 2. 数据库优化
将 JSON 存储改为 SQLite：
```python
import sqlite3
conn = sqlite3.connect('/path/to/tickets.db')
```

### 3. 启用 Gzip 压缩
```nginx
gzip on;
gzip_types text/plain text/css application/json application/javascript;
```

---

## 监控和备份

### 监控
```bash
# 实时监控
watch -n 5 'systemctl status ai-complaint'

# 资源使用
htop

# 端口监控
sudo netstat -tlnp | grep 8501
```

### 备份
```bash
# 备份数据
tar -czf backup-$(date +%Y%m%d).tar.gz /home/ai-app/ai-complaint-handler/data/

# 备份配置
sudo cp /etc/nginx/sites-available/ai-complaint ./nginx-backup.conf
sudo cp /etc/systemd/system/ai-complaint.service ./service-backup.conf
```

---

## 下一步

1. ✅ 选择部署方案
2. ✅ 按照对应步骤操作
3. ✅ 验证部署成功
4. ✅ 配置监控和备份
5. ✅ 开始使用！

**部署完成后访问：https://yupeng-ai.cn**

需要帮助？查看：
- DEPLOYMENT.md - 详细部署文档
- README_UNIFIED.md - 系统说明
- 或联系技术支持
