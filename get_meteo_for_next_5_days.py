import requests
import os
from datetime import datetime
from dotenv import load_dotenv

# For this project I use the free API of OpenWeather
geocoding_url_base = "https://api.openweathermap.org/geo/1.0/direct?"
forecast_url_base = "https://api.openweathermap.org/data/2.5/forecast?"
current_weather_url_base = "https://api.openweathermap.org/data/2.5/weather?"
meteo_translate = {
    "broken clouds": "éclaircies",
    "clear sky": "ensoleillé",
    "scattered clouds": "Ciel couvert",
    "snow": "Chute de neige",
    "overcast clouds": "Nuageux",
    "moderate rain": "Pluie modéré",
    "light rain": "Pluie légère"
}
lang = "US"

def convert_kelvin_to_celsius(kelvin):
    return kelvin - 273.15

def convert_celsius_to_fahrenheit(celsius):
    return (celsius * 9 / 5) + 32

def find_gps_localisation(city, api_key):
    geocoding_url = f"{geocoding_url_base}q={city}&limit=1&appid={api_key}"
    loc_geo = requests.get(geocoding_url)
    if loc_geo.status_code == 200:
        geodata = loc_geo.json()
        if not geodata:
            print(f"Erreur, la ville de {city} est introuvable.")
            exit(84)
        lat = geodata[0]["lat"]
        lon = geodata[0]["lon"]
        return lat, lon
    
    print(f"Error {loc_geo.status_code} while retrieving the city's coordinates.")
    print(f"Response: {loc_geo.text}")
    exit(84)

def get_current_weather(lat, lon, api_key):
    current_weather_url = f"{current_weather_url_base}lat={lat}&lon={lon}&appid={api_key}"
    result_current_weather = requests.get(current_weather_url)

    if result_current_weather.status_code == 200:
        weather_data = result_current_weather.json()
        temp = convert_kelvin_to_celsius(weather_data["main"]["temp"])
        feels_like = convert_kelvin_to_celsius(weather_data["main"]["feels_like"])
        humidity = weather_data["main"]["humidity"]
        wind_speed = weather_data["wind"]["speed"] * 3.6  # Convert m/s to km/h
        weather_desc = weather_data["weather"][0]["description"]
        lang = weather_data["sys"]["country"]
        
        return {
            "temp": temp,
            "feels_like": feels_like,
            "humidity": humidity,
            "wind_speed": wind_speed,
            "weather_desc": weather_desc
        }
    else:
        print(f"Error {result_current_weather.status_code} while retrieving the current weather.")
        print(f"Response: {result_current_weather.text}")
        exit(84)

def get_forecast_data(lat, lon, api_key):
    forecast_url = f"{forecast_url_base}lat={lat}&lon={lon}&appid={api_key}"
    result_forecast = requests.get(forecast_url)

    if result_forecast.status_code == 200:
        return result_forecast.json()
    else:
        print(f"Error {result_forecast.status_code} while retrieving the weather forecast.")
        print(f"Response: {result_forecast.text}")
        exit(84)

def main():
    load_dotenv()
    city = os.getenv("CITY")
    api_key = os.getenv("API_KEY")
    
    if city is None or api_key is None:
        print("Error, it seems there was an issue accessing data from dotenv.")
        exit(84)
    
    lat, lon = find_gps_localisation(city, api_key)
    current_weather = get_current_weather(lat, lon, api_key)
    forecast_data = get_forecast_data(lat, lon, api_key)

if __name__ == "__main__":
    main()
