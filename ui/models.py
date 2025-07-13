import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Razorback2.2",
    database="workflowdb"
)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100),
    password VARCHAR(100)
)
""")
