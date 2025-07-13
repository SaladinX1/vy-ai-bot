from fastapi import FastAPI
import sqlite3

app = FastAPI()
DB = "backend/monitoring.db"

def get_db():
    conn = sqlite3.connect(DB)
    return conn

@app.get("/executions")
def list_executions():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM executions ORDER BY start_time DESC")
    results = cur.fetchall()
    conn.close()
    return results

def log_execution(workflow_name, status, start_time, end_time, error=None):
    conn = get_db()
    conn.execute(
        "INSERT INTO executions(workflow_name, status, start_time, end_time, error) VALUES (?, ?, ?, ?, ?)",
        (workflow_name, status, start_time, end_time, error),
    )
    conn.commit()
    conn.close()

def init_db():
    conn = get_db()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS executions (
            id INTEGER PRIMARY KEY,
            workflow_name TEXT,
            status TEXT,
            start_time TEXT,
            end_time TEXT,
            error TEXT
        )
        """
    )
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
