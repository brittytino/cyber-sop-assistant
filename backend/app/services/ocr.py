import pytesseract
from PIL import Image
import io
import logging

logger = logging.getLogger(__name__)

# If tesseract is not in PATH, uncomment and set the path
# pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def extract_text_from_image(image_bytes: bytes) -> str:
    """
    Extract text from an image using OCR
    Attempts to use English + Hindi if available
    """
    try:
        image = Image.open(io.BytesIO(image_bytes))
        
        # Try to use multiple languages if installed
        # eng = English, hin = Hindi, tam = Tamil, te = Telugu, etc.
        # But standard installations might only have eng.
        # Let's try 'eng+hin' and fallback to 'eng'
        
        try:
            text = pytesseract.image_to_string(image, lang='eng+hin')
        except:
            # Fallback to just english if hindi trained data not found
            text = pytesseract.image_to_string(image)
            
        return text.strip()
    except Exception as e:
        logger.error(f"Error extracting text from image: {e}")
        return ""
