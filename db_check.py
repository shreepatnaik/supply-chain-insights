import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

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

#connect and query
with engine.connect() as conn:
    conn.execute(text("SELECT COUNT(*) FROM orders")).scalar()
