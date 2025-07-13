import time
import pyautogui
from vision.ui_detector import wait_for_image, click_on_image

class GumroadBot:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def open_gumroad_signup(self):
        # Ouvre le navigateur sur la page d’inscription
        import webbrowser
        webbrowser.open("https://gumroad.com/signup")
        time.sleep(5)

    def signup(self):
        self.open_gumroad_signup()
        # Attend champs email
        if wait_for_image("images/email_field.png", timeout=10):
            pyautogui.click(pyautogui.locateCenterOnScreen("images/email_field.png"))
            pyautogui.write(self.email)
            time.sleep(1)

        if wait_for_image("images/password_field.png", timeout=10):
            pyautogui.click(pyautogui.locateCenterOnScreen("images/password_field.png"))
            pyautogui.write(self.password)
            time.sleep(1)

        # Cliquer bouton Signup
        if wait_for_image("images/signup_button.png", timeout=10):
            click_on_image("images/signup_button.png")
            time.sleep(5)

        # Ici tu peux ajouter la gestion des emails de confirmation avec email_reader.py

    def upload_product(self, product_path):
        # A compléter selon UI Gumroad : navigation + upload fichier
        pass

if __name__ == "__main__":
    bot = GumroadBot("monemail@example.com", "monpassword123")
    bot.signup()
