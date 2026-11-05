import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from clean import get_clean_data

load_dotenv()

#env credentials
user = os.getenv("PGUSER")
host = os.getenv("PGHOST")
password = os.getenv("PGPASSWORD")
database = os.getenv("PGDATABASE")
port = os.getenv("PGPORT")

#connection string
url = f"postgresql+psycopg://{user}:{password}@{host}:{port}/{database}"

#engine
engine = create_engine(url)

df = get_clean_data()

#convert late_delivery_risk from 0/1 to True/False
df["late_delivery_risk"] = df["late_delivery_risk"].astype(bool)

# 5. load into Postgres:
load = df.to_sql("orders", engine, if_exists="append", index=False, chunksize=10000)

print (load)