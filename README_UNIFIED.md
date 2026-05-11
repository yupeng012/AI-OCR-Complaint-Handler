# AI Complaint Handler Pro - Unified System

## Overview
Merged version of AI Complaint Handler Demo and Pro with:
- Dark tech theme with gradients and animations
- Interactive demo for real-time experience
- Data visualization for analysis process and results
- Professional typography and motion effects

## Features
1. **OCR Text Recognition**: Upload images or input text manually
2. **Sentiment Analysis**: Real-time emotion detection (Positive/Neutral/Negative)
3. **Smart Categorization**: Auto-classify into 5 categories
4. **Ticket Management**: Full lifecycle tracking
5. **Auto-Response Generation**: AI-powered suggested replies
6. **Data Visualization**: Charts and analytics dashboard
7. **Telegram Notifications**: Real-time alerts

## File Structure
```
AI-OCR-Complaint-Handler/
├── app/
│   ├── unified_app.py          # Main unified application
│   ├── main.py                 # Original demo (legacy)
│   └── pro.py                  # Original pro (legacy)
├── components/
│   ├── sidebar.py              # Sidebar component
│   ├── upload_section.py       # Upload section
│   ├── analysis_result.py      # Analysis results display
│   └── ticket_manager.py       # Ticket management UI
├── styles/
│   └── dark_tech_theme.py      # Dark theme CSS
├── utils/
│   ├── ocr_engine.py           # OCR processing
│   ├── sentiment_analyzer.py   # Sentiment analysis
│   ├── categorizer.py          # Auto-categorization
│   └── response_generator.py   # Auto-response generation
├── data/
│   └── tickets.json            # Ticket database
├── assets/
│   └── logo.png                # Logo (optional)
├── requirements.txt
└── README.md
```

## Setup Instructions

### 1. Install Dependencies
```bash
pip install streamlit==1.28.0
pip install pillow==10.0.0
pip install plotly==5.17.0          # For data visualization
pip install pandas==2.0.0           # For data handling
# Optional: For production OCR
# pip install paddlepaddle paddleocr
```

### 2. Run the Application
```bash
cd /Users/wtueeq/AI-OCR-Complaint-Handler
streamlit run app/unified_app.py --server.headless true --server.port 8501
```

### 3. Access the Application
- Open browser: `http://localhost:8501`
- Theme: Dark Tech with neon accents
- Features: Interactive demo, real-time analysis, data visualization

## Key Components

### Dark Tech Theme
- Background: Deep gradient (#0a0e27 → #1a1f3a)
- Primary Color: Neon Blue (#00f2ff)
- Secondary Color: Electric Purple (#bd00ff)
- Accent: Cyan (#00ff9d)
- Typography: Modern sans-serif (Inter, Roboto)
- Animations: Smooth transitions, hover effects, loading animations

### Interactive Features
1. **Image Upload**: Drag & drop with preview
2. **Real-time OCR**: Instant text extraction
3. **Live Analysis**: Animated progress bars
4. **Sentiment Gauge**: Visual emotion indicator
5. **Category Chart**: Pie chart of complaint types
6. **Ticket Timeline**: Visual ticket status flow

### Data Visualization
- Sentiment distribution chart
- Category breakdown (pie/bar chart)
- Ticket status over time (line chart)
- Response time analytics
- Word cloud of common keywords

## Usage Flow

1. **Upload/Input**: User uploads complaint image or types text
2. **OCR Processing**: System extracts text (with loading animation)
3. **Analysis**: 
   - Sentiment analysis (gauge chart)
   - Category classification (pie chart)
   - Priority scoring
4. **Ticket Generation**: Auto-create ticket with ID
5. **Response Generation**: AI suggests professional reply
6. **Export**: Download ticket as JSON/PDF
7. **Dashboard**: View all tickets with analytics

## Customization

### Theme Variables (in styles/dark_tech_theme.py)
```python
THEME = {
    'bg_primary': '#0a0e27',
    'bg_secondary': '#1a1f3a',
    'primary': '#00f2ff',
    'secondary': '#bd00ff',
    'accent': '#00ff9d',
    'text_main': '#ffffff',
    'text_muted': '#a0a0a0',
}
```

### Add New Categories
Edit `utils/categorizer.py` to add custom complaint categories.

## Deployment

### Local Development
```bash
streamlit run app/unified_app.py
```

### Production (Streamlit Cloud)
1. Push code to GitHub
2. Connect to Streamlit Cloud
3. Set environment variables
4. Deploy

### Docker Deployment
```bash
docker build -t ai-complaint-handler .
docker run -p 8501:8501 ai-complaint-handler
```

## API Endpoints (Future)
- `POST /api/ocr`: Extract text from image
- `POST /api/analyze`: Analyze sentiment and category
- `GET /api/tickets`: List all tickets
- `POST /api/tickets`: Create new ticket
- `PUT /api/tickets/{id}`: Update ticket status

## Performance Metrics
- OCR Processing: < 2 seconds
- Sentiment Analysis: < 500ms
- Category Classification: < 300ms
- Ticket Generation: < 100ms
- Total Response Time: < 3 seconds

## Security Considerations
- Input sanitization for OCR text
- Rate limiting for API calls
- Secure storage of ticket data
- HTTPS for production

## Future Enhancements
1. Multi-language support (Chinese, English, Spanish)
2. Voice complaint input
3. Email integration
4. Slack/Discord bot
5. Advanced analytics dashboard
6. Machine learning model training interface
7. Custom workflow builder

## License
MIT License

## Contact
For questions or support, contact the development team.
