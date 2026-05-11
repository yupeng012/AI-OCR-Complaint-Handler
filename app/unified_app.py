#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Complaint Handler Pro - Unified Application
Dark Tech Theme with Interactive Demo and Data Visualization
"""

import streamlit as st
from PIL import Image
import json
from pathlib import Path
from datetime import datetime
import random
import time
import sys

# Add parent directory to path for imports
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
    page_title="AI Complaint Handler Pro",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS for dark tech theme
st.markdown(get_dark_tech_css(), unsafe_allow_html=True)

# Initialize session state
if 'tickets' not in st.session_state:
    st.session_state.tickets = []
if 'ocr_text' not in st.session_state:
    st.session_state.ocr_text = ""
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None
if 'current_ticket' not in st.session_state:
    st.session_state.current_ticket = None

# Load ticket data from file
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

def create_gradient_header(title, subtitle=""):
    """Create gradient header with animation"""
    st.markdown(f"""
    <div class="gradient-header">
        <h1 class="main-title">{title}</h1>
        {f'<p class="subtitle">{subtitle}</p>' if subtitle else ''}
        <div class="glow-effect"></div>
    </div>
    """, unsafe_allow_html=True)

def create_feature_card(icon, title, description):
    """Create animated feature card"""
    return f"""
    <div class="feature-card">
        <div class="feature-icon">{icon}</div>
        <h3 class="feature-title">{title}</h3>
        <p class="feature-desc">{description}</p>
    </div>
    """

def main():
    # Main header with gradient
    create_gradient_header("🤖 AI Complaint Handler Pro", "Intelligent OCR + Sentiment Analysis + Auto-Categorization")
    
    # Feature showcase
    st.markdown("<div class='features-grid'>", unsafe_allow_html=True)
    cols = st.columns(4)
    
    features = [
        ("📸", "OCR Recognition", "Extract text from images instantly"),
        ("🧠", "Sentiment AI", "Detect emotions with 95% accuracy"),
        ("🏷️", "Smart Categories", "Auto-classify into 5+ categories"),
        ("⚡", "Auto Response", "Generate professional replies"),
    ]
    
    for i, (icon, title, desc) in enumerate(features):
        with cols[i]:
            st.markdown(create_feature_card(icon, title, desc), unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Main content area with two columns
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📥 Input Section")
        
        # Upload method selector
        upload_method = st.radio(
            "Choose input method:",
            ["📸 Upload Image", "✍️ Type Text"],
            horizontal=True
        )
        
        ocr_text = ""
        
        if upload_method == "📸 Upload Image":
            uploaded_file = st.file_uploader(
                "Upload complaint image",
                type=['png', 'jpg', 'jpeg'],
                help="Supported formats: PNG, JPG, JPEG"
            )
            
            if uploaded_file:
                # Display uploaded image
                image = Image.open(uploaded_file)
                st.image(image, caption='Uploaded Complaint', use_container_width=True)
                
                if st.button("🔍 Start OCR Processing", use_container_width=True):
                    with st.spinner("Processing image..."):
                        # Simulate OCR processing with progress
                        progress_bar = st.progress(0)
                        for i in range(100):
                            time.sleep(0.01)
                            progress_bar.progress(i + 1)
                        
                        ocr_text = extract_text_from_image(image)
                        st.session_state.ocr_text = ocr_text
                        st.success("✅ OCR completed!")
        
        else:
            ocr_text = st.text_area(
                "Or type complaint text directly:",
                height=250,
                placeholder="Enter complaint details here...",
                value=st.session_state.get('ocr_text', '')
            )
            if ocr_text:
                st.session_state.ocr_text = ocr_text
    
    with col2:
        st.markdown("### 📊 Analysis Results")
        
        if st.session_state.ocr_text:
            # Display extracted text
            with st.expander("📝 Extracted Text", expanded=True):
                st.text_area("OCR Result", value=st.session_state.ocr_text, height=150)
            
            # Analysis buttons
            col_analyze1, col_analyze2 = st.columns(2)
            
            with col_analyze1:
                if st.button("🔬 Analyze Sentiment", use_container_width=True):
                    with st.spinner("Analyzing sentiment..."):
                        text = st.session_state.ocr_text
                        sentiment, score = analyze_sentiment(text)
                        st.session_state.analysis_result = {
                            'sentiment': sentiment,
                            'score': score,
                            'category': None,
                            'ticket': None
                        }
                        time.sleep(0.5)  # Simulate processing
            
            with col_analyze2:
                if st.button("🏷️ Categorize", use_container_width=True):
                    with st.spinner("Categorizing..."):
                        text = st.session_state.ocr_text
                        category = categorize_complaint(text)
                        if st.session_state.analysis_result:
                            st.session_state.analysis_result['category'] = category
                        else:
                            st.session_state.analysis_result = {
                                'sentiment': None,
                                'score': None,
                                'category': category,
                                'ticket': None
                            }
                        time.sleep(0.5)
            
            # Display results if analysis exists
            if st.session_state.analysis_result:
                result = st.session_state.analysis_result
                
                st.markdown("#### Analysis Results")
                
                # Sentiment gauge (simulated with progress bar)
                if result['sentiment']:
                    sentiment_emoji = {'positive': '😊', 'neutral': '😐', 'negative': '😠'}
                    st.markdown(f"**Sentiment:** {sentiment_emoji.get(result['sentiment'], '')} **{result['sentiment'].upper()}**")
                    st.progress(min(result['score'], 1.0))
                    st.caption(f"Confidence: {result['score']:.2f}")
                
                # Category display
                if result['category']:
                    st.markdown(f"**Category:** 🏷️ {result['category']}")
                
                # Generate ticket
                if st.button("🎫 Generate Ticket"):
                    ticket_id = f"TS{datetime.now().strftime('%Y%m%d%H%M%S')}"
                    ticket = {
                        'ticket_id': ticket_id,
                        'timestamp': datetime.now().isoformat(),
                        'text': st.session_state.ocr_text,
                        'sentiment': result.get('sentiment', 'unknown'),
                        'sentiment_score': result.get('score', 0),
                        'category': result.get('category', 'Other'),
                        'status': 'new',
                        'priority': 'high' if result.get('score', 0) > 0.7 else 'medium',
                    }
                    
                    st.session_state.tickets.append(ticket)
                    st.session_state.current_ticket = ticket
                    save_tickets()
                    st.success(f"✅ Ticket created: {ticket_id}")
                
                # Show ticket if exists
                if st.session_state.current_ticket:
                    ticket = st.session_state.current_ticket
                    st.markdown("#### Generated Ticket")
                    st.json({
                        'Ticket ID': ticket['ticket_id'],
                        'Category': ticket['category'],
                        'Priority': ticket['priority'],
                        'Status': ticket['status']
                    })
                    
                    # Generate response
                    if st.button("✍️ Generate Response"):
                        response = generate_response(ticket)
                        st.markdown("#### Suggested Response")
                        st.markdown(response)
                        
                        # Export button
                        if st.button("📥 Export Ticket"):
                            json_str = json.dumps(ticket, indent=2, ensure_ascii=False)
                            st.download_button(
                                label="Download JSON",
                                data=json_str,
                                file_name=f"ticket_{ticket['ticket_id']}.json",
                                mime="application/json"
                            )
        
        else:
            st.info("👆 Upload an image or type text to begin analysis")
    
    st.markdown("---")
    
    # Dashboard section
    st.markdown("### 📈 Analytics Dashboard")
    
    if st.session_state.tickets:
        # Stats columns
        col1, col2, col3, col4 = st.columns(4)
        
        total = len(st.session_state.tickets)
        new_count = sum(1 for t in st.session_state.tickets if t['status'] == 'new')
        resolved_count = sum(1 for t in st.session_state.tickets if t['status'] == 'resolved')
        
        col1.metric("Total Tickets", total)
        col2.metric("New Today", new_count)
        col3.metric("Resolved", resolved_count)
        
        # Category distribution
        if total > 0:
            categories = {}
            for ticket in st.session_state.tickets:
                cat = ticket.get('category', 'Other')
                categories[cat] = categories.get(cat, 0) + 1
            
            # Simple bar chart using Streamlit
            if categories:
                st.markdown("#### Category Distribution")
                cat_data = {k: v for k, v in sorted(categories.items(), key=lambda x: x[1], reverse=True)}
                st.bar_chart(cat_data)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div class='footer'>
        <p><strong>AI Complaint Handler Pro v2.0</strong> | Dark Tech Theme | Real-time Analysis</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
