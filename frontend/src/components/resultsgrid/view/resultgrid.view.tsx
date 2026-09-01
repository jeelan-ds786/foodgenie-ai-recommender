import { FoodCard } from "../../foodcard";
import type { FoodRecommendation } from "../types";

interface Props {
  foods: FoodRecommendation[];
}

export default function ResultsGrid({ foods }: Props) {
  if (!foods.length) return null;

  return (
    <div className="results-grid">
      {foods.map((food, index) => (
        <FoodCard
          key={`${food.restaurant_name}-${food.dish_name}-${index}`}
          food={food}
        />
      ))}
    </div>
  );
}
