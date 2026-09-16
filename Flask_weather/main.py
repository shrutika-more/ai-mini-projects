import os
import requests

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


def get_weather(city, state, country):

    location = f"{city}, {state}, {country}"

    search_location = location

    # Geocode the location
    geo_response = requests.get(
        GEOCODING_URL,
        params={
            "name": search_location,
            "count": 1,
            "language": "en",
            "format": "json"
        },
        timeout=10
    )

    geo_response.raise_for_status()

    geo_data = geo_response.json()

    if not geo_data.get("results"):
        raise ValueError(
            "Location not found. Please check the city and state."
        )

    place = geo_data["results"][0]

    latitude = place["latitude"]
    longitude = place["longitude"]

    # Get current weather + rainfall data
    weather_response = requests.get(
        WEATHER_URL,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": (
                "temperature_2m,"
                "relative_humidity_2m,"
                "apparent_temperature,"
                "is_day,"
                "precipitation,"
                "rain,"
                "weather_code,"
                "cloud_cover,"
                "wind_speed_10m"
            ),
            "hourly": "precipitation,rain",
            "forecast_days": 1,
            "timezone": "auto"
        },
        timeout=10
    )

    weather_response.raise_for_status()

    weather_data = weather_response.json()

    current = weather_data["current"]

    code = current.get("weather_code", 0)

    condition, icon, animation = weather_condition(code)

    # Current rainfall
    rain = current.get("rain", 0)
    precipitation = current.get("precipitation", 0)

    return {
        "temperature": round(
            current.get("temperature_2m", 0)
        ),

        "feels_like": round(
            current.get("apparent_temperature", 0)
        ),

        "humidity": current.get(
            "relative_humidity_2m", 0
        ),

        "wind": round(
            current.get("wind_speed_10m", 0)
        ),

        "rain": rain,

        "precipitation": precipitation,

        "cloud_cover": current.get(
            "cloud_cover", 0
        ),

        "condition": condition,

        "icon": icon,

        "animation": animation,

        "is_day": current.get(
            "is_day", 1
        ),

        "timezone": weather_data.get(
            "timezone", ""
        ),

        "latitude": latitude,

        "longitude": longitude
    }


def weather_condition(code):

    if code == 0:
        return "Clear Sky", "☀️", "sunny"

    if code in [1, 2]:
        return "Partly Cloudy", "🌤️", "cloudy"

    if code == 3:
        return "Cloudy", "☁️", "cloudy"

    if code in [45, 48]:
        return "Foggy", "🌫️", "foggy"

    if code in [51, 53, 55, 56, 57]:
        return "Drizzle", "🌦️", "rainy"

    if code in [61, 63, 65, 66, 67]:
        return "Rainy", "🌧️", "rainy"

    if code in [71, 73, 75, 77]:
        return "Snowy", "❄️", "winter"

    if code in [80, 81, 82]:
        return "Rain Showers", "🌦️", "rainy"

    if code in [85, 86]:
        return "Snow Showers", "🌨️", "winter"

    if code in [95, 96, 99]:
        return "Thunderstorm", "⛈️", "storm"

    return "Unknown", "🌤️", "cloudy"