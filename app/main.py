#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI-OCR Complaint Handler Demo
OCR + Sentiment Analysis + Auto-categorization
"""

import streamlit as st
from PIL import Image
import io
import json
from pathlib import Path
from datetime import datetime

# Mock OCR and sentiment analysis (replace with real APIs)
def extract_text_from_image(image):
    """Mock OCR - replace with PaddleOCR or similar"""
    return """
    投诉单号：TS20260511001
    投诉日期：2026-05-10
    客户姓名：张三
    联系方式：138****1234
    
    投诉内容：
    本人于 2026 年 5 月 8 日在贵公司官网购买了一台笔记本电脑，
    收到货后发现屏幕有严重漏光问题，且开机速度极慢。
    联系客服要求退换货，但被告知需要自行检测并出具报告。
    此行为严重侵害了消费者权益，要求立即处理并给予合理解释。
    
    投诉诉求：
    1. 立即办理退换货
    2. 赔偿交通费误工费共计 500 元
    3. 书面道歉
    """

def analyze_sentiment(text):
    """Mock sentiment analysis - replace with API"""
    keywords = ['严重', '问题', '侵害', '投诉', '赔偿']
    count = sum(1 for kw in keywords if kw in text)
    
    if count >= 4:
        return 'negative', 0.85
    elif count >= 2:
        return 'neutral', 0.45
    else:
        return 'positive', 0.25

def categorize_complaint(text):
    """Auto-categorize complaint"""
    categories = {
        '产品质量': ['质量', '问题', '故障', '损坏', '漏光'],
        '客户服务': ['客服', '态度', '服务', '联系'],
        '物流配送': ['物流', '快递', '配送', '发货'],
        '退款退货': ['退款', '退货', '换货', '退换'],
    }
    
    scores = {}
    for cat, words in categories.items():
        scores[cat] = sum(1 for word in words if word in text)
    
    top_cat = max(scores, key=scores.get)
    return top_cat if scores[top_cat] > 0 else '其他'

def generate_response(complaint_data):
    """Generate suggested response"""
    return f"""
## 建议回复方案

**投诉类型**: {complaint_data.get('category', '未分类')}
**紧急程度**: {'高' if complaint_data.get('sentiment_score', 0) > 0.7 else '中' if complaint_data.get('sentiment_score', 0) > 0.4 else '低'}

### 回复要点：
1. 首先对客户表示诚挚歉意
2. 说明公司将立即调查处理
3. 提供具体解决方案和时间表
4. 提供进一步沟通渠道

### 参考话术：
> 尊敬的{complaint_data.get('customer', '客户')}先生/女士：
> 
> 非常抱歉给您带来了不便！我们已收到您的投诉，高度重视您反映的问题。
> 我们将立即安排专人调查处理，并在 24 小时内给予回复。
> 如有任何进展，我们会第一时间通过{complaint_data.get('contact', '预留联系方式')}与您联系。
> 
> 感谢您的理解与支持！
"""

# Streamlit UI
st.set_page_config(page_title="AI 智能投诉处理系统", layout="wide")

st.title("🤖 AI 智能投诉处理系统 Demo")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("操作面板")
    upload_method = st.radio("选择输入方式", ["上传图片", "输入文本"])
    st.markdown("**功能特点**:")
    st.markdown("- OCR 文字识别")
    st.markdown("- 情感倾向分析")
    st.markdown("- 智能分类")
    st.markdown("- 自动生成回复")

# Main content
col1, col2 = st.columns(2)

complaint_data = {}

with col1:
    st.subheader("📥 输入区")
    
    if upload_method == "上传图片":
        uploaded_file = st.file_uploader("上传投诉单图片", type=['png', 'jpg', 'jpeg'])
        
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption='上传的投诉单', use_container_width=True)
            
            if st.button("开始识别"):
                with st.spinner("正在识别文字..."):
                    extracted_text = extract_text_from_image(image)
                    st.session_state['extracted_text'] = extracted_text
                    st.success("识别完成！")
    else:
        extracted_text = st.text_area("或直接输入投诉内容", height=300)
        if extracted_text:
            st.session_state['extracted_text'] = extracted_text

# Process and display results
if 'extracted_text' in st.session_state:
    text = st.session_state['extracted_text']
    
    # Extract info (mock)
    complaint_data = {
        'text': text,
        'customer': '张三',
        'contact': '138****1234',
        'date': '2026-05-10',
    }
    
    # Analyze
    sentiment, sentiment_score = analyze_sentiment(text)
    category = categorize_complaint(text)
    
    complaint_data['sentiment'] = sentiment
    complaint_data['sentiment_score'] = sentiment_score
    complaint_data['category'] = category
    
    with col2:
        st.subheader("📊 分析结果")
        
        # Display extracted text
        with st.expander("📝 识别的文字内容", expanded=True):
            st.text_area("OCR 结果", value=text, height=200)
        
        # Analysis results
        st.markdown("**情感分析**:")
        sentiment_emoji = {'positive': '😊', 'neutral': '😐', 'negative': '😠'}
        st.write(f"{sentiment_emoji.get(sentiment, '')} {sentiment.upper()} (置信度：{sentiment_score:.2f})")
        
        st.markdown("**投诉分类**:")
        st.write(f"🏷️ {category}")
        
        # Generate response
        st.markdown("---")
        if st.button("生成回复建议"):
            response = generate_response(complaint_data)
            st.session_state['response'] = response
        
        if 'response' in st.session_state:
            st.markdown(st.session_state['response'])
            
            if st.button("📥 导出报告"):
                report = {
                    'timestamp': datetime.now().isoformat(),
                    'complaint': complaint_data,
                    'response': st.session_state['response']
                }
                json_str = json.dumps(report, ensure_ascii=False, indent=2)
                st.download_button(
                    label="下载报告",
                    data=json_str,
                    file_name=f"complaint_report_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                    mime="application/json"
                )

# Footer
st.markdown("---")
st.markdown("**AI-OCR-Complaint-Handler v1.0** | 基于 OCR+ 情感分析+ 自动分类")
