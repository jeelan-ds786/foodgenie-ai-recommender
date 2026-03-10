from datetime import datetime

def get_time_of_day():

    hour = datetime.now().hour

    if 5 <= hour < 11:
        return "morning"
    elif 11 <= hour < 16:
        return "lunch"
    elif 16 <= hour < 21:
        return "dinner"
    else:
        return "late_night"
    
TIME_FOOD_RULES = {
    "morning": ["dosa", "idli", "pongal", "upma"],
    "lunch": ["meals", "rice", "biryani"],
    "dinner": ["biryani", "fried rice", "noodles"],
    "late_night": ["pizza", "burger", "shawarma"]
}