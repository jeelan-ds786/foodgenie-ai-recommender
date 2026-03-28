
import pandas as pd
from pathlib import Path

# Use parent data directory (project root/data)
project_root = Path(__file__).parent.parent.parent.parent
FEEDBACK_FILE = project_root / "data" / "feedback" / "user_feedback.csv"

def load_feedback():

    if FEEDBACK_FILE.exists():
        return pd.read_csv(FEEDBACK_FILE)
    
    return pd.DataFrame(
        columns = ["user_id","dish_name","action","reward"]
    )

def save_feedback(df):
    # Ensure the feedback directory exists
    FEEDBACK_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(FEEDBACK_FILE,index=False)