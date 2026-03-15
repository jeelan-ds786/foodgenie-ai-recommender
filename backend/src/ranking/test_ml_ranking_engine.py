from recommender.candidate_generator import generate_candidates
from context.context_engine import get_context_preferences
from ranking.ranking_engine import rank_candidates


def test_ml_ranking():

    query = "chicken"

    city = "madurai"

    user_id = 1

    candidates = generate_candidates(query, top_k=200)

    print("\nCandidates retrieved:", len(candidates))

    context = get_context_preferences(city)

    context["city"] = city

    # Step 3: ranking
    ranked = rank_candidates(
        candidates=candidates,
        context=context,
        user_id=user_id
    )

    print("\nTop Ranked Foods:\n")

    print(
        ranked[
            [
                "restaurant_name",
                "dish_name",
                "city",
                "similarity_score",
                "context_score",
                "preference_score",
                "ml_score"
            ]
        ].head(10)
    )


if __name__ == "__main__":
    test_ml_ranking()