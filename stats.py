import pandas as pd
from db import get_engine


def late_by_shipping_mode():
    query = """
        SELECT shipping_mode,
               COUNT(*) AS items,
               ROUND(COUNT(*) FILTER (WHERE days_shipping_real > days_shipping_scheduled)
                     * 100.0 / COUNT(*), 1) AS late_pct
        FROM orders
        WHERE delivery_status <> 'Shipping canceled'
        GROUP BY shipping_mode
        ORDER BY late_pct DESC;
    """
    return pd.read_sql(query, get_engine()).to_dict(orient="records")


def late_by_region():
         query = """
                    select order_region, count(*) as Items, round(count(*) filter (where days_shipping_real > days_shipping_scheduled) * 100.0 / COUNT(*), 1) AS late_pct 
                    from  orders where delivery_status <> 'Shipping canceled'  
                    group by order_region order by  late_pct DESC; """
         return pd.read_sql(query, get_engine()).to_dict(orient="records")
