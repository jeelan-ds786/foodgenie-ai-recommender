import pandas as pd
from pathlib import Path

FEATURE_STORE_PATH = Path("data/feature_store.parquet")


def load_features():

    if FEATURE_STORE_PATH.exists():
        return pd.read_parquet(FEATURE_STORE_PATH)

    return pd.DataFrame()


def save_features(df):

    df.to_parquet(FEATURE_STORE_PATH, index=False)