import pandas as pd
from pathlib import Path

# --------------------------------------------------
# PATH CONFIG
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve()
PROJECT_ROOT = BASE_DIR.parents[4]

DATA_DIR = PROJECT_ROOT / "data"

SYNTHETIC_DIR = DATA_DIR / "synthetic"
FEATURE_STORE_DIR = SYNTHETIC_DIR / "feature_store"

INTERACTIONS_FILE = SYNTHETIC_DIR / "interactions.parquet"
FEATURE_STORE_FILE = FEATURE_STORE_DIR / "feature_store.parquet"

MODEL_DATA_DIR = SYNTHETIC_DIR / "model_data"
MODEL_DATA_DIR.mkdir(parents=True, exist_ok=True) 

OUTPUT_FILE = MODEL_DATA_DIR / "ML_training_dataset.parquet"

print("=" * 60)
print("Building Training Dataset")
print("=" * 60)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

print("\nLoading datasets...")

interactions = pd.read_parquet(INTERACTIONS_FILE)
feature_store = pd.read_parquet(FEATURE_STORE_FILE)

print(f"Interactions rows: {len(interactions):,}")
print(f"Feature store rows: {len(feature_store):,}")

# --------------------------------------------------
# AGGREGATE USER BEHAVIOR
# --------------------------------------------------

print("\nAggregating interaction signals...")

agg = (
    interactions
    .groupby(["user_id", "food_id"])
    .agg({
        "impressions": "sum",
        "clicks": "sum",
        "orders": "sum"
    })
    .reset_index()
)

print(f"Aggregated rows: {len(agg):,}")

# --------------------------------------------------
# BUILD REWARD SIGNAL
# --------------------------------------------------

print("\nGenerating reward...")

# production-style reward weighting
agg["reward"] = (
    0.3 * agg["clicks"] +
    0.7 * agg["orders"]
)

# normalize reward between 0 and 1
agg["reward"] = agg["reward"].clip(0, 1)

print("Reward stats:")
print(agg["reward"].describe())

# --------------------------------------------------
# JOIN WITH FEATURE STORE
# --------------------------------------------------

print("\nJoining features with rewards...")

training_df = feature_store.merge(
    agg,
    on=["user_id", "food_id"],
    how="inner"
)

print(f"Training dataset size: {len(training_df):,}")

# --------------------------------------------------
# SAVE DATASET
# --------------------------------------------------

training_df.to_parquet(
    OUTPUT_FILE,
    index=False
)

print("\nTraining dataset saved")
print(f"Location: {OUTPUT_FILE}")

print("\nColumns:")
print(training_df.columns)
print(training_df.shape)

print("\nSample rows:")
print(training_df.head())

print("\nDone.")