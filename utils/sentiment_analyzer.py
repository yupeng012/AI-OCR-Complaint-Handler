"""
Sentiment Analyzer - Emotion Detection
Analyzes text sentiment (positive/neutral/negative)
"""

def analyze_sentiment(text):
    """
    Analyze sentiment of text
    
    Args:
        text: Input text to analyze
    
    Returns:
        tuple: (sentiment_label, confidence_score)
               sentiment_label: 'positive', 'neutral', or 'negative'
               confidence_score: float 0-1
    """
    # Negative keywords (English and Chinese)
    negative_keywords = [
        'severe', 'serious', 'problem', 'complaint', 'terrible', 'awful',
        'rude', 'infringe', 'compensation', 'scratch', 'defect', 'broken',
        'angry', 'disappointed', 'worst', 'horrible', 'useless',
        '严重', '问题', '投诉', '恶劣', '推诿', '侵害', '赔偿', '划痕', 
        '不足', '差劲', '失望', '糟糕', '垃圾', '愤怒'
    ]
    
    # Positive keywords
    positive_keywords = [
        'satisfied', 'thank', 'excellent', 'professional', 'timely',
        'great', 'awesome', 'helpful', 'perfect', 'love',
        '满意', '感谢', '好评', '优秀', '专业', '及时', '很好', '棒'
    ]
    
    # Count occurrences
    neg_count = sum(1 for kw in negative_keywords if kw.lower() in text.lower())
    pos_count = sum(1 for kw in positive_keywords if kw.lower() in text.lower())
    
    # Determine sentiment
    if neg_count >= 4:
        return 'negative', min(0.95, 0.70 + neg_count * 0.05)
    elif neg_count >= 2:
        return 'negative', min(0.90, 0.60 + neg_count * 0.05)
    elif neg_count >= 1:
        return 'neutral', 0.50
    elif pos_count >= 2:
        return 'positive', min(0.95, 0.60 + pos_count * 0.05)
    elif pos_count == 1:
        return 'positive', 0.65
    else:
        return 'neutral', 0.50

def analyze_sentiment_detailed(text):
    """
    Detailed sentiment analysis with scores
    
    Args:
        text: Input text
    
    Returns:
        dict: Detailed analysis results
    """
    sentiment, score = analyze_sentiment(text)
    
    return {
        'sentiment': sentiment,
        'confidence': score,
        'polarity': score if sentiment == 'positive' else (-score if sentiment == 'negative' else 0),
        'subjectivity': 0.8  # Placeholder
    }

if __name__ == "__main__":
    # Test sentiment analysis
    test_texts = [
        "This product is terrible and the service was rude. I want compensation!",
        "非常满意，感谢你们的专业服务！",
        "The product is okay, nothing special."
    ]
    
    print("Sentiment Analysis Test:\n")
    for text in test_texts:
        sentiment, score = analyze_sentiment(text)
        print(f"Text: {text[:50]}...")
        print(f"Sentiment: {sentiment.upper()} (Confidence: {score:.2f})\n")
