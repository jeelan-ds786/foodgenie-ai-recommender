import requests
import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).parent.parent.parent.parent / ".env"
load_dotenv(env_path)

API_KEY = os.getenv("OPENWEATHER_API_KEY", "default_key")

def get_weather(city="Chennai"):

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"

    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        
        if "weather" not in data:
            return "default"
        
        weather = data["weather"][0]["main"].lower()
        return weather
    except (requests.RequestException, KeyError, IndexError):
        return "default"


WEATHER_FOOD_RULES = {

    "rain": ["soup", "ramen", "hot chocolate"],

    "clear": ["juice", "ice cream"],

    "clouds": ["coffee", "snacks"],

    "mist": ["tea", "pakora"]
}