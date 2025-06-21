import pytesseract
from PIL import Image

# ⚠️ Pour Windows uniquement, décommente et modifie le chemin vers tesseract.exe
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text
