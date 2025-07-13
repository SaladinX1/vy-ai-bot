import smtplib
from email.message import EmailMessage


def send_alert(subject, body):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = "bot@autobot.com"
    msg['To'] = "admin@example.com"
    with smtplib.SMTP('localhost') as server:
        server.send_message(msg)

def alert_on_error(error_msg):
    print(f"⚠️ Envoi d'alerte pour l'erreur : {error_msg}")
    send_alert("Erreur dans workflow", error_msg, "destinataire@example.com")





