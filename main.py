from fastapi import FastAPI
from sqlalchemy import text
from db import get_engine

app=FastAPI()
engine = get_engine()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/stats/late-by-region")
def late_by_region():
    query = text("""
                    select order_region, count(*) as Items, round(count(*) filter (where days_shipping_real > days_shipping_scheduled) * 100.0 / COUNT(*), 1) AS late_pct 
                    from  orders where delivery_status <> 'Shipping canceled'  
                    group by order_region order by  late_pct DESC; """)

    with engine.connect() as conn:
        result = conn.execute(query)
        return [dict(row._mapping) for row in result]

@app.get("/stats/late-by-shipping-mode")
def late_by_shippingmode(): 
    query = text("""
                    SELECT shipping_mode,
                        COUNT(*) AS items,
                        ROUND(COUNT(*) FILTER (WHERE days_shipping_real > days_shipping_scheduled) * 100.0 / COUNT(*), 1) AS late_pct
                    FROM orders
                    WHERE delivery_status <> 'Shipping canceled'
                    GROUP BY shipping_mode
                    ORDER BY late_pct DESC; """)

    with engine.connect() as conn:
        result = conn.execute(query)
        return [dict(row._mapping) for row in result]