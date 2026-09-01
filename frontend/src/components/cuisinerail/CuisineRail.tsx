import { useState } from "react";
import { ChevronDown, ChevronUp, Leaf, Star, Utensils } from "lucide-react";
import type { Dish } from "../../api/restaurantApi";

interface CuisineRailProps {
  cuisineName: string;
  dishes: Dish[];
  isFiltering?: boolean;
}

const INITIAL_DISH_COUNT = 12;

export default function CuisineRail({
  cuisineName,
  dishes,
  isFiltering = false,
}: CuisineRailProps) {
  const [isExpanded, setIsExpanded] = useState(false);

  const visibleDishes =
    isExpanded || isFiltering ? dishes : dishes.slice(0, INITIAL_DISH_COUNT);
  const hiddenDishCount = dishes.length - visibleDishes.length;

  return (
    <section
      className="cuisine-section"
      aria-labelledby={`cuisine-${cuisineName}`}
    >
      <div className="cuisine-heading">
        <div>
          <span className="cuisine-icon" aria-hidden="true">
            <Utensils size={18} />
          </span>
          <h3 id={`cuisine-${cuisineName}`}>{cuisineName}</h3>
        </div>
        <span>
          {dishes.length} {dishes.length === 1 ? "dish" : "dishes"}
        </span>
      </div>

      <div className="dish-grid">
        {visibleDishes.map((dish, index) => {
          const isVeg = dish.veg_or_non_veg?.toLocaleLowerCase() === "veg";
          return (
            <article className="dish-card" key={`${dish.dish_name}-${index}`}>
              <div className="dish-card-topline">
                <span
                  className={`diet-mark ${isVeg ? "is-veg" : "is-non-veg"}`}
                >
                  {isVeg ? (
                    <Leaf size={14} aria-hidden="true" />
                  ) : (
                    <Utensils size={14} aria-hidden="true" />
                  )}
                  {isVeg ? "Veg" : "Non-veg"}
                </span>
                {dish.rating !== null &&
                  dish.rating !== undefined &&
                  dish.rating > 0 && (
                    <span className="dish-rating">
                      <Star size={14} fill="currentColor" aria-hidden="true" />
                      {dish.rating.toFixed(1)}
                    </span>
                  )}
              </div>
              <h4 title={dish.dish_name}>{dish.dish_name}</h4>
              <div className="dish-card-footer">
                <span>{dish.category || "House specialty"}</span>
                {Boolean(dish.rating_count) && (
                  <span>{dish.rating_count?.toLocaleString()} ratings</span>
                )}
              </div>
            </article>
          );
        })}
      </div>

      {!isFiltering && dishes.length > INITIAL_DISH_COUNT && (
        <button
          className="menu-expand"
          onClick={() => setIsExpanded((value) => !value)}
        >
          {isExpanded ? (
            <ChevronUp size={18} aria-hidden="true" />
          ) : (
            <ChevronDown size={18} aria-hidden="true" />
          )}
          {isExpanded
            ? "Show fewer dishes"
            : `Show ${hiddenDishCount} more dishes`}
        </button>
      )}
    </section>
  );
}
