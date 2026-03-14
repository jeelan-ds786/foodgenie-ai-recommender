
import pandas as pd
from pathlib import Path

FEEDBACK_FILE = Path("data/user_feedback.csv")

def load_feedback():

    if FEEDBACK_FILE.exist():
        return pd.read_csv(FEEDBACK_FILE)
    
    return pd.DataFrame(
        columns = ["user_id","dish_name","action","reward"]
    )

def save_feedback(df):
    df.to_csv(FEEDBACK_FILE,index=False)