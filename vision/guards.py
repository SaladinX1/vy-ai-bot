# vision/guards.py

from vision.ocr import extract_text
from vision.screen_capture import take_screenshot

def detect_blockers():
    text = extract_text(take_screenshot())
    if "captcha" in text.lower() or "robot" in text.lower():
        return True
    return False
