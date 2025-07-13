import pytesseract
from PIL import Image
import cv2
import numpy as np
import pyautogui

def screenshot():
    return pyautogui.screenshot()

def preprocess_image(pil_img):
    img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 11, 2)
    return thresh

def extract_text_from_screen():
    img = screenshot()
    processed = preprocess_image(img)
    text = pytesseract.image_to_string(processed, lang='fra')
    return text.strip()
