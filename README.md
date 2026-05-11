# AI-OCR-Complaint-Handler

AI 智能投诉处理系统 Demo - OCR + 情感分析 + 自动分类 + 回复生成

## 功能特点

- 📸 **OCR 文字识别**: 从投诉单图片中提取文字
- 🧠 **情感分析**: 自动判断投诉情感倾向 (正面/中性/负面)
- 🏷️ **智能分类**: 自动归类到产品质量/客户服务/物流配送/退款退货等
- ✍️ **自动生成回复**: 基于投诉内容生成专业回复建议
- 📥 **导出报告**: 一键导出 JSON 格式报告

## 安装依赖

```bash
pip install streamlit pillow paddlepaddle paddleocr
```

或使用简化版 (mock OCR):

```bash
pip install streamlit pillow
```

## 运行 Demo

```bash
cd /Users/wtueeq/AI-OCR-Complaint-Handler
streamlit run app/main.py
```

## 项目结构

```
AI-OCR-Complaint-Handler/
├── app/
│   └── main.py          # Streamlit 主程序
├── templates/           # HTML 模板 (可选)
├── static/             # 静态资源
├── data/               # 数据存储
├── README.md           # 本文件
└── requirements.txt    # 依赖列表
```

## 下一步优化

1. **集成真实 OCR**: 使用 PaddleOCR 替换 mock OCR
2. **情感分析 API**: 接入百度/腾讯情感分析 API
3. **工单系统**: 生成工单并跟踪处理进度
4. **Telegram 通知**: 新投诉自动推送
5. **数据统计**: 投诉趋势分析仪表盘

## 商业模式

面向中小企业提供 SaaS 服务:
- 免费版：每月 50 次投诉处理
- 专业版：¥299/月，无限次 + 高级分析
- 企业版：¥999/月，定制分类 + API 接入

---

**版本**: v1.0 Demo  
**日期**: 2026-05-11
