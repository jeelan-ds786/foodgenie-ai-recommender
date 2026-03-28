import pandas as pd
from pathlib import Path

# Use parent data directory (project root/data)
project_root = Path(__file__).parent.parent.parent.parent
PREFERENCE_FILE = project_root / "data" / "feedback" / "user_preference.csv"


def load_preferences():

    if PREFERENCE_FILE.exists():
        return pd.read_csv(PREFERENCE_FILE)
    
    return pd.DataFrame(columns=["user_id","dish_name","score"])


def save_preferences(df):
    # Ensure the feedback directory exists
    PREFERENCE_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(PREFERENCE_FILE,index=False)