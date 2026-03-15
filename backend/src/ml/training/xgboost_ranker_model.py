import pandas as pd
import xgboost as xgb
import joblib
from pathlib import Path

BASE_DIR = Path(__file__).resolve()

# backend/src/ml/training/xgboost_ranker_model.py
SRC_DIR = BASE_DIR.parents[2]   # backend/src

DATA_DIR = SRC_DIR.parent.parent / "data"

MODEL_DATA_DIR = DATA_DIR / "synthetic" / "model_data"

TRAIN_FILE = MODEL_DATA_DIR / "train.parquet"
VAL_FILE = MODEL_DATA_DIR / "validation.parquet"

# save model inside backend/src/models
MODEL_DIR = SRC_DIR / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

MODEL_FILE = MODEL_DIR / "xgboost_food_ranker.pkl"

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

print("Loading training dataset...")
train_df = pd.read_parquet(TRAIN_FILE)

print("Loading validation dataset...")
val_df = pd.read_parquet(VAL_FILE)

print("Train rows:", len(train_df))
print("Validation rows:", len(val_df))


# --------------------------------------------------
# TEMP FIX: Convert reward to integer relevance
# --------------------------------------------------

train_df["reward"] = train_df["reward"].round().astype(int)
val_df["reward"] = val_df["reward"].round().astype(int)

# ensure non-negative labels
train_df["reward"] = train_df["reward"].clip(lower=0)
val_df["reward"] = val_df["reward"].clip(lower=0)


# --------------------------------------------------
# FEATURES
# --------------------------------------------------

features = [
    "similarity_score",
    "rating_num",
    "rating_count_num",
    "context_score",
    "preference_score"
]

X_train = train_df[features]
y_train = train_df["reward"]

X_val = val_df[features]
y_val = val_df["reward"]

# --------------------------------------------------
# GROUPS (CRITICAL FOR RANKING)
# --------------------------------------------------

train_group = train_df.groupby("user_id").size().to_list()
val_group = val_df.groupby("user_id").size().to_list()

print("Number of training groups:", len(train_group))

# --------------------------------------------------
# MODEL
# --------------------------------------------------

model = xgb.XGBRanker(
    objective="rank:ndcg",
    n_estimators=300,
    learning_rate=0.05,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    eval_metric="ndcg",
    random_state=42
)

# --------------------------------------------------
# TRAIN
# --------------------------------------------------

print("\nTraining XGBoost Ranker...")

model.fit(
    X_train,
    y_train,
    group=train_group,
    eval_set=[(X_val, y_val)],
    eval_group=[val_group],
    verbose=True
)

# --------------------------------------------------
# SAVE MODEL
# --------------------------------------------------

joblib.dump(model, MODEL_FILE)

print("\nModel saved to:", MODEL_FILE)