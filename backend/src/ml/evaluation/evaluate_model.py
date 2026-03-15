import pandas as pd
import joblib
from pathlib import Path

from ml.evaluation.metrics import evaluate_ranking


# --------------------------------------------------
# PATH CONFIG
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve()

SRC_DIR = BASE_DIR.parents[2]
PROJECT_ROOT = SRC_DIR.parent.parent

DATA_DIR = PROJECT_ROOT / "data"
MODEL_DATA_DIR = DATA_DIR / "synthetic" / "model_data"

TEST_FILE = MODEL_DATA_DIR / "test.parquet"
MODEL_PATH = SRC_DIR / "models" / "xgboost_food_ranker.pkl"


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

print("Loading test dataset...")

df = pd.read_parquet(TEST_FILE)

print("Rows:", len(df))


# --------------------------------------------------
# LOAD MODEL
# --------------------------------------------------

print("Loading ML model...")

model = joblib.load(MODEL_PATH)


# --------------------------------------------------
# FEATURE SET
# --------------------------------------------------

FEATURES = [
    "similarity_score",
    "rating_num",
    "rating_count_num",
    "context_score",
    "preference_score"
]


# --------------------------------------------------
# ML PREDICTIONS
# --------------------------------------------------

print("Generating ML predictions...")

X = df[FEATURES]

df["ml_score"] = model.predict(X)


# --------------------------------------------------
# RULE BASELINE
# --------------------------------------------------

print("Generating rule-based scores...")

df["rule_score"] = (
    0.45 * df["similarity_score"]
    + 0.20 * df["rating_num"]
    + 0.20 * df["rating_count_num"]
    + 0.10 * df["context_score"]
    + 0.05 * df["preference_score"]
)


# --------------------------------------------------
# BUILD RELEVANCE LISTS
# --------------------------------------------------

ml_lists = []
rule_lists = []

for user_id, group in df.groupby("user_id"):

    ml_ranked = group.sort_values("ml_score", ascending=False)
    rule_ranked = group.sort_values("rule_score", ascending=False)

    ml_lists.append(ml_ranked["reward"].values)
    rule_lists.append(rule_ranked["reward"].values)


# --------------------------------------------------
# EVALUATE
# --------------------------------------------------

print("\nEvaluating ML model...")

ml_results = evaluate_ranking(ml_lists, k=10)

print("\nEvaluating Rule-based baseline...")

rule_results = evaluate_ranking(rule_lists, k=10)


# --------------------------------------------------
# PRINT COMPARISON
# --------------------------------------------------

print("\n==============================")
print("MODEL COMPARISON")
print("==============================")

for metric in ml_results.keys():

    ml_value = ml_results[metric]
    rule_value = rule_results[metric]

    print(
        f"{metric}  |  ML: {ml_value:.4f}   Rule: {rule_value:.4f}"
    )