import pandas as pd

from features.feature_pipeline import store_candidate_features


def normalize(series):
    return (series - series.min()) / (series.max() - series.min()+1e-8)


def compute_context_score(row, context_food_types):

    '''checking food matches with context preferences'''

    food_name = str(row["dish_name"]).lower()

    for keyword in context_food_types:
        if keyword in food_name:
            return 1.0  

    return 0.0


def rank_candidates(candidates: pd.DataFrame, context):

    candidates = candidates.copy()

    store_candidate_features(candidates)

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

    candidates["final_score"] = (

        0.5 * candidates["similarity_norm"]
        + 0.2 * candidates["rating_norm"]
        + 0.2 * candidates["popularity_norm"]
        + 0.1 * candidates["context_score"]

    )

    ranked = candidates.sort_values("final_score", ascending=False)

    return ranked