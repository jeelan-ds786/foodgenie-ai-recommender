export interface FoodRecommendation {
  restaurant_name: string
  dish_name: string
  city: string
  score: number
}

export interface Props {
    food: FoodRecommendation;
}