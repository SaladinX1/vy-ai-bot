import smtplib
from email.message import EmailMessage
import json
import time

ALERT_EMAIL = "toi@example.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "ton.email@gmail.com"
SMTP_PASS = "tonpassword"

def send_alert(subject, content):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = ALERT_EMAIL
    msg.set_content(content)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(SMTP_USER, SMTP_PASS)
        smtp.send_message(msg)
    print("⚠️ Alerte envoyée par email.")

def check_logs(log_path="logs/system.log"):
    with open(log_path, "r") as f:
        lines = f.readlines()
    errors = [line for line in lines if "ERROR" in line or "Exception" in line]
    if errors:
        send_alert("Erreur détectée dans le système", "\n".join(errors[-10:]))

if __name__ == "__main__":
    while True:
        check_logs()
        time.sleep(3600)  # Vérifier toutes les heures
