from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import pandas as pd
from pathlib import Path

router = APIRouter()

# Load the preprocessed data
BASE_DIR = Path(__file__).resolve().parents[3]
DATA_FILE = BASE_DIR.parent.parent / "data" / "processed" / "dataPreprocessed_FoodGenie_Dataset.parquet"


class RestaurantDetailResponse(BaseModel):
    restaurant_name: str
    city: str
    total_dishes: int
    cuisines: list[dict]


@router.get("/restaurant/{restaurant_name}")
def get_restaurant_details(restaurant_name: str, city: str = None):
    """
    Get detailed information about a restaurant including all cuisines and dishes
    """
    try:
        # Load data
        df = pd.read_parquet(DATA_FILE)
        
        # URL decode restaurant name (replace %20 with spaces, etc.)
        from urllib.parse import unquote
        restaurant_name = unquote(restaurant_name)
        
        # Filter by restaurant name
        restaurant_df = df[df['restaurant_name'] == restaurant_name]
        
        # Optionally filter by city
        if city:
            restaurant_df = restaurant_df[restaurant_df['city'] == city]
        
        if restaurant_df.empty:
            raise HTTPException(status_code=404, detail=f"Restaurant '{restaurant_name}' not found")
        
        # Get unique cuisines and their dishes
        cuisines_data = []
        
        for cuisine in restaurant_df['cuisine'].unique():
            cuisine_df = restaurant_df[restaurant_df['cuisine'] == cuisine]
            
            dishes = []
            for _, row in cuisine_df.iterrows():
                dish = {
                    "dish_name": row['dish_name'],
                    "category": row.get('category', 'Unknown'),
                    "veg_or_non_veg": row.get('veg_or_non_veg', 'Unknown'),
                    "rating": float(row.get('rating_num', 0)) if pd.notna(row.get('rating_num')) else None,
                    "rating_count": int(row.get('rating_count_num', 0)) if pd.notna(row.get('rating_count_num')) else None,
                }
                dishes.append(dish)
            
            cuisines_data.append({
                "cuisine_name": cuisine,
                "dish_count": len(dishes),
                "dishes": dishes
            })
        
        # Get restaurant city (take first one if multiple)
        city_value = restaurant_df['city'].iloc[0] if not restaurant_df.empty else "Unknown"
        
        return {
            "restaurant_name": restaurant_name,
            "city": city_value,
            "total_dishes": len(restaurant_df),
            "cuisines": cuisines_data
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching restaurant details: {str(e)}")


@router.get("/restaurant/{restaurant_name}/dishes")
def get_restaurant_dishes(restaurant_name: str, cuisine: str = None, city: str = None):
    """
    Get all dishes from a restaurant, optionally filtered by cuisine
    """
    try:
        # Load data
        df = pd.read_parquet(DATA_FILE)
        
        # URL decode restaurant name
        from urllib.parse import unquote
        restaurant_name = unquote(restaurant_name)
        
        # Filter by restaurant
        restaurant_df = df[df['restaurant_name'] == restaurant_name]
        
        if city:
            restaurant_df = restaurant_df[restaurant_df['city'] == city]
        
        if cuisine:
            restaurant_df = restaurant_df[restaurant_df['cuisine'] == cuisine]
        
        if restaurant_df.empty:
            return {"dishes": []}
        
        dishes = []
        for _, row in restaurant_df.iterrows():
            dish = {
                "dish_name": row['dish_name'],
                "cuisine": row['cuisine'],
                "category": row.get('category', 'Unknown'),
                "veg_or_non_veg": row.get('veg_or_non_veg', 'Unknown'),
                "rating": float(row.get('rating_num', 0)) if pd.notna(row.get('rating_num')) else None,
                "rating_count": int(row.get('rating_count_num', 0)) if pd.notna(row.get('rating_count_num')) else None,
            }
            dishes.append(dish)
        
        return {
            "restaurant_name": restaurant_name,
            "cuisine": cuisine,
            "city": city,
            "dishes": dishes
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching dishes: {str(e)}")
