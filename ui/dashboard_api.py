# ui/dashboard_api.py

from flask import Blueprint, jsonify
from agents.scheduler import daily_autorun
from fastapi import FastAPI, APIRouter
from fastapi.responses import JSONResponse

import streamlit as st
from core.memory_store import load_memory

st.set_page_config(page_title="IA Business Dashboard", layout="wide")
st.title("📊 Business Autonome IA")

logs = load_memory()

for item in logs[-10:][::-1]:
    st.write(f"**{item['timestamp']}** - {item['type']} - {item['content']}")

# -------------------------------

app = FastAPI()
router = APIRouter()

# Données fictives pour le dashboard
sales_data = {
    "total_sales": 25,
    "revenue": 1250.50,
    "active_customers": 18,
    "products_sold": {
        "Ebook": 15,
        "Templates": 10
    }
}

dashboard_api = Blueprint('dashboard_api', __name__)

@router.get("/api/dashboard")
async def get_dashboard_data():
    return JSONResponse(content=sales_data)



@dashboard_api.route('/api/run_autonomous_cycle', methods=['POST'])
def run_cycle():
    try:
        daily_autorun()
        return jsonify({"status": "success", "message": "Cycle exécuté"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


app.include_router(router)
