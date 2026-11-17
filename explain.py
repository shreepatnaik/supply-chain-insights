import os
import json
from dotenv import load_dotenv
from anthropic import Anthropic
from forecast import monthly_demand, backtest

load_dotenv()
client = Anthropic()
model = os.getenv("ANTHROPIC_MODEL")

def get_facts():
    units = monthly_demand()["units"]
    scores = backtest(units)
    return {name: round(float(score), 1) for name, score in scores.items()}


RULES = """You explain forecasting results to a supply-chain planner.
Use only the facts provided. Do not invent, estimate, or calculate any numbers.
Only mention numbers that appear in the facts, exactly as written.
Do not recommend actions the facts don't support.
Write 3 to 4 plain-English sentences."""


def explain(facts):
    try:
         response = client.messages.create(
            model=model,
            max_tokens=1000,
            system=RULES,
            messages=[{
                "role": "user",
                "content": "Rolling backtest MAPE by forecasting method (lower is better):\n"
                        + json.dumps(facts),
            }],
        )
         text = "".join(block.text for block in response.content if block.type == "text")
         return {"explanation": text, "based_on": facts}
    except Exception as error:
        return {
            "explanation": None,
            "reason": f"Explanation unavailable: {type(error).__name__}",
            "based_on": facts,
        }

if __name__ == "__main__":
    facts = get_facts()
    result = explain(facts)
    print(result["explanation"])
    print(result["based_on"])