import requests
import os

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK")

def slack_notify(message):
    if SLACK_WEBHOOK_URL:
        payload = {"text": message}
        try:
            requests.post(SLACK_WEBHOOK_URL, json=payload)
        except Exception as e:
            print(f"Slack error: {e}")


