from fastapi import FastAPI, Body
import uvicorn
from core.plan_executor import execute_plan  # Chemin corrigé selon ton projet

app = FastAPI()

@app.post("/run")
def run_workflow(plan: dict = Body(...)):
    try:
        execute_plan(plan)
        return {"status": "done"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
