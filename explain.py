from forecast import monthly_demand, backtest

def get_facts():
    units = monthly_demand()["units"]
    scores = backtest(units)
    return {name: round(float(scores), 1) for name, scores in scores.items()}

if __name__ == "__main__":
    facts = get_facts()
    print(facts)