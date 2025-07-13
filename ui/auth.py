from flask import Flask, request, redirect, url_for, render_template, session
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'secret!'

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Razorback2.2",
    database="workflowdb"
)
cursor = conn.cursor()

def create_user(username, password):
    hashed = generate_password_hash(password)
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed))
    conn.commit()

def verify_user(username, password):
    cursor.execute("SELECT password FROM users WHERE username=%s", (username,))
    result = cursor.fetchone()
    if result and check_password_hash(result[0], password):
        return True
    return False

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if verify_user(request.form["username"], request.form["password"]):
            session["user"] = request.form["username"]
            return redirect(url_for("index"))
        return "Échec de connexion"
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

# Protéger les routes avec @login_required (à créer)

