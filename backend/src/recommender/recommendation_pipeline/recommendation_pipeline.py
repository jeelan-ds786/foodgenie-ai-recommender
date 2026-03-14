from recommender.candidate_generator import generate_candidates
from context.context_engine import get_context_preferences
from ranking.ranking_engine import rank_candidates


def recommend_food(query: str, city: str = "Chennai", top_k: int = 10):

    candidates = generate_candidates(query, top_k=1000)

    city_filtered = candidates[candidates["city"].str.lower() == city.lower()]

    if len(city_filtered) > 0:
        candidates = city_filtered

    context = get_context_preferences(city)

    ranked_results = rank_candidates(candidates, context)

    return ranked_results.head(top_k)