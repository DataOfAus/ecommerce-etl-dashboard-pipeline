import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Database connection parameters
DB_USER = os.getenv("CLOUD_DB_USER")
DB_PASSWORD = os.getenv("CLOUD_DB_PASSWORD")
DB_HOST = os.getenv("CLOUD_DB_HOST")
DB_PORT = os.getenv("CLOUD_DB_PORT")
DB_NAME = os.getenv("CLOUD_DB_NAME")

# SQLAlchemy connection string
DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Table name
TABLE_NAME = "products_transformed"

def load_data(df: pd.DataFrame, table_name: str = TABLE_NAME) -> None:
    """
    Loads a cleaned DataFrame into a PostgreSQL table.
    Overwrites table if it already exists.
    """

    if df.empty:    
        print("No data to load.")
        return

    try:
        engine = create_engine(DB_URL, echo=True)
        with engine.connect() as conn:
            df.to_sql(table_name, con=conn, if_exists="replace", index=False)
            print(f"[{datetime.now()}] Loaded {len(df)} rows into '{table_name}' table.")

    except Exception as e:
        print(f"❌ Load failed: {e}")


if __name__ == "__main__":
    from extract import get_data
    from transform import transform

    raw_df = get_data(source="api")   # or source="csv"
    clean_df = transform(raw_df)
    load_data(clean_df)
