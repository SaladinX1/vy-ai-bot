from PIL import Image
import pyautogui
import os

def take_screenshot(save_path="screenshot.png"):
    image = pyautogui.screenshot()
    os.makedirs(os.path.dirname(save_path), exist_ok=True) if os.path.dirname(save_path) else None
    image.save(save_path)
    return save_path
