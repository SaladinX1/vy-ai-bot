import smtplib
from email.mime.text import MIMEText

def send_feedback_report(to_email):
    try:
        with open("logs/feedback.csv") as f:
            content = f.read()
    except FileNotFoundError:
        content = "Aucun feedback reçu."

    msg = MIMEText(content)
    msg["Subject"] = "Rapport Feedback Workflows"
    msg["From"] = "monbot@autobot.com"
    msg["To"] = to_email

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login("VOTRE_EMAIL@gmail.com", "VOTRE_MDP_APP")
        smtp.send_message(msg)

# Pour lancer une fois : send_feedback_report("ton@mail.com")
