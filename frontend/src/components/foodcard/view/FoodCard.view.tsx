import { useState } from "react";
import type { FoodRecommendation } from "../types";
import {
  likeFoodItem,
  unlikeFoodItem,
  skipFoodItem,
  unskipFoodItem,
  orderFoodItem,
  unorderFoodItem,
} from "../../../api/feedbackApi";

interface FoodCardProps {
  food: FoodRecommendation;
}

export default function FoodCard({ food }: FoodCardProps) {
  const [isLiked, setIsLiked] = useState(false);
  const [isSkipped, setIsSkipped] = useState(false);
  const [isOrdered, setIsOrdered] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  if (!food) {
    return null;
  }

  const handleLike = async (e: React.MouseEvent) => {
    e.stopPropagation();
    if (isLoading) return;

    setIsLoading(true);
    try {
      if (isLiked) {
        // Remove like
        console.log("🗑️ Removing like for:", food.dish_name);
        const response = await unlikeFoodItem(food.dish_name);
        console.log("✅ Unlike response:", response);
        setIsLiked(false);
      } else {
        // Add like
        console.log("❤️ Adding like for:", food.dish_name);
        const response = await likeFoodItem(food.dish_name);
        console.log("✅ Like response:", response);
        setIsLiked(true);
      }
    } catch (error) {
      console.error("❌ Failed to toggle like:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSkip = async (e: React.MouseEvent) => {
    e.stopPropagation();
    if (isLoading) return;

    setIsLoading(true);
    try {
      if (isSkipped) {
        // Remove skip
        await unskipFoodItem(food.dish_name);
        setIsSkipped(false);
        console.log("Unskipped:", food.dish_name);
      } else {
        // Add skip
        await skipFoodItem(food.dish_name);
        setIsSkipped(true);
        console.log("Skipped:", food.dish_name);
      }
    } catch (error) {
      console.error("Failed to toggle skip:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleOrder = async (e: React.MouseEvent) => {
    e.stopPropagation();
    if (isLoading) return;

    setIsLoading(true);
    try {
      if (isOrdered) {
        // Remove order
        await unorderFoodItem(food.dish_name);
        setIsOrdered(false);
        console.log("Unordered:", food.dish_name);
      } else {
        // Add order
        await orderFoodItem(food.dish_name);
        setIsOrdered(true);
        console.log("Ordered:", food.dish_name);
      }
    } catch (error) {
      console.error("Failed to toggle order:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div
      style={{
        border: "1px solid #ddd",
        padding: "20px",
        borderRadius: "10px",
        backgroundColor: "#fff",
        boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
        transition: "transform 0.2s, box-shadow 0.2s",
        opacity: isSkipped ? 0.5 : 1,
        position: "relative",
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

      {/* Action Buttons */}
      <div
        style={{
          display: "flex",
          gap: "10px",
          marginTop: "15px",
          justifyContent: "space-between",
        }}
      >
        <button
          onClick={handleLike}
          disabled={isLoading}
          style={{
            flex: 1,
            padding: "10px 15px",
            border: "none",
            borderRadius: "6px",
            backgroundColor: isLiked ? "#4CAF50" : "#f0f0f0",
            color: isLiked ? "#fff" : "#333",
            fontSize: "14px",
            fontWeight: "500",
            cursor: isLoading ? "not-allowed" : "pointer",
            transition: "all 0.2s",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            gap: "5px",
          }}
          onMouseEnter={(e) => {
            if (!isLoading) {
              (e.target as HTMLButtonElement).style.backgroundColor = isLiked
                ? "#45a049"
                : "#e0e0e0";
            }
          }}
          onMouseLeave={(e) => {
            (e.target as HTMLButtonElement).style.backgroundColor = isLiked
              ? "#4CAF50"
              : "#f0f0f0";
          }}
        >
          <span style={{ fontSize: "16px" }}>{isLiked ? "❤️" : "🤍"}</span>
          <span>{isLiked ? "Liked" : "Like"}</span>
        </button>

        <button
          onClick={handleSkip}
          disabled={isLoading}
          style={{
            flex: 1,
            padding: "10px 15px",
            border: "none",
            borderRadius: "6px",
            backgroundColor: isSkipped ? "#9e9e9e" : "#f0f0f0",
            color: isSkipped ? "#fff" : "#333",
            fontSize: "14px",
            fontWeight: "500",
            cursor: isLoading ? "not-allowed" : "pointer",
            transition: "all 0.2s",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            gap: "5px",
          }}
          onMouseEnter={(e) => {
            if (!isLoading) {
              (e.target as HTMLButtonElement).style.backgroundColor = isSkipped
                ? "#757575"
                : "#e0e0e0";
            }
          }}
          onMouseLeave={(e) => {
            (e.target as HTMLButtonElement).style.backgroundColor = isSkipped
              ? "#9e9e9e"
              : "#f0f0f0";
          }}
        >
          <span style={{ fontSize: "16px" }}>⏭️</span>
          <span>{isSkipped ? "Skipped" : "Skip"}</span>
        </button>

        <button
          onClick={handleOrder}
          disabled={isLoading}
          style={{
            flex: 1,
            padding: "10px 15px",
            border: "none",
            borderRadius: "6px",
            backgroundColor: isOrdered ? "#FF9800" : "#FF5722",
            color: "#fff",
            fontSize: "14px",
            fontWeight: "500",
            cursor: isLoading ? "not-allowed" : "pointer",
            transition: "all 0.2s",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            gap: "5px",
          }}
          onMouseEnter={(e) => {
            if (!isLoading) {
              (e.target as HTMLButtonElement).style.backgroundColor = isOrdered
                ? "#F57C00"
                : "#E64A19";
            }
          }}
          onMouseLeave={(e) => {
            (e.target as HTMLButtonElement).style.backgroundColor = isOrdered
              ? "#FF9800"
              : "#FF5722";
          }}
        >
          <span style={{ fontSize: "16px" }}>{isOrdered ? "✅" : "🛒"}</span>
          <span>{isOrdered ? "Ordered" : "Order"}</span>
        </button>
      </div>

      {/* Loading indicator */}
      {isLoading && (
        <div
          style={{
            position: "absolute",
            top: "50%",
            left: "50%",
            transform: "translate(-50%, -50%)",
            backgroundColor: "rgba(255, 255, 255, 0.9)",
            padding: "10px 20px",
            borderRadius: "6px",
            boxShadow: "0 2px 8px rgba(0,0,0,0.2)",
          }}
        >
          Loading...
        </div>
      )}
    </div>
  );
}
