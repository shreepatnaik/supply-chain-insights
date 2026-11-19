from fastapi import FastAPI
from sqlalchemy import text
from core.db import get_engine
from core.explain import get_facts, explain
import core.stats as stats
import uuid
from langgraph.types import Command
from agents.workflow import graph

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

@app.post("/forecast/propose")
def propose_forecast():
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    result = graph.invoke({}, config)
    if "__interrupt__" not in result:
        return {"thread_id": thread_id, "status": "rejected",
                "feedback": result.get("feedback")}
    return {"thread_id": thread_id, "status": "awaiting_approval",
            "proposal": result["__interrupt__"][0].value}


@app.post("/forecast/{thread_id}/decision")
def decide(thread_id: str, approve: bool):
    config = {"configurable": {"thread_id": thread_id}}
    final = graph.invoke(Command(resume="yes" if approve else "no"), config)
    return {"thread_id": thread_id, "approved": final["approved"]}

