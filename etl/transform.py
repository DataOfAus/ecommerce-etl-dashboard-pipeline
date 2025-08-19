import pandas as pd

def flatten_nested_columns(df: pd.DataFrame, sep: str = "_") -> pd.DataFrame:
    """
    Automatically flattens all columns in the DataFrame that contain nested dicts.
    Returns a new DataFrame with flattened columns, preserving original data.
    """

    df = df.copy()

    # Find all columns where at least one value is a dictionary (nested object)
    nested_cols = [col for col in df.columns if df[col].apply(lambda x: isinstance(x, dict)).any()]

    for col in nested_cols:
        # Normalize the nested dictionaries into new columns with prefixed names
        normalized = pd.json_normalize(df[col]).add_prefix(f"{col}{sep}")
        df = df.drop(columns=[col]).reset_index(drop=True)
        df = pd.concat([df, normalized], axis=1)

    return df


def transform(df_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms raw product data by flattening nested fields and enforcing type consistency.
    Returns a clean, load-ready DataFrame.
    """

    if df_raw.empty:
        print("No data to transform.")
        return pd.DataFrame()

    df = df_raw.copy()

    # Flatten any nested dict columns
    df = flatten_nested_columns(df)

    # Convert timestamp column to UTC if it exists
    if "extracted_at" in df.columns:
        df["extracted_at"] = pd.to_datetime(df["extracted_at"], utc=True)

    # Type enforcement for commonly expected fields
    if "id" in df.columns:
        df["id"] = df["id"].astype(int)

    if "price" in df.columns:
        df["price"] = df["price"].astype(float)

    return df


if __name__ == "__main__":
    from extract import get_data

    raw_df = get_data(source="api")  # or source="csv"
    clean_df = transform(raw_df)
    print(clean_df.head())