# 4. email_reader.py (dans /email)
import imaplib
import email

def check_email_code(email_address, password, keyword="Code"):
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(email_address, password)
    mail.select("inbox")
    typ, data = mail.search(None, "ALL")
    ids = data[0].split()
    latest_id = ids[-1]
    typ, msg_data = mail.fetch(latest_id, "(RFC822)")
    raw_email = msg_data[0][1]
    msg = email.message_from_bytes(raw_email)
    if keyword in msg.get_payload():
        return msg.get_payload()
    return None

# ---