import os
import joblib
from pathlib import Path

# --------------------------------------------------
# Thread Safety: Prevent segmentation faults
# --------------------------------------------------
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"

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
        
        _model.set_params(nthread=1)

    return _model