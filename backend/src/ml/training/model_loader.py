import joblib
from pathlib import Path

# --------------------------------------------------
# PATH CONFIG
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve()

# backend/src
SRC_DIR = BASE_DIR.parents[2]

MODEL_PATH = SRC_DIR / "models" / "xgboost_food_ranker.pkl"


# --------------------------------------------------
# MODEL LOADER
# --------------------------------------------------

_model = None


def get_model():
    global _model

    # load once (singleton)
    if _model is None:

        if not MODEL_PATH.exists():
            print("⚠ ML model not found:", MODEL_PATH)
            return None

        print("Loading ML model:", MODEL_PATH)

        _model = joblib.load(MODEL_PATH)

    return _model