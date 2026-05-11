"""
Complaint Categorizer - Auto Classification
Automatically categorizes complaints into predefined categories
"""

def categorize_complaint(text):
    """
    Categorize complaint into predefined categories
    
    Args:
        text: Complaint text
    
    Returns:
        str: Category name
    """
    # Category definitions with keywords
    categories = {
        'Product Quality': [
            'quality', 'defect', 'broken', 'damage', 'scratch', 'malfunction',
            'not working', 'faulty', 'poor quality', 'durability',
            '质量', '缺陷', '损坏', '故障', '划痕', '坏', '问题', '不良'
        ],
        'Customer Service': [
            'service', 'rude', 'attitude', 'unprofessional', 'helpful',
            'support', 'representative', 'staff', 'training',
            '服务', '态度', '客服', '差劲', '粗鲁', '不专业', '培训'
        ],
        'Shipping & Logistics': [
            'shipping', 'delivery', 'logistics', 'late', 'delay', 'package',
            'courier', 'tracking', 'lost', 'damaged in transit',
            '物流', '快递', '配送', '延误', '发货', '包裹', '运输'
        ],
        'Refund & Return': [
            'refund', 'return', 'exchange', 'money back', 'replacement',
            '退货', '退款', '换货', '退换', '返还', '赔偿'
        ],
        'False Advertising': [
            'false', 'misleading', 'advertisement', 'description', 'not as described',
            'expectation', 'promise', 'claim',
            '虚假', '宣传', '误导', '不符', '描述', '承诺'
        ]
    }
    
    # Score each category
    scores = {}
    text_lower = text.lower()
    
    for category, keywords in categories.items():
        score = sum(1 for kw in keywords if kw.lower() in text_lower)
        scores[category] = score
    
    # Get highest scoring category
    if max(scores.values()) > 0:
        top_category = max(scores, key=scores.get)
        return top_category
    else:
        return 'Other'

def categorize_with_confidence(text):
    """
    Categorize with confidence scores
    
    Args:
        text: Complaint text
    
    Returns:
        dict: Category with confidence scores
    """
    categories = {
        'Product Quality': [
            'quality', 'defect', 'broken', 'damage', 'scratch', 'malfunction',
            '质量', '缺陷', '损坏', '故障', '划痕'
        ],
        'Customer Service': [
            'service', 'rude', 'attitude', 'unprofessional',
            '服务', '态度', '客服', '差劲'
        ],
        'Shipping & Logistics': [
            'shipping', 'delivery', 'logistics', 'late', 'delay',
            '物流', '快递', '配送', '延误'
        ],
        'Refund & Return': [
            'refund', 'return', 'exchange', 'money back',
            '退货', '退款', '换货'
        ],
        'False Advertising': [
            'false', 'misleading', 'advertisement', 'not as described',
            '虚假', '宣传', '误导', '不符'
        ]
    }
    
    scores = {}
    total_matches = 0
    text_lower = text.lower()
    
    for category, keywords in categories.items():
        score = sum(1 for kw in keywords if kw.lower() in text_lower)
        scores[category] = score
        total_matches += score
    
    # Calculate confidence
    confidence = {}
    for category, score in scores.items():
        if total_matches > 0:
            confidence[category] = score / total_matches
        else:
            confidence[category] = 0
    
    return {
        'category': max(scores, key=scores.get) if max(scores.values()) > 0 else 'Other',
        'scores': scores,
        'confidence': confidence
    }

if __name__ == "__main__":
    # Test categorization
    test_texts = [
        "The product quality is terrible, very broken and defective.",
        "Customer service was rude and unprofessional.",
        "Shipping was delayed and package arrived damaged.",
        "I want a refund and return my money.",
        "Advertisement was false and misleading."
    ]
    
    print("Categorization Test:\n")
    for text in test_texts:
        category = categorize_complaint(text)
        print(f"Text: {text[:50]}...")
        print(f"Category: {category}\n")
