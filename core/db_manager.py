import os
import json
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

# ==== CONFIGURATION MYSQL ====
MYSQL_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASS", ""),
    "database": os.getenv("MYSQL_DB", "ai_project_manager")
}

def get_mysql_conn():
    return mysql.connector.connect(**MYSQL_CONFIG)

# ==== DATABASE MANAGER UNIFIÉ ====
class DBManager:

    @staticmethod
    def init():
        """Initialise les tables nécessaires si elles n'existent pas."""
        conn = get_mysql_conn()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                project_id VARCHAR(255) PRIMARY KEY,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS project_states (
                project_id VARCHAR(255) PRIMARY KEY,
                state_json JSON
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS metadata (
                id INT PRIMARY KEY,
                last_used_project VARCHAR(255)
            )
        """)
        conn.commit()
        conn.close()

    @staticmethod
    def list_projects():
        conn = get_mysql_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT project_id FROM projects")
        result = [row[0] for row in cursor.fetchall()]
        conn.close()
        return result

    @staticmethod
    def add_project(project_id, plan=None, status="pending"):
        """Ajoute un projet s'il n'existe pas déjà."""
        conn = get_mysql_conn()
        cursor = conn.cursor()
        cursor.execute("INSERT IGNORE INTO projects (project_id) VALUES (%s)", (project_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def save_state(project_id, state_dict):
        conn = get_mysql_conn()
        cursor = conn.cursor()
        state_json = json.dumps(state_dict)
        query = """
            INSERT INTO project_states (project_id, state_json)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE state_json = VALUES(state_json)
        """
        cursor.execute(query, (project_id, state_json))
        conn.commit()
        conn.close()

    @staticmethod
    def get_state(project_id):
        conn = get_mysql_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT state_json FROM project_states WHERE project_id = %s", (project_id,))
        row = cursor.fetchone()
        conn.close()
        return json.loads(row[0]) if row else {}

    @staticmethod
    def set_last_used(project_id):
        conn = get_mysql_conn()
        cursor = conn.cursor()
        cursor.execute("REPLACE INTO metadata (id, last_used_project) VALUES (1, %s)", (project_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def get_last_used():
        conn = get_mysql_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT last_used_project FROM metadata WHERE id = 1")
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else None
