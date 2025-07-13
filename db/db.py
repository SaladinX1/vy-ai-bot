import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="TON_MDP_MYSQL",
        database="autopilot_db"
    )
