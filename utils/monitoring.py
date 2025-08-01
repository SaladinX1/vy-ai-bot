# utils/slack_notifier.py

import requests
import os
import logging

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

def slack_notify(message: str):
    if not SLACK_WEBHOOK_URL:
        raise ValueError("SLACK_WEBHOOK_URL non défini")

    payload = {"text": message}
    response = requests.post(SLACK_WEBHOOK_URL, json=payload)

    if response.status_code != 200:
        raise Exception(f"Erreur Slack: {response.text}")

def log_metric(key: str, value):
    """
    Log une métrique pour monitoring ou dashboard.
    Peut être relié à Prometheus, Grafana, etc.
    """
    message = f"[METRIC] {key}: {value}"
    print(message)
    logging.info(message)


def notify_failure(message: str):
    """
    Envoie une notification d’échec critique.
    Actuellement via Slack (via slack_notifier).
    """
    formatted = f"💥 Échec détecté : {message}"
    print("[ALERTE]", formatted)
    logging.error(formatted)

    try:
        slack_notify(formatted)
    except Exception as e:
        logging.error(f"⚠️ Impossible d’envoyer l’alerte Slack : {e}")