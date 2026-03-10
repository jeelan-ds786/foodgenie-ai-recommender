try:
    from context.context_intents.time_context import get_time_of_day, TIME_FOOD_RULES
    from context.context_intents.weather_context import get_weather, WEATHER_FOOD_RULES
except ImportError:
    from time_context import get_time_of_day, TIME_FOOD_RULES
    from weather_context import get_weather, WEATHER_FOOD_RULES


def get_context_preferences(city="Chennai"):

    time_of_day = get_time_of_day()

    weather = get_weather(city)

    time_foods = TIME_FOOD_RULES.get(time_of_day, [])

    weather_foods = WEATHER_FOOD_RULES.get(weather, [])

    context_foods = list(set(time_foods + weather_foods))

    return {
        "time_of_day": time_of_day,
        "weather": weather,
        "recommended_food_types": context_foods
    }