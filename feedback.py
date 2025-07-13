feedback_log = "logs/feedback.csv"

from db.db import get_connection

def save_feedback(workflow, score, note):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO feedback (workflow_name, score, note) VALUES (%s, %s, %s)",
        (workflow, score, note)
    )
    conn.commit()
    conn.close()




# def save_feedback(workflow, score, note):
#     with open(feedback_log, "a") as f:
#         f.write(f"{workflow},{score},{note}\n")

# def save_feedback(workflow, score, note):
#     with open(feedback_log, "a") as f:
#         f.write(f"{workflow},{score},{note}\n")