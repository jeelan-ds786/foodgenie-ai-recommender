import type { FoodRecommendation } from "../types";

interface FoodCardProps {
  food: FoodRecommendation;
}

export default function FoodCard({ food }: FoodCardProps) {
  if (!food) {
    return null;
  }

  return (
    <div
      style={{
        border: "1px solid #ddd",
        padding: "20px",
        borderRadius: "10px",
        backgroundColor: "#fff",
        boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
        transition: "transform 0.2s, box-shadow 0.2s",
      }}
      onMouseEnter={(e) => {
        e.currentTarget.style.transform = "translateY(-5px)";
        e.currentTarget.style.boxShadow = "0 4px 8px rgba(0,0,0,0.15)";
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.transform = "translateY(0)";
        e.currentTarget.style.boxShadow = "0 2px 4px rgba(0,0,0,0.1)";
      }}
    >
      <h3 style={{ margin: "0 0 10px 0", color: "#333", fontSize: "18px" }}>
        {food.dish_name ?? "Unknown Dish"}
      </h3>

      <p style={{ margin: "5px 0", color: "#666", fontSize: "14px" }}>
        🏪 {food.restaurant_name ?? "Unknown Restaurant"}
      </p>

      <p style={{ margin: "5px 0", color: "#666", fontSize: "14px" }}>
        📍 {food.city ?? "Unknown City"}
      </p>

      <p style={{ margin: "10px 0 0 0", fontWeight: "bold", color: "#4CAF50" }}>
        Score: {food.score?.toFixed(3) ?? "N/A"}
      </p>
    </div>
  );
}
