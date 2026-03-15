import pandas as pd

from personalization.personalization_engine import get_user_preferences
from features.feature_pipeline import store_candidate_features
from recommender.candidate_generator.candidate_generator import generate_candidates

# Try loading ML ranker
try:
    from ml.training.rank_model import ml_rank
    ML_MODEL_AVAILABLE = True
except Exception:
    ML_MODEL_AVAILABLE = False


def normalize(series):
    return (series - series.min()) / (series.max() - series.min() + 1e-8)


def compute_context_score(row, context_food_types):
    """Check if food matches context preferences"""
    food_name = str(row["dish_name"]).lower()

    for keyword in context_food_types:
        if keyword in food_name:
            return 1.0

    return 0.0


def compute_preference_score(row, user_preferences):
    """Check if dish matches user preference history"""
    dish = str(row["dish_name"]).lower()

    for pref in user_preferences:
        if pref.lower() in dish:
            return 1.0

    return 0.0


def rule_based_rank(candidates: pd.DataFrame):
    """
    Fallback ranking if ML model is unavailable
    """

    candidates["final_score"] = (
        0.45 * candidates["similarity_norm"]
        + 0.20 * candidates["rating_norm"]
        + 0.20 * candidates["popularity_norm"]
        + 0.10 * candidates["context_score"]
        + 0.05 * candidates["preference_score"]
    )

    return candidates.sort_values("final_score", ascending=False)


def rank_candidates(candidates: pd.DataFrame, context, user_id=None):

    candidates = candidates.copy()

    # --------------------------------------------------
    # City Filtering
    # --------------------------------------------------

    if "city" in context and context["city"]:
        city_filtered = candidates[
            candidates["city"].str.lower() == context["city"].lower()
        ]

        if len(city_filtered) > 0:
            candidates = city_filtered

    # --------------------------------------------------
    # Feature Engineering
    # --------------------------------------------------

    candidates["similarity_norm"] = normalize(candidates["similarity_score"])
    candidates["rating_norm"] = normalize(candidates["rating_num"])
    candidates["popularity_norm"] = normalize(candidates["rating_count_num"])

    context_food_types = context["recommended_food_types"]

    candidates["context_score"] = candidates.apply(
        lambda row: compute_context_score(row, context_food_types),
        axis=1
    )

    candidates["preference_score"] = 0

    if user_id is not None:
        user_preferences = get_user_preferences(user_id)

        candidates["preference_score"] = candidates.apply(
            lambda row: compute_preference_score(row, user_preferences),
            axis=1
        )

    # --------------------------------------------------
    # Log Candidate Features
    # --------------------------------------------------

    # store_candidate_features(candidates)

    # --------------------------------------------------
    # Ranking Strategy
    # --------------------------------------------------

    if ML_MODEL_AVAILABLE:
        try:
            ranked = ml_rank(candidates)
        except Exception:
            # fallback if model crashes
            ranked = rule_based_rank(candidates)
    else:
        ranked = rule_based_rank(candidates)

    return ranked


def recommend_food(query, context, user_id=None, top_k=10):
    """
    High-level orchestration function: candidate retrieval + ranking.
    
    Args:
        query: Search query string
        context: Context dict with 'recommended_food_types', optional 'city'
        user_id: Optional user ID for personalization
        top_k: Number of final recommendations to return
    
    Returns:
        DataFrame with top_k ranked food recommendations
    """

    # --------------------------------------------------
    # Stage 1: Candidate Retrieval (FAISS)
    # --------------------------------------------------

    candidates = generate_candidates(query, top_k=300)

    if candidates is None or len(candidates) == 0:
        return []

    # --------------------------------------------------
    # Stage 2: Ranking
    # --------------------------------------------------

    ranked = rank_candidates(candidates, context, user_id)

    # --------------------------------------------------
    # Return top recommendations
    # --------------------------------------------------

    return ranked.head(top_k)