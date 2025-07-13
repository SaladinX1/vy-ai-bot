import cv2
import pytesseract
import torch

class UIDetector:
    def __init__(self, model_path="models/yolo_ui_detection.pt"):
        try:
            self.model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path, force_reload=False)
        except Exception as e:
            print(f"❌ Erreur chargement modèle YOLO: {e}")
            self.model = None

    def detect_elements(self, screenshot_path):
        if self.model is None:
            return []
        img = cv2.imread(screenshot_path)
        if img is None:
            print(f"❌ Image introuvable: {screenshot_path}")
            return []
        results = self.model(img)

        detected = []
        for *box, conf, cls in results.xyxy[0].tolist():
            x1, y1, x2, y2 = map(int, box)
            label = self.model.names[int(cls)]
            detected.append({
                "label": label,
                "confidence": conf,
                "bbox": (x1, y1, x2, y2)
            })
        return detected

    def extract_text(self, screenshot_path):
        img = cv2.imread(screenshot_path)
        if img is None:
            return ""
        return pytesseract.image_to_string(img).strip()
