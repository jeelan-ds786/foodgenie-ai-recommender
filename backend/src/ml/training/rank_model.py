from ml.training.model_loader import get_model


MODEL_FEATURES = [
    "similarity_score",
    "rating_num",
    "rating_count_num",
    "context_score",
    "preference_score"
]


def ml_rank(candidates):

    model = get_model()

    # copy dataframe to avoid modifying original
    df = candidates.copy()

    # --------------------------------------------------
    # Fallback if model not available
    # --------------------------------------------------
    if model is None:
        return df.sort_values("similarity_score", ascending=False)

    # --------------------------------------------------
    # Ensure required features exist
    # --------------------------------------------------
    for feature in MODEL_FEATURES:
        if feature not in df.columns:
            df[feature] = 0

    features = df[MODEL_FEATURES]

    # --------------------------------------------------
    # Predict ranking score
    # --------------------------------------------------
    scores = model.predict(features)

    df["ml_score"] = scores

    ranked = df.sort_values("ml_score", ascending=False)

    return ranked