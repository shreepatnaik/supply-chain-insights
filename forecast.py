import pandas as pd
from db import get_engine
from sqlalchemy import text

engine = get_engine()

def monthly_demand(): 
    query = text("""
                    select DATE_TRUNC('month', order_date) AS Month, Sum(quantity) as Units 
                    from orders where order_date < '2017-10-01'
                    group by month order by month; """)
    df = pd.read_sql(query, engine)
    return df

if __name__ == "__main__":
    df = monthly_demand()
    # print(df)
    #print(len(df))
    train = df.iloc[:27]
    test = df.iloc[27:]
    #print(len(train), len(test))
    naive_pred=train["units"].iloc[-1]
    print("Naive prediction for April 2017:", naive_pred)
    print("Actual demand for April 2017:", test["units"].iloc[0])