import { useDeferredValue, useEffect, useState } from "react";
import { useParams, useNavigate, useSearchParams } from "react-router-dom";
import {
  ArrowLeft,
  ChefHat,
  Drumstick,
  Leaf,
  MapPin,
  Search,
  Sparkles,
  Star,
  Store,
  Utensils,
} from "lucide-react";
import {
  fetchRestaurantDetails,
  type RestaurantDetail,
} from "../api/restaurantApi";
import CuisineRail from "../components/cuisinerail/CuisineRail";

type DietFilter = "all" | "veg" | "non-veg";
const ALL_CUISINES = "all";

export default function RestaurantPage() {
  const { restaurantName } = useParams<{ restaurantName: string }>();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const selectedDish = searchParams.get("dish")?.trim() ?? "";
  const selectedCity = searchParams.get("city")?.trim() || undefined;
  const [restaurant, setRestaurant] = useState<RestaurantDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [menuQuery, setMenuQuery] = useState("");
  const [dietFilter, setDietFilter] = useState<DietFilter>("all");
  const [cuisineFilter, setCuisineFilter] = useState(ALL_CUISINES);
  const deferredMenuQuery = useDeferredValue(menuQuery);

  useEffect(() => {
    if (!restaurantName) return;

    const loadRestaurantDetails = async () => {
      setLoading(true);
      setError(null);

      try {
        const data = await fetchRestaurantDetails(restaurantName, selectedCity);
        setRestaurant(data);
      } catch (err) {
        setError("Failed to load restaurant details. Please try again.");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    loadRestaurantDetails();
  }, [restaurantName, selectedCity]);

  if (loading) {
    return (
      <main className="restaurant-status" aria-live="polite">
        <span className="loader restaurant-loader" aria-hidden="true" />
        <strong>Preparing the menu</strong>
        <span>Gathering every dish from this restaurant...</span>
      </main>
    );
  }

  if (error || !restaurant) {
    return (
      <main className="restaurant-status restaurant-error" role="alert">
        <Store size={34} aria-hidden="true" />
        <h1>We couldn't open this menu</h1>
        <p>{error || "Restaurant not found"}</p>
        <button
          className="restaurant-primary-action"
          onClick={() => navigate("/")}
        >
          <ArrowLeft size={18} aria-hidden="true" /> Back to search
        </button>
      </main>
    );
  }

  const normalizedQuery = deferredMenuQuery.trim().toLocaleLowerCase();
  const isVegetarian = (diet?: string) =>
    diet?.trim().toLocaleLowerCase() === "veg";
  const selectedDishKey = selectedDish.toLocaleLowerCase();
  const featuredMatch = restaurant.cuisines
    .flatMap((cuisine) =>
      cuisine.dishes.map((dish) => ({
        dish,
        cuisineName: cuisine.cuisine_name,
      })),
    )
    .find(({ dish }) => dish.dish_name.toLocaleLowerCase() === selectedDishKey);
  const allDishes = restaurant.cuisines.flatMap((cuisine) =>
    cuisine.dishes.filter(
      (dish) => dish.dish_name.toLocaleLowerCase() !== selectedDishKey,
    ),
  );
  const vegDishCount = allDishes.filter((dish) =>
    isVegetarian(dish.veg_or_non_veg),
  ).length;
  const nonVegDishCount = allDishes.length - vegDishCount;
  const filteredCuisines = restaurant.cuisines
    .filter(
      (cuisine) =>
        cuisineFilter === ALL_CUISINES ||
        cuisine.cuisine_name === cuisineFilter,
    )
    .map((cuisine) => ({
      ...cuisine,
      dishes: cuisine.dishes.filter((dish) => {
        if (dish.dish_name.toLocaleLowerCase() === selectedDishKey) {
          return false;
        }

        const matchesQuery =
          !normalizedQuery ||
          [dish.dish_name, dish.category, dish.veg_or_non_veg].some((value) =>
            value?.toLocaleLowerCase().includes(normalizedQuery),
          );
        const dishIsVeg = isVegetarian(dish.veg_or_non_veg);
        const matchesDiet =
          dietFilter === "all" ||
          (dietFilter === "veg" ? dishIsVeg : !dishIsVeg);

        return matchesQuery && matchesDiet;
      }),
    }))
    .filter((cuisine) => cuisine.dishes.length > 0);

  const visibleDishCount = filteredCuisines.reduce(
    (total, cuisine) => total + cuisine.dishes.length,
    0,
  );

  return (
    <main className="restaurant-page">
      <header className="restaurant-nav">
        <a className="brand" href="/" aria-label="FoodGenie home">
          <span className="brand-mark" aria-hidden="true">
            FG
          </span>
          <span>FoodGenie</span>
        </a>
        <button className="restaurant-back" onClick={() => navigate("/")}>
          <ArrowLeft size={18} aria-hidden="true" /> Back to results
        </button>
      </header>

      <section className="restaurant-hero" aria-labelledby="restaurant-name">
        <div className="restaurant-hero-inner">
          <div className="restaurant-monogram" aria-hidden="true">
            <ChefHat size={34} />
          </div>
          <div className="restaurant-intro">
            <span className="section-kicker">Restaurant menu</span>
            <h1 id="restaurant-name">{restaurant.restaurant_name}</h1>
            <div className="restaurant-facts" aria-label="Restaurant details">
              <span>
                <MapPin size={17} aria-hidden="true" /> {restaurant.city}
              </span>
              <span>
                <Utensils size={17} aria-hidden="true" />{" "}
                {restaurant.total_dishes} dishes
              </span>
              <span>
                <ChefHat size={17} aria-hidden="true" />{" "}
                {restaurant.cuisines.length}{" "}
                {restaurant.cuisines.length === 1 ? "cuisine" : "cuisines"}
              </span>
            </div>
          </div>
        </div>
      </section>

      <section className="menu-shell" aria-labelledby="menu-title">
        {featuredMatch && (
          <article
            className="featured-dish"
            aria-labelledby="featured-dish-name"
          >
            <div className="featured-dish-accent" aria-hidden="true">
              <Sparkles size={38} />
            </div>
            <div className="featured-dish-content">
              <span className="featured-dish-kicker">
                <Sparkles size={14} aria-hidden="true" /> Your recommendation
              </span>
              <h2 id="featured-dish-name">{featuredMatch.dish.dish_name}</h2>
              <p>
                The dish that brought you here, featured from{" "}
                {restaurant.restaurant_name}.
              </p>
              <div className="featured-dish-meta">
                <span
                  className={`diet-mark ${
                    isVegetarian(featuredMatch.dish.veg_or_non_veg)
                      ? "is-veg"
                      : "is-non-veg"
                  }`}
                >
                  {isVegetarian(featuredMatch.dish.veg_or_non_veg) ? (
                    <Leaf size={14} aria-hidden="true" />
                  ) : (
                    <Drumstick size={14} aria-hidden="true" />
                  )}
                  {isVegetarian(featuredMatch.dish.veg_or_non_veg)
                    ? "Veg"
                    : "Non-veg"}
                </span>
                <span>{featuredMatch.cuisineName}</span>
                <span>{featuredMatch.dish.category || "House specialty"}</span>
                {featuredMatch.dish.rating !== undefined &&
                  featuredMatch.dish.rating > 0 && (
                    <span className="featured-dish-rating">
                      <Star size={14} fill="currentColor" aria-hidden="true" />
                      {featuredMatch.dish.rating.toFixed(1)}
                      {Boolean(featuredMatch.dish.rating_count) &&
                        ` (${featuredMatch.dish.rating_count?.toLocaleString()} ratings)`}
                    </span>
                  )}
              </div>
            </div>
          </article>
        )}

        <div className="menu-toolbar">
          <div>
            <span className="section-kicker">Explore the menu</span>
            <h2 id="menu-title">Find your next favorite</h2>
          </div>
          <label className="menu-search">
            <Search size={19} aria-hidden="true" />
            <span className="sr-only">Search this menu</span>
            <input
              type="search"
              value={menuQuery}
              onChange={(event) => setMenuQuery(event.target.value)}
              placeholder="Search dishes or categories"
            />
          </label>
        </div>

        <div className="diet-filter-scroll" aria-label="Filter menu by diet">
          <div className="diet-filter" role="group">
            <button
              className={dietFilter === "all" ? "is-active" : ""}
              type="button"
              aria-pressed={dietFilter === "all"}
              onClick={() => setDietFilter("all")}
            >
              All <span>{allDishes.length}</span>
            </button>
            <button
              className={`diet-filter-veg ${dietFilter === "veg" ? "is-active" : ""}`}
              type="button"
              aria-pressed={dietFilter === "veg"}
              onClick={() => setDietFilter("veg")}
            >
              <Leaf size={15} aria-hidden="true" /> Veg{" "}
              <span>{vegDishCount}</span>
            </button>
            <button
              className={`diet-filter-non-veg ${dietFilter === "non-veg" ? "is-active" : ""}`}
              type="button"
              aria-pressed={dietFilter === "non-veg"}
              onClick={() => setDietFilter("non-veg")}
            >
              <Drumstick size={15} aria-hidden="true" /> Non-veg{" "}
              <span>{nonVegDishCount}</span>
            </button>
          </div>
        </div>

        <div className="cuisine-filter" aria-label="Filter menu by cuisine">
          <label htmlFor="cuisine-filter-select">Cuisine</label>
          <select
            id="cuisine-filter-select"
            value={cuisineFilter}
            onChange={(event) => setCuisineFilter(event.target.value)}
          >
            <option value={ALL_CUISINES}>All cuisines</option>
            {restaurant.cuisines.map((cuisine) => {
              const regularDishCount = cuisine.dishes.filter(
                (dish) =>
                  dish.dish_name.toLocaleLowerCase() !== selectedDishKey,
              ).length;

              return (
                <option key={cuisine.cuisine_name} value={cuisine.cuisine_name}>
                  {cuisine.cuisine_name} ({regularDishCount})
                </option>
              );
            })}
          </select>
        </div>

        {(menuQuery ||
          dietFilter !== "all" ||
          cuisineFilter !== ALL_CUISINES) && (
          <p className="menu-result-count" aria-live="polite">
            {visibleDishCount} {visibleDishCount === 1 ? "dish" : "dishes"}{" "}
            found
          </p>
        )}

        {filteredCuisines.length === 0 ? (
          <div className="menu-empty">
            <Search size={28} aria-hidden="true" />
            <strong>No dishes match these filters</strong>
            <span>Try another dish, category, or dietary option.</span>
            <button
              onClick={() => {
                setMenuQuery("");
                setDietFilter("all");
                setCuisineFilter(ALL_CUISINES);
              }}
            >
              Clear filters
            </button>
          </div>
        ) : (
          filteredCuisines.map((cuisine) => (
            <CuisineRail
              key={cuisine.cuisine_name}
              cuisineName={cuisine.cuisine_name}
              dishes={cuisine.dishes}
              isFiltering={
                Boolean(normalizedQuery) ||
                dietFilter !== "all" ||
                cuisineFilter !== ALL_CUISINES
              }
            />
          ))
        )}
      </section>
    </main>
  );
}
