import { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  ArrowRight,
  Check,
  Heart,
  MapPin,
  ShoppingBag,
  Store,
  X,
} from "lucide-react";
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
  const navigate = useNavigate();
  const [isLiked, setIsLiked] = useState(false);
  const [isSkipped, setIsSkipped] = useState(false);
  const [isOrdered, setIsOrdered] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  if (!food) {
    return null;
  }

  const handleCardClick = () => {
    const encodedName = encodeURIComponent(food.restaurant_name);
    const params = new URLSearchParams({
      dish: food.dish_name,
      city: food.city,
    });
    navigate(`/restaurant/${encodedName}?${params.toString()}`);
  };

  const handleCardKeyDown = (event: React.KeyboardEvent<HTMLElement>) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      handleCardClick();
    }
  };

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
    <article
      onClick={handleCardClick}
      onKeyDown={handleCardKeyDown}
      className={`food-card${isSkipped ? " is-skipped" : ""}`}
      tabIndex={0}
      aria-label={`View ${food.restaurant_name}`}
    >
      <div className="card-topline">
        <span className="match-score">
          {Math.round((food.score ?? 0) * 100)}% match
        </span>
        <ArrowRight size={19} aria-hidden="true" />
      </div>
      <h3>{food.dish_name ?? "Unknown Dish"}</h3>
      <div className="food-meta">
        <span>
          <Store size={16} aria-hidden="true" />{" "}
          {food.restaurant_name ?? "Unknown Restaurant"}
        </span>
        <span>
          <MapPin size={16} aria-hidden="true" /> {food.city ?? "Unknown City"}
        </span>
      </div>
      <div
        className="card-actions"
        aria-label={`Actions for ${food.dish_name}`}
      >
        <button
          onClick={handleLike}
          disabled={isLoading}
          className={isLiked ? "is-active like-action" : ""}
          aria-pressed={isLiked}
        >
          <Heart
            size={17}
            fill={isLiked ? "currentColor" : "none"}
            aria-hidden="true"
          />{" "}
          {isLiked ? "Liked" : "Like"}
        </button>
        <button
          onClick={handleSkip}
          disabled={isLoading}
          className={isSkipped ? "is-active skip-action" : ""}
          aria-pressed={isSkipped}
        >
          <X size={17} aria-hidden="true" /> {isSkipped ? "Skipped" : "Skip"}
        </button>
        <button
          onClick={handleOrder}
          disabled={isLoading}
          className="order-action"
          aria-pressed={isOrdered}
        >
          {isOrdered ? (
            <Check size={17} aria-hidden="true" />
          ) : (
            <ShoppingBag size={17} aria-hidden="true" />
          )}
          {isOrdered ? "Ordered" : "Order"}
        </button>
      </div>
      {isLoading && (
        <div className="card-loading">
          <span className="loader" aria-label="Saving feedback" />
        </div>
      )}
    </article>
  );
}
