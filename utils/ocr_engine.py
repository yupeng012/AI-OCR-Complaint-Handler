"""
OCR Engine - Text Extraction from Images
Supports PaddleOCR (production) and mock OCR (demo)
"""

from PIL import Image
import io

# Try to import PaddleOCR, fall back to mock if not available
try:
    from paddleocr import PaddleOCR
    PADDLE_AVAILABLE = True
except ImportError:
    PADDLE_AVAILABLE = False
    print("⚠️  PaddleOCR not available, using mock OCR for demo")

# Initialize OCR engine
if PADDLE_AVAILABLE:
    ocr_engine = PaddleOCR(use_angle_cls=True, lang='ch')
else:
    ocr_engine = None

# Mock OCR text for demo
MOCK_TEXT = """Complaint Ticket #TS20260511002
Date: May 11, 2026
Customer: John Smith
Contact: 139****5678

Complaint Details:
I purchased a smartphone from your Tmall flagship store on May 9, 2026. 
Upon receipt, I discovered scratches on the screen and severely inadequate 
battery life. When I contacted online customer service requesting a return 
or exchange, the representative was rude and shifted blame. This behavior 
serely infringes on consumer rights. I demand immediate resolution.

Demands:
1. Immediate return or exchange
2. Compensation of 1000 CNY
3. Training and apology from customer service staff
"""

def extract_text_from_image(image):
    """
    Extract text from image using OCR
    
    Args:
        image: PIL Image object or file path
    
    Returns:
        str: Extracted text
    """
    if ocr_engine:
        # Use PaddleOCR for production
        try:
            if isinstance(image, Image.Image):
                # Convert PIL Image to numpy array
                import numpy as np
                img_array = np.array(image)
                result = ocr_engine.ocr(img_array, cls=True)
            else:
                result = ocr_engine.ocr(image, cls=True)
            
            if result and len(result) > 0:
                texts = []
                for line in result[0]:
                    if line:
                        texts.append(line[1][0])
                return '\n'.join(texts)
        except Exception as e:
            print(f"OCR Error: {e}")
            return MOCK_TEXT
    else:
        # Mock OCR for demo
        return MOCK_TEXT

def extract_text_from_path(image_path):
    """
    Extract text from image file path
    
    Args:
        image_path: Path to image file
    
    Returns:
        str: Extracted text
    """
    return extract_text_from_image(image_path)

if __name__ == "__main__":
    # Test OCR
    print("Testing OCR Engine...")
    if PADDLE_AVAILABLE:
        print("✓ PaddleOCR available")
    else:
        print("⚠ Using mock OCR")
    
    # Test with mock
    print("\nMock OCR Result:")
    print(MOCK_TEXT[:200] + "...")
