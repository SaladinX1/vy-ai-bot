# execution/keyboard_control.py

from pynput.keyboard import Controller
import time
import random

keyboard = Controller()

def type_text(text: str, min_delay: float = 0.05, max_delay: float = 0.2, start_delay: float = 0.5) -> None:
    """
    Simule la frappe d'un texte caractère par caractère.
    
    Args:
        text (str): le texte à taper.
        min_delay (float): délai minimum entre chaque caractère.
        max_delay (float): délai maximum entre chaque caractère.
        start_delay (float): délai avant de commencer à taper.
    """
    time.sleep(start_delay)
    for ch in text:
        keyboard.type(ch)
        time.sleep(random.uniform(min_delay, max_delay))
