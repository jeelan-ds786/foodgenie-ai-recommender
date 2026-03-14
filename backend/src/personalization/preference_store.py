import pandas as pd
from pathlib import Path

PREFERENCE_FILE = Path('data/user_preference.csv')


def load_preferences():

    if PREFERENCE_FILE.exists():
        return pd.read_csv(PREFERENCE_FILE)
    
    return pd.DataFrame(columns=["user_id","dish_name","score"])


def save_preferences(df):
    df.to_csv(PREFERENCE_FILE,index=False)