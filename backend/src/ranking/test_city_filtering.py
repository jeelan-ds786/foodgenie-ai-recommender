import pandas as pd

from ranking.ranking_engine import rank_candidates


def test_rank_candidates_does_not_fall_back_to_other_cities():
    candidates = pd.DataFrame(
        {
            "dish_name": ["Parotta", "Veechu Parotta"],
            "city": ["Madurai", "Vellore"],
            "similarity_score": [0.9, 0.8],
            "rating_num": [4.5, 4.4],
            "rating_count_num": [100, 80],
        }
    )
    context = {"city": "Chennai", "recommended_food_types": []}

    ranked = rank_candidates(candidates, context)

    assert ranked.empty