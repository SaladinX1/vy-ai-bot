# core/cleanup.py

import os
import time

def clean_old_logs(directory="logs/", max_age_days=10):
    now = time.time()
    for fname in os.listdir(directory):
        path = os.path.join(directory, fname)
        if os.path.isfile(path):
            if now - os.path.getmtime(path) > max_age_days * 86400:
                os.remove(path)
