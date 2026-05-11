"""
Dark Tech Theme for AI Complaint Handler Pro
Professional gradient-based dark theme with animations
"""

def get_dark_tech_css():
    return """
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Roboto+Mono:wght@400;500&display=swap');
    
    /* Root Variables */
    :root {
        --bg-primary: #0a0e27;
        --bg-secondary: #1a1f3a;
        --bg-tertiary: #2d3561;
        --primary: #00f2ff;
        --secondary: #bd00ff;
        --accent: #00ff9d;
        --text-main: #ffffff;
        --text-muted: #a0a0a0;
        --success: #00ff9d;
        --warning: #ffbd00;
        --danger: #ff0066;
        --gradient-1: linear-gradient(135deg, #00f2ff 0%, #bd00ff 100%);
        --gradient-2: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
        --shadow-glow: 0 0 20px rgba(0, 242, 255, 0.3);
        --shadow-glow-purple: 0 0 20px rgba(189, 0, 255, 0.3);
    }
    
    /* Base Styles */
    .stApp {
        background: var(--gradient-2);
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Container */
    .main .block-container {
        background: rgba(26, 31, 58, 0.5);
        border-radius: 16px;
        padding: 2rem;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 242, 255, 0.1);
    }
    
    /* Gradient Header */
    .gradient-header {
        background: linear-gradient(135deg, rgba(0, 242, 255, 0.1) 0%, rgba(189, 0, 255, 0.1) 100%);
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(0, 242, 255, 0.2);
    }
    
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #00f2ff 0%, #bd00ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        text-shadow: 0 0 30px rgba(0, 242, 255, 0.3);
    }
    
    .subtitle {
        color: var(--text-muted);
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }
    
    .glow-effect {
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(0, 242, 255, 0.1) 0%, transparent 70%);
        animation: glow 3s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        0% { opacity: 0.5; transform: scale(1); }
        100% { opacity: 0.8; transform: scale(1.1); }
    }
    
    /* Feature Cards */
    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .feature-card {
        background: rgba(45, 53, 97, 0.5);
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid rgba(0, 242, 255, 0.1);
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        border-color: var(--primary);
        box-shadow: var(--shadow-glow);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    .feature-title {
        color: var(--text-main);
        font-size: 1.2rem;
        font-weight: 600;
        margin: 0.5rem 0;
    }
    
    .feature-desc {
        color: var(--text-muted);
        font-size: 0.9rem;
        margin: 0;
    }
    
    /* Buttons */
    .stButton > button {
        background: var(--gradient-1);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 242, 255, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 242, 255, 0.5);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Text Areas */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(10, 14, 39, 0.8);
        border: 1px solid rgba(0, 242, 255, 0.3);
        color: var(--text-main);
        border-radius: 8px;
        font-family: 'Roboto Mono', monospace;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary);
        box-shadow: 0 0 10px rgba(0, 242, 255, 0.2);
    }
    
    /* Metric Cards */
    [data-testid="stMetric"] {
        background: rgba(45, 53, 97, 0.5);
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid rgba(0, 242, 255, 0.1);
    }
    
    [data-testid="stMetricValue"] {
        color: var(--primary);
        font-size: 2rem;
        font-weight: 700;
    }
    
    [data-testid="stMetricLabel"] {
        color: var(--text-muted);
        font-size: 0.9rem;
    }
    
    /* Progress Bars */
    .stProgress > div > div {
        background: var(--gradient-1);
    }
    
    /* Selectboxes */
    .stSelectbox > div > div {
        background: rgba(10, 14, 39, 0.8);
        border: 1px solid rgba(0, 242, 255, 0.3);
        color: var(--text-main);
    }
    
    /* Radio buttons */
    .stRadio > div {
        background: rgba(45, 53, 97, 0.5);
        border-radius: 8px;
        padding: 0.5rem;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(45, 53, 97, 0.5);
        border: 1px solid rgba(0, 242, 255, 0.2);
        color: var(--text-main);
    }
    
    /* JSON Display */
    pre {
        background: rgba(10, 14, 39, 0.8);
        border: 1px solid rgba(0, 242, 255, 0.2);
        border-radius: 8px;
        padding: 1rem;
        color: var(--text-main);
        font-family: 'Roboto Mono', monospace;
    }
    
    /* Success/Error Messages */
    .stAlert {
        border-radius: 8px;
        border: 1px solid;
    }
    
    .stAlert[data-baseweb="notification"] {
        background: rgba(0, 255, 157, 0.1);
        border-color: var(--success);
        color: var(--success);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: var(--text-muted);
        border-top: 1px solid rgba(0, 242, 255, 0.1);
        margin-top: 2rem;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .main .block-container > div {
        animation: fadeIn 0.5s ease-out;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-primary);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--bg-tertiary);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--primary);
    }
    
    /* Chart containers */
    .element-container:has([aria-label="Bar chart"]) {
        background: rgba(45, 53, 97, 0.3);
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid rgba(0, 242, 255, 0.1);
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .main-title {
            font-size: 1.8rem;
        }
        
        .features-grid {
            grid-template-columns: 1fr;
        }
    }
    </style>
    """
