from typing import TypedDict
import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from core import forecast
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt, Command

load_dotenv()
llm = ChatAnthropic(model=os.getenv("ANTHROPIC_MODEL"), max_tokens=300)

class ForecastState(TypedDict):
    method: str
    forecast: dict
    reason: str
    verdict: str
    feedback: str
    approved: bool

def forecaster(state: ForecastState) -> dict:
    scores = forecast.backtest_summary()
    prompt = (
        f"Backtest MAPE by method (lower is better): {scores}. "
        f"Reviewer feedback so far: {state.get('feedback') or 'none'}. "
        "Reply with exactly one method name from that list on the first line, "
        "then one sentence explaining the choice."
    )
    reply = llm.invoke(prompt).content.strip().splitlines()
    method = reply[0].strip()
    return {
        "method": method,
        "forecast": forecast.forecast_next(method, 3),
        "reason": " ".join(reply[1:]),
    }

def verifier(state: ForecastState) -> dict:
    scores = forecast.backtest_summary()
    method = state["method"]
    if method not in scores:
        return {"verdict": "reject", "feedback": f"'{method}' is not a valid method."}
    best = min(scores.values())
    if scores[method] - best > 0.5:
        return {"verdict": "reject",
                "feedback": f"{method} scores {scores[method]}, well above the best {best}."}
    if state["forecast"] != forecast.forecast_next(method, 3):
        return {"verdict": "reject", "feedback": "Forecast numbers don't match the tool output."}
    return {"verdict": "approve", "feedback": ""}

def human_approval(state: ForecastState) -> dict:
    answer = interrupt({"method": state["method"],
                        "forecast": state["forecast"],
                        "reason": state["reason"]})
    return {"approved": answer.strip().lower() in ("y", "yes")}


def after_verify(state: ForecastState):
    if state["verdict"] == "approve":
        return "human"
    if state.get("attempts", 0) >= 3:
        return END
    return "forecaster"


builder = StateGraph(ForecastState)
builder.add_node("forecaster", forecaster)
builder.add_node("verifier", verifier)
builder.add_node("human", human_approval)
builder.add_edge(START, "forecaster")
builder.add_edge("forecaster", "verifier")
builder.add_conditional_edges("verifier", after_verify)
builder.add_edge("human", END)
graph = builder.compile(checkpointer=MemorySaver())

if __name__ == "__main__":
    config = {"configurable": {"thread_id": "1"}}
    result = graph.invoke({}, config)
    print(result["__interrupt__"][0].value)
    answer = input("Approve? (yes/no): ")
    final = graph.invoke(Command(resume=answer), config)
    print("Approved:", final["approved"])