import { FoodCard } from "../../foodcard";
import type { FoodRecommendation } from "../types";

interface Props {
  foods: FoodRecommendation[];
}

export default function ResultsGrid({ foods }: Props) {
  if (!foods.length) return null;

  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns: "repeat(3,1fr)",
        gap: "20px",
        marginTop: "20px",
      }}
    >
      {foods.map((food, index) => (
        <FoodCard key={index} food={food} />
      ))}
    </div>
  );
}
