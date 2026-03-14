from recommender.candidate_generator import generate_candidates
from context.context_engine import get_context_preferences
from ranking.ranking_engine import rank_candidates


query = "parotta mutton chukka"


candidates = generate_candidates(query,top_k=200)

print(candidates["city"].value_counts().head(20))

candidates = candidates[candidates["city"].str.lower() == "madurai"]

context = get_context_preferences("madurai")

ranked_results = rank_candidates(candidates, context)

print("\nTop Ranked Foods:\n")

print(
    ranked_results[
        ["restaurant_name", "dish_name", "final_score", "city"]
    ].head(10)
)