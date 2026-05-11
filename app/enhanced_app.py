#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Complaint Handler Pro - Enhanced Version
Features:
- Single & Batch Analysis
- Custom Templates
- Excel Export
- Real-time Telegram Alerts
- Dark Tech Theme
"""

import streamlit as st
from PIL import Image
import json
from pathlib import Path
from datetime import datetime
import time
import sys
import pandas as pd
import requests
from io import BytesIO

# Add parent directory to path
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

# Import utilities
from utils.ocr_engine import extract_text_from_image
from utils.sentiment_analyzer import analyze_sentiment
from utils.categorizer import categorize_complaint
from utils.response_generator import generate_response
from styles.dark_tech_theme import get_dark_tech_css

# Page config
st.set_page_config(
    page_title="AI Complaint Handler Pro - Enhanced",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply dark tech theme
st.markdown(get_dark_tech_css(), unsafe_allow_html=True)

# Telegram config
TELEGRAM_ENABLED = False
TELEGRAM_BOT_TOKEN = ""  # Add your bot token
TELEGRAM_CHAT_ID = ""    # Add your chat ID

# Initialize session state
if 'tickets' not in st.session_state:
    st.session_state.tickets = []
if 'templates' not in st.session_state:
    st.session_state.templates = {
        'default': {
            'name': 'Default Response',
            'template': 'Dear Customer,\n\nThank you for your feedback. We are investigating your concern regarding {category}.\n\nTicket ID: {ticket_id}\n\nBest regards,\nCustomer Service Team'
        }
    }
if 'batch_mode' not in st.session_state:
    st.session_state.batch_mode = False

# Load tickets from file
data_dir = Path(__file__).parent.parent / 'data'
data_dir.mkdir(parents=True, exist_ok=True)
tickets_file = data_dir / 'tickets.json'

if tickets_file.exists():
    with open(tickets_file, 'r', encoding='utf-8') as f:
        st.session_state.tickets = json.load(f)

def save_tickets():
    """Save tickets to file"""
    with open(tickets_file, 'w', encoding='utf-8') as f:
        json.dump(st.session_state.tickets, f, indent=2, ensure_ascii=False)

def send_telegram_alert(message):
    """Send real-time alert to Telegram"""
    if not TELEGRAM_ENABLED or not TELEGRAM_BOT_TOKEN:
        return False
    
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': message,
            'parse_mode': 'HTML'
        }
        resp = requests.post(url, json=data, timeout=5)
        return resp.status_code == 200
    except:
        return False

def export_to_excel(tickets):
    """Export tickets to Excel"""
    if not tickets:
        return None
    
    df_data = []
    for ticket in tickets:
        df_data.append({
            'Ticket ID': ticket.get('ticket_id', ''),
            'Timestamp': ticket.get('timestamp', '')[:19],
            'Category': ticket.get('category', ''),
            'Sentiment': ticket.get('sentiment', ''),
            'Priority': ticket.get('priority', ''),
            'Status': ticket.get('status', ''),
            'Text': ticket.get('text', '')[:200]
        })
    
    df = pd.DataFrame(df_data)
    
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Tickets', index=False)
    
    return output.getvalue()

def main():
    # Header
    st.markdown("""
    <div class="gradient-header">
        <h1 class="main-title">🤖 AI Complaint Handler Pro</h1>
        <p class="subtitle">Automatically analyze complaints • Categorize issues • Generate responses</p>
        <div class="glow-effect"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        
        # Mode selection
        mode = st.radio("Analysis Mode", ["Single", "Batch"], index=0)
        st.session_state.batch_mode = (mode == "Batch")
        
        st.markdown("---")
        st.markdown("### 📊 Statistics")
        total = len(st.session_state.tickets)
        new_count = sum(1 for t in st.session_state.tickets if t.get('status') == 'new')
        st.metric("Total Tickets", total)
        st.metric("New Today", new_count)
        
        st.markdown("---")
        st.markdown("### 📥 Export")
        if st.button("📊 Export to Excel", use_container_width=True):
            if st.session_state.tickets:
                excel_data = export_to_excel(st.session_state.tickets)
                if excel_data:
                    st.download_button(
                        label="Download Excel",
                        data=excel_data,
                        file_name=f"complaints_{datetime.now().strftime('%Y%m%d')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
        
        st.markdown("---")
        st.markdown("### 📱 Telegram Alerts")
        telegram_enabled = st.checkbox("Enable Telegram Alerts", value=False)
        if telegram_enabled:
            st.text_input("Bot Token", type="password")
            st.text_input("Chat ID")
    
    # Main content
    if st.session_state.batch_mode:
        # Batch mode
        st.markdown("### 📦 Batch Analysis")
        
        uploaded_files = st.file_uploader(
            "Upload multiple complaint images",
            type=['png', 'jpg', 'jpeg'],
            accept_multiple_files=True
        )
        
        batch_text = st.text_area("Or paste multiple complaints (one per line)", height=150)
        
        if st.button("🚀 Process Batch", use_container_width=True):
            if uploaded_files or batch_text:
                progress_bar = st.progress(0)
                results = []
                
                # Process uploaded files
                if uploaded_files:
                    for i, uploaded_file in enumerate(uploaded_files):
                        image = Image.open(uploaded_file)
                        text = extract_text_from_image(image)
                        
                        sentiment, score = analyze_sentiment(text)
                        category = categorize_complaint(text)
                        
                        ticket_id = f"TS{datetime.now().strftime('%Y%m%d%H%M%S')}_{i+1}"
                        ticket = {
                            'ticket_id': ticket_id,
                            'timestamp': datetime.now().isoformat(),
                            'text': text,
                            'sentiment': sentiment,
                            'sentiment_score': score,
                            'category': category,
                            'status': 'new',
                            'priority': 'high' if score > 0.7 else 'medium',
                            'source': 'batch_upload'
                        }
                        
                        st.session_state.tickets.append(ticket)
                        results.append(ticket)
                        
                        # Telegram alert
                        if telegram_enabled:
                            send_telegram_alert(f"🔔 New Complaint\nID: {ticket_id}\nCategory: {category}\nSentiment: {sentiment}")
                        
                        progress_bar.progress((i + 1) / len(uploaded_files))
                
                save_tickets()
                st.success(f"✅ Processed {len(results)} complaints!")
    
    else:
        # Single mode
        st.markdown("### 📥 Single Analysis")
        
        upload_method = st.radio("Input Method", ["📸 Upload Image", "✍️ Type Text"], horizontal=True)
        
        if upload_method == "📸 Upload Image":
            uploaded_file = st.file_uploader("Upload complaint image", type=['png', 'jpg', 'jpeg'])
            
            if uploaded_file:
                image = Image.open(uploaded_file)
                st.image(image, caption='Uploaded Complaint', use_container_width=True)
                
                if st.button("🔍 Extract & Analyze", use_container_width=True):
                    with st.spinner("Processing..."):
                        text = extract_text_from_image(image)
                        st.session_state.ocr_text = text
                        
                        sentiment, score = analyze_sentiment(text)
                        category = categorize_complaint(text)
                        
                        st.session_state.analysis_result = {
                            'text': text,
                            'sentiment': sentiment,
                            'score': score,
                            'category': category
                        }
        else:
            text = st.text_area("Enter complaint text", height=200, value=st.session_state.get('ocr_text', ''))
            if text:
                st.session_state.ocr_text = text
                
                if st.button("🔍 Analyze", use_container_width=True):
                    sentiment, score = analyze_sentiment(text)
                    category = categorize_complaint(text)
                    
                    st.session_state.analysis_result = {
                        'text': text,
                        'sentiment': sentiment,
                        'score': score,
                        'category': category
                    }
    
    # Display results
    if st.session_state.get('analysis_result'):
        result = st.session_state.analysis_result
        
        st.markdown("---")
        st.markdown("### 📊 Analysis Results")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Sentiment", f"{result['sentiment'].upper()}")
            st.progress(min(result['score'], 1.0))
            st.caption(f"Confidence: {result['score']:.2f}")
        
        with col2:
            st.metric("Category", result['category'])
        
        with col3:
            priority = '🔴 High' if result['score'] > 0.7 else '🟡 Medium'
            st.metric("Priority", priority)
        
        # Generate ticket
        if st.button("🎫 Generate Ticket"):
            ticket_id = f"TS{datetime.now().strftime('%Y%m%d%H%M%S')}"
            ticket = {
                'ticket_id': ticket_id,
                'timestamp': datetime.now().isoformat(),
                'text': result['text'],
                'sentiment': result['sentiment'],
                'sentiment_score': result['score'],
                'category': result['category'],
                'status': 'new',
                'priority': 'high' if result['score'] > 0.7 else 'medium',
            }
            
            st.session_state.tickets.append(ticket)
            st.session_state.current_ticket = ticket
            save_tickets()
            
            # Telegram alert
            if telegram_enabled:
                send_telegram_alert(f"🔔 New Complaint\nID: {ticket_id}\nCategory: {result['category']}")
            
            st.success(f"✅ Ticket created: {ticket_id}")
            
            # Generate response
            if st.button("✍️ Generate Response"):
                response = generate_response(ticket)
                st.markdown("#### Suggested Response")
                st.markdown(response)
    
    # Custom templates section
    st.markdown("---")
    st.markdown("### 📝 Custom Templates")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Create New Template**")
        template_name = st.text_input("Template Name")
        template_content = st.text_area("Template Content", height=150, 
                                        placeholder="Use {category}, {ticket_id}, {sentiment} as placeholders")
        
        if st.button("💾 Save Template"):
            if template_name and template_content:
                st.session_state.templates[template_name] = {
                    'name': template_name,
                    'template': template_content
                }
                st.success(f"Template '{template_name}' saved!")
    
    with col2:
        st.markdown("**Existing Templates**")
        if st.session_state.templates:
            for name, template in st.session_state.templates.items():
                st.markdown(f"**{name}**")
                st.text_area("Template:", value=template['template'], height=100, key=f"tmpl_{name}")

if __name__ == "__main__":
    main()
