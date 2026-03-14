import pandas as pd
from personalization.personalization_engine import get_user_preferences


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


def rank_candidates(candidates: pd.DataFrame, context, user_id=None):

    candidates = candidates.copy()


    if "city" in context and context["city"]:
        city_filtered = candidates[
            candidates["city"].str.lower() == context["city"].lower()
        ]

        if len(city_filtered) > 0:
            candidates = city_filtered


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


    candidates["final_score"] = (

        0.45 * candidates["similarity_norm"]
        + 0.20 * candidates["rating_norm"]
        + 0.20 * candidates["popularity_norm"]
        + 0.10 * candidates["context_score"]
        + 0.05 * candidates["preference_score"]
    )

    ranked = candidates.sort_values("final_score", ascending=False)

    return ranked