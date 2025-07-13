from flask import Flask, request, jsonify
from workflows import manager
from core import plan_executor
import threading

app = Flask(__name__)

def run_workflow_async(name):
    steps = manager.load_workflow(name)
    if not steps:
        return f"Workflow '{name}' introuvable", 404
    try:
        plan_executor.execute_plan(steps)
    except Exception as e:
        return str(e), 500
    return f"Workflow '{name}' exécuté avec succès", 200

@app.route("/run_workflow", methods=["POST"])
def run_workflow():
    data = request.json
    name = data.get("name")
    if not name:
        return jsonify({"error": "Paramètre 'name' requis"}), 400

    thread = threading.Thread(target=run_workflow_async, args=(name,))
    thread.start()
    return jsonify({"status": f"Workflow '{name}' lancé"}), 200

if __name__ == "__main__":
    app.run(port=5000)
