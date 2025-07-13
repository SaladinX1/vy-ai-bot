
import requests
from utils.logger import append_log

API_KEY_2CAPTCHA = "YOUR_2CAPTCHA_API_KEY"

def solve_captcha(image_base64):
    # Envoi à 2Captcha
    try:
        resp = requests.post("http://2captcha.com/in.php", data={
            "key": API_KEY_2CAPTCHA,
            "method": "base64",
            "body": image_base64,
            "json": 1
        })
        request_id = resp.json().get("request")
        # Polling pour récupérer la solution
        for _ in range(20):
            res = requests.get(f"http://2captcha.com/res.php?key={API_KEY_2CAPTCHA}&action=get&id={request_id}&json=1")
            if res.json().get("status") == 1:
                solution = res.json().get("request")
                append_log("[CaptchaSolver] Captcha résolu.")
                return solution
            time.sleep(5)
        append_log("[CaptchaSolver] Échec résolution captcha.")
    except Exception as e:
        append_log(f"[CaptchaSolver] Exception: {e}")
    return None
