import pytesseract
from PIL import ImageGrab
import cv2
import numpy as np

def capture_screen():
    # Capture écran entier (Windows, macOS)
    img = ImageGrab.grab()
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

def extract_text_from_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255,
                                   cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 11, 2)
    text = pytesseract.image_to_string(thresh, lang='fra+eng')
    return text.strip()

def get_screen_text():
    img = capture_screen()
    return extract_text_from_image(img)
