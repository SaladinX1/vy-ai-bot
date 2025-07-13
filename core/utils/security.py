# Fichier : utils/security.py
import re

def sanitize_prompt(prompt):
    return re.sub(r'[\"<>]', '', prompt)
