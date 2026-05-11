# 🤖 AI Complaint Handler Pro

AI-powered complaint handling system with OCR, sentiment analysis, auto-categorization, and real-time notifications.

![Features](https://img.shields.io/badge/features-OCR%20%7C%20Sentiment%20Analysis%20%7C%20Auto--Categorization-blue)
![Deployment](https://img.shields.io/badge/deployment-Streamlit%20Cloud%20%7C%20Docker%20%7C%20VPS-green)
![License](https://img.shields.io/badge/license-MIT-orange)

## ✨ Features

- **📸 OCR Recognition**: Extract text from complaint images instantly
- **🧠 Sentiment Analysis**: Detect customer emotions with AI (95%+ accuracy)
- **🏷️ Smart Categorization**: Auto-classify complaints into predefined categories
- **⚡ Auto Response**: Generate professional responses automatically
- **📊 Batch Processing**: Handle multiple complaints simultaneously
- **📝 Custom Templates**: Create and save response templates
- **📤 Excel Export**: Export all tickets and analytics to Excel
- **🔔 Real-time Alerts**: Instant Telegram notifications for new complaints
- **🎨 Dark Tech Theme**: Modern, professional UI with dark theme

## 🚀 Quick Start

### Option 1: Streamlit Cloud (Recommended)

1. Visit [Streamlit Cloud](https://streamlit.io/cloud)
2. Connect this repository
3. Deploy instantly!

### Option 2: Local Deployment

```bash
# Clone the repository
git clone https://github.com/yupeng012/AI-OCR-Complaint-Handler.git
cd AI-OCR-Complaint-Handler

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app/unified_app.py
```

### Option 3: Docker

```bash
docker build -t ai-complaint-handler .
docker run -p 8501:8501 ai-complaint-handler
```

## 📋 Requirements

- Python 3.9+
- Streamlit 1.28+
- Tesseract OCR
- Pandas
- OpenPyXL

## 🔧 Configuration

### Telegram Notifications

Create `.streamlit/secrets.toml`:

```toml
[telegram]
bot_token = "YOUR_BOT_TOKEN"
chat_id = "YOUR_CHAT_ID"
```

### Environment Variables

```bash
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=127.0.0.1
```

## 📊 Usage

1. **Upload Image**: Upload complaint image or type text
2. **Analyze**: Click "Analyze Sentiment" and "Categorize"
3. **Generate Ticket**: Create a ticket with one click
4. **Auto Response**: Get AI-generated professional response
5. **Export**: Download results as Excel or JSON

### Batch Processing

1. Switch to "Batch" mode
2. Upload multiple images
3. Process all at once
4. Export results

## 🏗️ Project Structure

```
AI-OCR-Complaint-Handler/
├── app/
│   ├── unified_app.py       # Main application
│   └── enhanced_app.py      # Enhanced version
├── utils/
│   ├── ocr_engine.py        # OCR functionality
│   ├── sentiment_analyzer.py # Sentiment analysis
│   ├── categorizer.py       # Auto-categorization
│   └── response_generator.py # Response generation
├── styles/
│   └── dark_tech_theme.py   # Dark theme CSS
├── data/
│   └── tickets.json         # Ticket storage
├── deploy/
│   ├── deploy-to-yupeng.sh  # Deployment script
│   └── quick-deploy.sh      # Quick deploy
├── requirements.txt
├── .gitignore
└── README.md
```

## 🌐 Deployment

### Streamlit Cloud

1. Push code to GitHub (✅ Done)
2. Connect to Streamlit Cloud
3. Configure domain: `yupeng-ai.cn`
4. Add secrets for Telegram

### VPS Deployment

```bash
# Run deployment script
./deploy-to-yupeng.sh
```

See [DEPLOY.md](DEPLOY.md) for detailed instructions.

## 📈 Analytics Dashboard

- Total tickets processed
- Category distribution
- Sentiment trends
- Response time metrics

## 🔒 Security

- API keys stored in `.streamlit/secrets.toml` (not committed)
- Sensitive files in `.gitignore`
- HTTPS enforced in production
- Input validation and sanitization

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## 📝 License

MIT License - see LICENSE file for details

## 👨‍💻 Author

**yupeng012**

## 🙏 Acknowledgments

- Streamlit team for the amazing framework
- Tesseract OCR team
- Open source AI community

## 📞 Support

- Issues: https://github.com/yupeng012/AI-OCR-Complaint-Handler/issues
- Email: support@yupeng-ai.cn

---

**Live Demo**: [https://yupeng-ai.cn](https://yupeng-ai.cn) (coming soon)

**Star this repo if you find it useful! ⭐**
