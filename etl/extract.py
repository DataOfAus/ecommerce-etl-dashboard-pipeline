
import requests
import pandas as pd
import os
from datetime import datetime, timezone

# Define paths relative to your project root (any operating system)
CSV_NAME = "shopify_orders.csv"
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
CSV_PATH = os.path.join(DATA_DIR, CSV_NAME)
SHOPIFY_API_URL = "https://fakestoreapi.com/products"

def extract_from_api():
    """
    Extracts order data from a mock Shopify-style API.
    Returns a pandas DataFrame.
    """
    try:
        response = requests.get(SHOPIFY_API_URL, timeout=10)
        response.raise_for_status()
        raw_data = response.json()

        # Shopify-style structure
        normalized = pd.json_normalize(raw_data)
        normalized["extracted_at"] = datetime.now(timezone.utc)
        return normalized

    except requests.RequestException as e:
        print(f"API extraction failed: {e}")
        return pd.DataFrame()
    

def extract_from_csv():
    """
    Reads a Shopify-style CSV export file from local storage.
    Returns a pandas DataFrame.
    """
    if not os.path.exists(CSV_PATH):
        print(f"CSV file not found at {CSV_PATH}")
        return pd.DataFrame()

    df = pd.read_csv(CSV_PATH)
    df["extracted_at"] = datetime.now(timezone.utc)
    return df


def get_data(source="api"):
    """
    General extractor interface — use 'api' or 'csv'.
    """
    if source == "api":
        return extract_from_api()
    elif source == "csv":
        return extract_from_csv()
    else:
        raise ValueError("Source must be either 'api' or 'csv'")


if __name__ == "__main__":
    # Example usage
    df = get_data(source="api")  # or source="csv"
    print(df.head())
