import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
FEATURE_STORE_PATH = PROJECT_ROOT / "data" / "feature_store" / "feature_store.parquet"

OVERWRITE_FEATURE_STORE = False

def load_features():

    if FEATURE_STORE_PATH.exists():
        return pd.read_parquet(FEATURE_STORE_PATH)

    return pd.DataFrame()


def save_features(df):
    
    FEATURE_STORE_PATH.parent.mkdir(parents=True, exist_ok=True)

    # development mode → overwrite file
    if OVERWRITE_FEATURE_STORE:
        df.to_parquet(FEATURE_STORE_PATH, index=False)
        return

    # production mode → append
    if FEATURE_STORE_PATH.exists():
        existing = pd.read_parquet(FEATURE_STORE_PATH)
        df = pd.concat([existing, df])


    df.to_parquet(FEATURE_STORE_PATH, index=False)

    print("===========FEATURE STORE DATA====================")
    print("Columns in dataset:")
    print(df.columns)

    print("\nFirst rows:")
    print(df.head())

    print("\nDataset shape:")
    print(df.shape)