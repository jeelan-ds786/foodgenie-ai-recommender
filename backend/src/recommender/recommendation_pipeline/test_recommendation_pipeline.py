from recommender.recommendation_pipeline import recommend_food


query = "spicy chicken"

results = recommend_food(query, city="Erode")

print("\nFoodGenie Recommendations:\n")

print(
    results[
        ["restaurant_name", "dish_name", "ml_score", "city"]
    ]
)