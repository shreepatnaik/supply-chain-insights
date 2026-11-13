import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

def get_engine():
    load_dotenv()

    #env credentials
    user = os.getenv("PGUSER")
    host = os.getenv("PGHOST")
    password = os.getenv("PGPASSWORD")
    database = os.getenv("PGDATABASE")
    port = os.getenv("PGPORT")

    #connection string
    url = f"postgresql+psycopg://{user}:{password}@{host}:{port}/{database}"
    engine = create_engine(url)
    return engine 