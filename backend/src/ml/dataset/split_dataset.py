import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split

# --------------------------------------------------
# PATH CONFIG
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve()
PROJECT_ROOT = BASE_DIR.parents[4]

DATA_DIR = PROJECT_ROOT / "data"
SYNTHETIC_DIR = DATA_DIR / "synthetic"

MODEL_DATA_DIR = SYNTHETIC_DIR / "model_data"

INPUT_FILE = MODEL_DATA_DIR / "ML_training_dataset.parquet"

TRAIN_FILE = MODEL_DATA_DIR  / "train.parquet"
VAL_FILE = MODEL_DATA_DIR  / "validation.parquet"
TEST_FILE = MODEL_DATA_DIR  / "test.parquet"

print("=" * 60)
print("Splitting Training Dataset")
print("=" * 60)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

print("\nLoading training dataset...")

df = pd.read_parquet(INPUT_FILE)

print(f"Dataset rows: {len(df):,}")

# --------------------------------------------------
# TRAIN / TEMP SPLIT
# --------------------------------------------------

train_df, temp_df = train_test_split(
    df,
    test_size=0.30,
    random_state=42
)

# --------------------------------------------------
# VALIDATION / TEST SPLIT
# --------------------------------------------------

val_df, test_df = train_test_split(
    temp_df,
    test_size=0.50,
    random_state=42
)

# --------------------------------------------------
# SAVE DATASETS
# --------------------------------------------------

train_df.to_parquet(TRAIN_FILE, index=False)
val_df.to_parquet(VAL_FILE, index=False)
test_df.to_parquet(TEST_FILE, index=False)

# --------------------------------------------------
# REPORT
# --------------------------------------------------

print("\nDataset split completed\n")

print(f"Train size: {len(train_df):,}")
print(f"Validation size: {len(val_df):,}")
print(f"Test size: {len(test_df):,}")

print("\nFiles saved:")

print(TRAIN_FILE)
print(VAL_FILE)
print(TEST_FILE)