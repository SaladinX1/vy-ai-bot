# Dockerfile

# Étape 1 : base Python
FROM python:3.11-slim

# Étape 2 : créer un dossier app
WORKDIR /app

# Étape 3 : copier les fichiers
COPY . /app

# Étape 4 : installer les dépendances
RUN pip install --upgrade pip && pip install -r requirements.txt

# Exposer le port de Streamlit
EXPOSE 8501

# Étape 5 : commande de lancement
CMD ["python", "main.py"]
