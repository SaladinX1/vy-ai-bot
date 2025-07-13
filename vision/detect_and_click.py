import pytesseract
import cv2
import pyautogui
from difflib import SequenceMatcher


def find_text_position(image_path, target_text, threshold=0.6):
    image = cv2.imread(image_path)
    if image is None:
        print(f"❌ Image introuvable ou illisible : {image_path}")
        return None

    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

    best_match = None
    best_score = 0.0

    for i, word in enumerate(data['text']):
        if not word.strip():
            continue
        score = SequenceMatcher(None, word.lower(), target_text.lower()).ratio()
        if score > best_score and score >= threshold:
            x = data['left'][i]
            y = data['top'][i]
            w = data['width'][i]
            h = data['height'][i]
            best_match = (x + w // 2, y + h // 2)
            best_score = score

    return best_match


def click_on_text(image_path, target_text):
    pos = find_text_position(image_path, target_text)
    if pos:
        pyautogui.moveTo(pos[0], pos[1])
        pyautogui.click()
        print(f"🖱️ Clic effectué sur (approx) : '{target_text}' en {pos}")
    else:
        print(f"❌ Texte non trouvé (même flou) : '{target_text}'")
