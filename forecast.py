import pandas as pd
import numpy as np
from db import get_engine
from sqlalchemy import text
from statsmodels.tsa.holtwinters import ExponentialSmoothing

def monthly_demand(): 
    query = text("""
                    select DATE_TRUNC('month', order_date) AS Month, Sum(quantity) as Units 
                    from orders where order_date < '2017-10-01'
                    group by month order by month; """)
    return pd.read_sql(query, get_engine())


def mape(actual, predicted):
    actual = np.asarray(actual, dtype=float)
    predicted = np.asarray(predicted, dtype=float)
    return np.mean(np.abs(actual - predicted) / actual) * 100

# Each method gets the past demand (history) and how many months to forecast (h),
# and returns h predictions.

def naive(history, h):
    return [history.iloc[-1]] * h


def seasonal_naive(history, h):
    n = len(history)
    return history.iloc[n - 12 : n - 12 + h].values


def moving_average(history, h, window=3):
    return [history.iloc[-window:].mean()] * h


def ets(history, h):
    model = ExponentialSmoothing(
        history,
        trend="add",
        seasonal="add",
        seasonal_periods=12,
    ).fit()
    return model.forecast(h).values


METHODS = {
    "naive": naive,
    "seasonal": seasonal_naive,
    "moving average": moving_average,
    "ets": ets,
}

def backtest(units, h=3, start =24):
    results = {name:[] for name in METHODS}
    for n in range(start, len(units) - h+1):
        history = units.iloc[:n]
        actual = units.iloc[n : n+h] .values
        for name, method in METHODS.items():
            results[name].append(mape(actual, method(history, h)))
    return {name: sum(scores) / len(scores) for name, scores in results.items()}


if __name__ == "__main__":
    units = monthly_demand()["units"]
   
    # single split: learn from 27 months, test on the last 6
    train, test = units.iloc[:27], units.iloc[27:]
    for name, method in METHODS.items():
        pred = method(train, len(test))
        print(f"{name} MAPE (single split): {mape(test.values, pred):.1f}%")

    # rolling backtest: 7 windows, forecasting 3 months each time
    print()
    for name, score in backtest(units).items():
        print(f"{name} MAPE (rolling): {score:.1f}%")   
