# automation/email_reader.py

import imaplib
import email

EMAIL = "you@example.com"
PASSWORD = "yourpassword"

def read_otp_from_email():
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(EMAIL, PASSWORD)
    imap.select("inbox")
    _, messages = imap.search(None, 'ALL')
    for num in messages[0].split()[-10:]:
        _, msg_data = imap.fetch(num, '(RFC822)')
        msg = email.message_from_bytes(msg_data[0][1])
        if "OTP" in msg["Subject"]:
            body = msg.get_payload(decode=True).decode()
            otp = ''.join(filter(str.isdigit, body))
            return otp
    return None
