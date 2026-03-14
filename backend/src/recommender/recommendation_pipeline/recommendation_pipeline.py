from recommender.candidate_generator import generate_candidates
from context.context_engine import get_context_preferences
from ranking.ranking_engine import rank_candidates


def recommend_food(query: str, city: str, user_id: int = None, top_k: int = 10):


    candidates = generate_candidates(query, top_k=1000)

    context = get_context_preferences(city)

    context["city"] = city


    ranked_results = rank_candidates(
        candidates=candidates,
        context=context,
        user_id=user_id
    )

    return ranked_results.head(top_k)