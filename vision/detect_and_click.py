import pytesseract
import cv2
import pyautogui

def find_text_position(image_path, target_text):
    image = cv2.imread(image_path)
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

    for i in range(len(data['text'])):
        word = data['text'][i]
        if target_text.lower() in word.lower():
            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            return (x + w // 2, y + h // 2)  # Coordonnée centrale du mot

    return None

def click_on_text(image_path, target_text):
    pos = find_text_position(image_path, target_text)
    if pos:
        pyautogui.moveTo(pos[0], pos[1])
        pyautogui.click()
        print(f"🖱️ Clic effectué sur : {target_text}")
    else:
        print(f"❌ Texte non trouvé à l’écran : {target_text}")
