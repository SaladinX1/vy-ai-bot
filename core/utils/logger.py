import logging
import os
import json

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "execution.log")

# Création du dossier logs s'il n'existe pas
os.makedirs(LOG_DIR, exist_ok=True)

# Configuration du logger
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

def log_info(msg: str):
    logging.info(msg)

def log_warning(msg: str):
    logging.warning(msg)

def log_error(msg: str):
    logging.error(msg)

def append_log(text: str):
    """Ajoute une ligne de texte brute dans le fichier de logs."""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(text + "\n")

def read_log() -> str:
    """Lit tout le contenu du fichier de logs, ou retourne vide si absent."""
    if not os.path.exists(LOG_FILE):
        return ""
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        return f.read()


def load_logs_summary(n=50):
    try:
        with open("logs.json", encoding="utf-8") as f:
            logs = json.load(f)
            return logs[-n:]
    except:
        return []