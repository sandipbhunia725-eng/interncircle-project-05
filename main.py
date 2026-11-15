"""
Project 05: Weather App with Live OpenWeather API
InternCircle | Python Programming

Setup:
1. Copy .env.example to .env
2. Add your OpenWeather API key to .env
3. Install packages: pip install -r requirements.txt
4. Run: python main.py

Never commit .env or publish your API key.
"""

import os
import time
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv


BASE_URL = "https://api.openweathermap.org/data/2.5"
CURRENT_WEATHER_URL = f"{BASE_URL}/weather"
FORECAST_URL = f"{BASE_URL}/forecast"
REQUEST_TIMEOUT = 10
CACHE_SECONDS = 300  # Cache results for five minutes.
CACHE = {}


def load_api_key():
    """Load the API key from .env; return None if it is missing."""
    env_path = Path(__file__).with_name(".env")
    load_dotenv(dotenv_path=env_path)
    key = os.getenv("OPENWEATHER_KEY", "").strip()
    if not key or key == "your_key_here":
        print("API key missing. Add OPENWEATHER_KEY=your_key_here to your .env file.")
        return None
    return key


def request_json(endpoint, city, api_key):
    """Request an OpenWeather endpoint and return parsed JSON or None."""
    cache_key = (endpoint, city.casefold())
    cached = CACHE.get(cache_key)
    now = time.time()

    if cached and now - cached["time"] < CACHE_SECONDS:
        print("(Using cached result; cache lasts 5 minutes.)")
        return cached["data"]

    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
    }

    try:
        response = requests.get(
            endpoint,
            params=params,
            timeout=REQUEST_TIMEOUT,
        )
    except requests.exceptions.RequestException:
        print("Network problem. Check your internet connection and try again.")
        return None

    if response.status_code == 404:
        print("City not found. Check the spelling and try again.")
        return None
    if response.status_code == 401:
        print("Invalid or inactive API key (401). Check your key; a new key may take time to activate.")
        return None
    if response.status_code != 200:
        print(f"Weather API error: HTTP {response.status_code}.")
        return None

    try:
        data = response.json()
    except ValueError:
        print("The weather service returned an invalid JSON response.")
        return None

    CACHE[cache_key] = {"time": now, "data": data}
    return data


def get_current_weather(city, api_key):
    """Fetch current weather for a city."""
    return request_json(CURRENT_WEATHER_URL, city, api_key)


def get_forecast(city, api_key):
    """Fetch the 5-day / 3-hour forecast for a city."""
    return request_json(FORECAST_URL, city, api_key)


def display_current_weather(data):
    """Safely display temperature, humidity, description, and wind speed."""
    main = data.get("main") or {}
    weather_items = data.get("weather") or []
    wind = data.get("wind") or {}
    description = "Description unavailable"

    if weather_items and isinstance(weather_items[0], dict):
        description = weather_items[0].get("description", description)

    city_name = data.get("name", "Unknown city")
    temperature = main.get("temp", "N/A")
    humidity = main.get("humidity", "N/A")
    wind_speed = wind.get("speed", "N/A")

    print("\nCURRENT WEATHER")
    print("-" * 42)
    print(f"City        : {city_name}")
    print(f"Temperature : {temperature} °C")
    print(f"Humidity    : {humidity}%")
    print(f"Conditions  : {description}")
    print(f"Wind speed  : {wind_speed} m/s")


def select_daily_forecasts(data, days=5):
    """Select one forecast item per date from the 3-hour forecast response."""
    entries = data.get("list") or []
    selected = {}
    for entry in entries:
        timestamp = entry.get("dt")
        if not timestamp:
            continue
        date_text = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
        if date_text in selected:
            continue
        main = entry.get("main") or {}
        weather_items = entry.get("weather") or []
        description = "Description unavailable"
        if weather_items and isinstance(weather_items[0], dict):
            description = weather_items[0].get("description", description)

        selected[date_text] = {
            "date": date_text,
            "temperature": main.get("temp", "N/A"),
            "description": description,
        }
        if len(selected) >= days:
            break
    return list(selected.values())


def display_forecast(data):
    """Print a compact multi-day forecast table."""
    forecasts = select_daily_forecasts(data)
    print("\n5-DAY FORECAST")
    print("-" * 65)
    print(f"{'Date':<14}{'Temperature':<18}Description")
    print("-" * 65)
    if not forecasts:
        print("Forecast data is unavailable.")
        return

    for item in forecasts:
        temperature = item["temperature"]
        temperature_text = f"{temperature} °C" if temperature != "N/A" else "N/A"
        print(f"{item['date']:<14}{temperature_text:<18}{item['description']}")
    print("-" * 65)


def show_city_weather(city, api_key):
    """Fetch and display current conditions and forecast."""
    current = get_current_weather(city, api_key)
    if current is None:
        return

    display_current_weather(current)

    forecast = get_forecast(city, api_key)
    if forecast is not None:
        display_forecast(forecast)


def main():
    """Run the city-search CLI until the user enters a blank city."""
    print("=" * 48)
    print("       WEATHER APP - OPENWEATHER API")
    print("=" * 48)
    print("Temperatures are displayed in Celsius (metric units).")
    api_key = load_api_key()
    if api_key is None:
        return

    while True:
        city = input("\nEnter a city name (blank to quit): ").strip()
        if not city:
            print("Goodbye!")
            break
        show_city_weather(city, api_key)


if __name__ == "__main__":
    main()
