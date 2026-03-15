import pandas as pd
from pathlib import Path

from ml.training.rank_model import ml_rank


# --------------------------------------------------
# PATH CONFIG
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve()

# backend/src
SRC_DIR = BASE_DIR.parents[2]

# project root
PROJECT_ROOT = SRC_DIR.parent.parent

DATA_DIR = PROJECT_ROOT / "data"

FEATURE_STORE_FILE = (
    DATA_DIR
    / "synthetic"
    / "feature_store"
    / "feature_store.parquet"
)

print("Feature store path:", FEATURE_STORE_FILE)


# --------------------------------------------------
# LOAD SAMPLE DATA
# --------------------------------------------------

df = pd.read_parquet(FEATURE_STORE_FILE)

print("Loaded rows:", len(df))

# take random candidates
candidates = df.sample(20).copy()


# --------------------------------------------------
# FEATURE PREP
# --------------------------------------------------

def normalize(series):
    return (series - series.min()) / (series.max() - series.min() + 1e-8)


candidates["similarity_norm"] = normalize(candidates["similarity_score"])

candidates["rating_norm"] = normalize(candidates["rating_num"])

candidates["popularity_norm"] = normalize(candidates["rating_count_num"])

# mock context + preference
candidates["context_score"] = 0.5
candidates["preference_score"] = 0.3


# --------------------------------------------------
# RUN ML RANKER
# --------------------------------------------------

ranked = ml_rank(candidates)

print("\nTop ranked foods:\n")

print(
    ranked[
        [
            "food_id",
            "similarity_norm",
            "rating_norm",
            "popularity_norm",
            "ml_score"
        ]
    ].head(10)
)