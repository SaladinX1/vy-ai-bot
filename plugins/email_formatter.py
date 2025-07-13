import os

def export_emails_html(args, context):
    emails = args["emails"]
    os.makedirs("exports/emails", exist_ok=True)
    paths = []
    for i, email in enumerate(emails):
        filename = f"exports/emails/email_{i+1}.html"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"<h2>{email['subject']}</h2><p>{email['body'].replace('\n', '<br>')}</p>")
        paths.append(filename)
    return f"{len(emails)} emails générés dans exports/emails/"
