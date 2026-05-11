# Streamlit Cloud 部署说明

## ✅ 已完成的配置

以下文件已为 Streamlit Cloud 优化：

1. **requirements.txt** - 最小化依赖，移除了需要系统级安装的 OCR 库
2. **setup.sh** - 系统安装脚本（Streamlit Cloud 会自动执行）
3. **.streamlit/config.toml** - Streamlit 配置
4. **.streamlit/secrets.template.toml** - 密钥配置模板

## 🚀 部署步骤

### 1. 在 Streamlit Cloud 创建应用

访问：https://streamlit.io/cloud

1. 用 GitHub 登录
2. 点击 "New app"
3. 选择仓库：`yupeng012/AI-OCR-Complaint-Handler`
4. 分支：`main`
5. **重要**：文件路径填写 `app/unified_app.py`
6. 点击 "Advanced settings"
7. 在 "Build" 部分确认：
   - Python version: 3.9+
   - Requirements file: `requirements.txt`
   - Install command: (留空)
   - Setup script: `setup.sh`
8. 点击 "Deploy!"

### 2. 等待部署完成

部署过程：
- 📦 Installing dependencies...
- 🔧 Running setup.sh...
- 🚀 Starting app...
- ✅ Deployment successful!

### 3. 查看部署日志

如果部署失败：
1. 点击 "Manage app"
2. 查看 "Logs" 标签
3. 查看错误信息

### 4. 配置自定义域名

部署成功后：
1. 点击 "Settings"
2. 找到 "Domain" 部分
3. 点击 "Add domain"
4. 输入：`yupeng-ai.cn`
5. 按照提示配置 DNS

### 5. 配置 Telegram（可选）

在 "Secrets" 标签添加：

```toml
[telegram]
bot_token = "YOUR_BOT_TOKEN"
chat_id = "YOUR_CHAT_ID"
```

## ⚠️ 注意事项

### OCR 功能限制

Streamlit Cloud 免费版本不支持安装 Tesseract OCR，因此：

- ✅ 文本输入模式：完全可用
- ✅ 批量文本处理：完全可用
- ⚠️ 图片 OCR：将使用模拟数据（MOCK_TEXT）
- ⚠️ 图片上传：会返回预设的示例文本

### 解决方案

如需完整的 OCR 功能，有以下选项：

**选项 1：使用 VPS 部署（推荐）**
- 完全控制，可安装所有依赖
- 成本：$5-20/月
- 使用 `deploy-to-yupeng.sh` 脚本

**选项 2：使用云 OCR 服务**
- Google Cloud Vision API
- AWS Textract
- 百度 OCR
- Azure Computer Vision

**选项 3：升级到 Streamlit 企业版**
- 可自定义 Docker 镜像
- 成本较高

## 📊 功能对比

| 功能 | Streamlit Cloud | VPS 部署 |
|------|----------------|---------|
| 文本输入分析 | ✅ 完全支持 | ✅ 完全支持 |
| 情感分析 | ✅ 完全支持 | ✅ 完全支持 |
| 自动分类 | ✅ 完全支持 | ✅ 完全支持 |
| 生成回复 | ✅ 完全支持 | ✅ 完全支持 |
| Excel 导出 | ✅ 完全支持 | ✅ 完全支持 |
| Telegram 通知 | ✅ 完全支持 | ✅ 完全支持 |
| 图片 OCR | ⚠️ 模拟数据 | ✅ 完全支持 |
| 批量处理 | ✅ 完全支持 | ✅ 完全支持 |
| 自定义域名 | ✅ 支持 | ✅ 支持 |
| 成本 | 免费 | $5-20/月 |

## 🔧 故障排除

### 错误：Error installing requirements

**原因**：依赖冲突或系统库缺失

**解决**：
1. 检查 `requirements.txt` 是否最简
2. 移除需要系统库的依赖
3. 重新部署

### 错误：No module named 'utils'

**原因**：导入路径问题

**解决**：
已在 `unified_app.py` 中添加：
```python
sys.path.insert(0, str(parent_dir))
```

### 错误：Tesseract not found

**原因**：系统未安装 Tesseract OCR

**解决**：
这是预期的行为（在 Streamlit Cloud 上）。应用会自动使用模拟数据。
如需真实 OCR，请使用 VPS 部署。

## 📝 下一步

1. **立即可用**：在 Streamlit Cloud 上部署测试版
2. **生产环境**：使用 VPS 部署获得完整功能
3. **配置域名**：DNS 设置完成后访问 `https://yupeng-ai.cn`

## 📞 需要帮助？

- 查看日志：Streamlit Cloud → Manage app → Logs
- 查看文档：`DEPLOY.md` 或 `部署指南.md`
- GitHub Issues: https://github.com/yupeng012/AI-OCR-Complaint-Handler/issues

---

**开始部署**: https://streamlit.io/cloud
