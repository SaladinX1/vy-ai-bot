import pytesseract
from PIL import Image

def ocr_image(image_path):
    try:
        text = pytesseract.image_to_string(Image.open(image_path))
        return text.strip()
    except Exception as e:
        return f"Erreur OCR: {e}"
