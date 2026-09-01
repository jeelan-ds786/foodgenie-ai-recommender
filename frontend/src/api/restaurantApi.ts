import axios from "axios";

const API_BASE_URL = "http://localhost:8000/v1";

export interface Dish {
  dish_name: string;
  category: string;
  veg_or_non_veg: string;
  rating?: number;
  rating_count?: number;
}

export interface Cuisine {
  cuisine_name: string;
  dish_count: number;
  dishes: Dish[];
}

export interface RestaurantDetail {
  restaurant_name: string;
  city: string;
  total_dishes: number;
  cuisines: Cuisine[];
}

export async function fetchRestaurantDetails(
  restaurantName: string,
  city?: string
): Promise<RestaurantDetail> {
  try {
    const encodedName = encodeURIComponent(restaurantName);
    const url = city
      ? `${API_BASE_URL}/restaurant/${encodedName}?city=${city}`
      : `${API_BASE_URL}/restaurant/${encodedName}`;

    const response = await axios.get(url);
    return response.data;
  } catch (error) {
    console.error("Failed to fetch restaurant details:", error);
    throw error;
  }
}

export async function fetchRestaurantDishes(
  restaurantName: string,
  cuisine?: string,
  city?: string
): Promise<{ restaurant_name: string; cuisine?: string; city?: string; dishes: Dish[] }> {
  try {
    const encodedName = encodeURIComponent(restaurantName);
    const params = new URLSearchParams();
    if (cuisine) params.append("cuisine", cuisine);
    if (city) params.append("city", city);

    const url = `${API_BASE_URL}/restaurant/${encodedName}/dishes${
      params.toString() ? `?${params.toString()}` : ""
    }`;

    const response = await axios.get(url);
    return response.data;
  } catch (error) {
    console.error("Failed to fetch restaurant dishes:", error);
    throw error;
  }
}
