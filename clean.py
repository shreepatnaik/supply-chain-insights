import pandas as pd
df = pd.read_csv("data/DataCoSupplyChainDataset.csv", encoding="latin-1")
#print(df.shape)
dfcol= df[["Order Id", "Order Item Id", "order date (DateOrders)", "shipping date (DateOrders)", "Days for shipping (real)", "Days for shipment (scheduled)", "Late_delivery_risk", "Delivery Status", "Shipping Mode", "Order Region", "Market", "Category Name", "Order Item Quantity", "Sales", "Order Status"]].copy()
#print(dfcol.shape)

dfcol = dfcol.rename(columns={
    "Order Id": "order_id",
    "Order Item Id": "order_item_id",
    "order date (DateOrders)": "order_date",
    "shipping date (DateOrders)": "shipping_date",
    "Days for shipping (real)": "days_shipping_real",
    "Days for shipment (scheduled)": "days_shipping_scheduled",
    "Late_delivery_risk": "late_delivery_risk",
    "Delivery Status": "delivery_status",
    "Shipping Mode": "shipping_mode",
    "Order Region": "order_region",
    "Market": "market",
    "Category Name": "category_name",
    "Order Item Quantity": "quantity",
    "Sales": "sales",
    "Order Status": "order_status",
})
dfcol["order_date"]=pd.to_datetime(dfcol["order_date"])
dfcol["shipping_date"]=pd.to_datetime(dfcol["shipping_date"])
print(dfcol.dtypes)
