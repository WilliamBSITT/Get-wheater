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
        lang = geodata[0]["country"]
        return lat, lon, lang
    
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

def parse_forecast_data(forecast_data):
    daily_summary = {}
    today = datetime.today().strftime("%d-%m-%Y")
    
    for entry in forecast_data["list"]:
        date = datetime.fromtimestamp(entry["dt"]).strftime("%d-%m-%Y")
        if date == today:
            continue
        
        temp_min = convert_kelvin_to_celsius(entry["main"]["temp_min"])
        temp_max = convert_kelvin_to_celsius(entry["main"]["temp_max"])
        feels_like = convert_kelvin_to_celsius(entry["main"]["feels_like"])
        humidity = entry["main"]["humidity"]
        wind_speed = entry["wind"]["speed"]
        weather_desc = entry["weather"][0]["description"]

        if date not in daily_summary:
            daily_summary[date] = {
                "temp_min": temp_min,
                "temp_max": temp_max,
                "feels_like_sum": feels_like,
                "wind_speed_sum": wind_speed,
                "weather_desc_sum": [weather_desc],
                "humidity": humidity,
                "count": 1
            }
        else:
            daily_summary[date]["temp_min"] = min(daily_summary[date]["temp_min"], temp_min)
            daily_summary[date]["temp_max"] = max(daily_summary[date]["temp_max"], temp_max)
            daily_summary[date]["feels_like_sum"] += feels_like
            daily_summary[date]["wind_speed_sum"] += wind_speed
            daily_summary[date]["weather_desc_sum"].append(weather_desc)
            daily_summary[date]["humidity"] += humidity
            daily_summary[date]["count"] += 1

    return daily_summary

def display_weather(daily_summary, current_weather, lang):
    if lang == "FR":
        print(f"Météo en direct:\nTempérature: {current_weather['temp']:.2f}°C\nTempérature ressentie: {current_weather['feels_like']:.2f}°C")
        print(f"Humidité: {current_weather['humidity']:.2f}%\nVitesse du vent: {current_weather['wind_speed']:.2f} Km/h")
        try:
            print(f"Météo: {meteo_translate[current_weather['weather_desc']]}")
        except KeyError:
            print(f"Erreur: {current_weather['weather_desc']} n'a pas de traduction")
            print(f"Météo: {current_weather['weather_desc']}")
        print("-------------\n\n")

        for date, summary in daily_summary.items():
            avg_feels_like = summary["feels_like_sum"] / summary["count"]
            avg_wind_speed = (summary["wind_speed_sum"] / summary["count"]) * 3.6
            avg_weather_desc = max(set(summary["weather_desc_sum"]), key=summary["weather_desc_sum"].count)
            humidity = summary["humidity"] / summary["count"]
            print(f"Date: {date}\nTempérature minimale: {summary['temp_min']:.2f}°C\nTempérature maximale: {summary['temp_max']:.2f}°C")
            print(f"Température ressentie moyenne: {avg_feels_like:.2f}°C\nVitesse du vent moyenne: {avg_wind_speed:.2f} Km/h\nHumidité: {humidity:.2f} %")
            try:
                print(f"Météo: {meteo_translate[avg_weather_desc]}")
            except KeyError:
                print(f"Erreur: {avg_weather_desc} n'a pas de traduction")
                print(f"Météo: {avg_weather_desc}")
            print("-------------")
    else:
        print(f"Current weather:\nTemperature: {current_weather['temp']:.2f}°F\nFeels like: {current_weather['feels_like']:.2f}°F\nHumidity: {current_weather['humidity']:.2f}%")
        print(f"Wind speed: {current_weather['wind_speed']:.2f} mph\nWeather: {current_weather['weather_desc']}")
        print("-------------\n\n")
        
        for date, summary in daily_summary.items():
            min_temp = convert_celsius_to_fahrenheit(summary['temp_min'])
            max_temp = convert_celsius_to_fahrenheit(summary['temp_max'])
            avg_feels_like = convert_celsius_to_fahrenheit(summary['feels_like_sum'] / summary['count'])
            avg_wind_speed = summary['wind_speed_sum'] * 2.237 / summary['count']
            avg_weather_desc = max(set(summary["weather_desc_sum"]), key=summary["weather_desc_sum"].count)
            humidity = summary['humidity'] / summary['count']

            print(f"Date: {date}\nMinimal temperature: {min_temp:.2f}°F\nMaximal temperature: {max_temp:.2f}°F\nAverage feels like temperature: {avg_feels_like:.2f}°F")
            print(f"Average wind speed: {avg_wind_speed:.2f} mph\nAverage humidity: {humidity:.2f} %\nWeather: {avg_weather_desc}")
            print("-------------")

def main():
    load_dotenv()
    city = os.getenv("CITY")
    api_key = os.getenv("API_KEY")
    
    if city is None or api_key is None:
        print("Error, it seems there was an issue accessing data from dotenv.")
        exit(84)
    
    lat, lon, lang = find_gps_localisation(city, api_key)
    current_weather = get_current_weather(lat, lon, api_key)
    forecast_data = get_forecast_data(lat, lon, api_key)
    daily_summary = parse_forecast_data(forecast_data)
    display_weather(daily_summary, current_weather, lang)

if __name__ == "__main__":
    main()
