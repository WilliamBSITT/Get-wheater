import requests
import os
from dotenv import load_dotenv

# For this projet I use the free api of openWeather
Base_URL = "https://api.openweathermap.org/data/2.5/weather?"
meteo_type = {
                "broken clouds": "éclaircies", 
                "clear sky": "ensoleillé", 
                "scattered clouds": "Ciel couvert", 
                "snow": "Chute de neige", 
                "overcast clouds": "Nuageux", 
                "moderate rain" : "Pluie modéré", 
                "light rain" : "Pluie légère"
            }

def convert_kelvin_to_celisus(kelvin):
    celsius = kelvin - 273.15
    return celsius

def convert_kelvin_to_fahrenheit(kelvin):
    fahrenheit = (kelvin - 273.15) * 9 / 5 + 32
    return fahrenheit

def display(data, city):
    temp_kelvin = data["main"]["temp"]
    temp_feel_kelvin = data["main"]["feels_like"]
    humdity = data["main"]["humidity"]
    meteo = data["weather"][0]["description"]
    if data["sys"]["country"] == "FR":
        for i, j in meteo_type.items():
            if i == meteo:
                translate_weather = j
        temp_celsius = convert_kelvin_to_celisus(temp_kelvin)
        temp_feel_celsius = convert_kelvin_to_celisus(temp_feel_kelvin)
        print(f"La météo actuelle à {city} est de :\nAvec un température de {temp_celsius:.2f}°C avec un ressentie de {temp_feel_celsius}.")
        print(f"L'humidité est d'environ {humdity}% et la météo est {translate_weather}.")
    else :
        temp_fahrenheit = convert_kelvin_to_fahrenheit(temp_kelvin)
        temp_feel_fahrenheit = convert_kelvin_to_fahrenheit(temp_feel_kelvin)
        print(f"The current weather in {city} is :\nA temperature of {temp_fahrenheit:.2f}°F with a fell of {temp_feel_fahrenheit:.2f}.")
        print(f"The humidity is about {humdity}% and the wheater is {meteo}.")

def main():
    load_dotenv()
    city = os.getenv("CITY")
    api_key = os.getenv("API_KEY")
    if city == None or api_key == None:
        print(f"Error, it seems there is an error when accessing the data from dotenv.")
    url = Base_URL + "appid=" + str(api_key) + "&q=" + str(city)
    result = requests.get(url)
    if result.status_code == 200:
        wheater_data = result.json()
        display(wheater_data, city)
    else:
        print(f"Error {result.status_code}")

    
if __name__ == "__main__":
    main()
