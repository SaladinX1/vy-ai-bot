import imaplib
import email
from email.header import decode_header
import webbrowser
import re

class EmailReader:
    def __init__(self, imap_server, email_user, email_pass):
        self.imap_server = imap_server
        self.email_user = email_user
        self.email_pass = email_pass
        self.mail = None

    def connect(self):
        self.mail = imaplib.IMAP4_SSL(self.imap_server)
        self.mail.login(self.email_user, self.email_pass)
        self.mail.select("inbox")

    def search_emails(self, subject_contains=None, from_contains=None):
        criteria = []
        if subject_contains:
            criteria.append(f'(SUBJECT "{subject_contains}")')
        if from_contains:
            criteria.append(f'(FROM "{from_contains}")')
        if not criteria:
            criteria = ['ALL']
        query = ' '.join(criteria)
        status, messages = self.mail.search(None, query)
        email_ids = messages[0].split()
        return email_ids

    def fetch_email(self, email_id):
        status, msg_data = self.mail.fetch(email_id, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                return msg
        return None

    def get_email_body(self, msg):
        if msg.is_multipart():
            for part in msg.walk():
                ctype = part.get_content_type()
                cdispo = str(part.get('Content-Disposition'))
                if ctype == 'text/plain' and 'attachment' not in cdispo:
                    return part.get_payload(decode=True).decode('utf-8', errors='ignore')
        else:
            return msg.get_payload(decode=True).decode('utf-8', errors='ignore')
        return ""

    def find_code(self, text, regex=r'\b\d{4,8}\b'):
        # Trouve des codes à 4-8 chiffres (modifiable selon besoin)
        matches = re.findall(regex, text)
        return matches[0] if matches else None

    def logout(self):
        self.mail.logout()

if __name__ == "__main__":
    import os
    EMAIL = os.getenv("BUSINESS_EMAIL")
    PASSWORD = os.getenv("BUSINESS_EMAIL_PASS")
    IMAP_SERVER = "imap.gmail.com"  # Modifier selon fournisseur email

    reader = EmailReader(IMAP_SERVER, EMAIL, PASSWORD)
    reader.connect()
    email_ids = reader.search_emails(subject_contains="confirmation")
    for eid in email_ids[-5:]:  # Derniers 5 emails
        msg = reader.fetch_email(eid)
        body = reader.get_email_body(msg)
        print("Email body:", body)
        code = reader.find_code(body)
        if code:
            print(f"Code trouvé: {code}")
    reader.logout()
