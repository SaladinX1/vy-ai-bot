from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional
import sqlite3
import hashlib

app = FastAPI()

DATABASE = "backend/users.db"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn

def create_user(username: str, password: str):
    conn = get_db()
    cur = conn.cursor()
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    cur.execute("INSERT INTO users(username, password) VALUES (?, ?)", (username, hashed_pw))
    conn.commit()
    conn.close()

def authenticate_user(username: str, password: str):
    conn = get_db()
    cur = conn.cursor()
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed_pw))
    user = cur.fetchone()
    conn.close()
    return user

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Nom d'utilisateur ou mot de passe incorrect")
    # Ici on retourne un token factice (à remplacer par JWT)
    return {"access_token": user[0], "token_type": "bearer"}

# À lancer une fois pour créer la table users
def init_db():
    conn = get_db()
    conn.execute(
        "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)"
    )
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
