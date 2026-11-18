from fastapi import FastAPI
from sqlalchemy import text
from db import get_engine
from explain import get_facts, explain
import stats

app=FastAPI()
engine = get_engine()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/stats/late-by-region")
def late_by_region():
   
        return stats.late_by_region()

@app.get("/stats/late-by-shipping-mode")
def late_by_shippingmode(): 
    return stats.late_by_shipping_mode()

@app.get("/explain/forecast")
def explain_forecast():
    facts = get_facts()
    return explain(facts)


