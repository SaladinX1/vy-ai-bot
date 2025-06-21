from PIL import Image
import pyautogui
import datetime
import os

def take_screenshot(save_path="screenshot.png"):
    image = pyautogui.screenshot()
    image.save(save_path)
    return save_path
