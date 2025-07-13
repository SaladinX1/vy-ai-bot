import cv2
import pytesseract

def extract_text_from_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        return ""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    processed = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    return pytesseract.image_to_string(processed, config='--psm 6').strip()

def detect_element(image_path, element_text):
    text_data = extract_text_from_image(image_path)
    return element_text.lower() in text_data.lower()
