import requests
import os
from dotenv import load_dotenv

# For this projet I use the free api of openWeather
Base_URL = "https://api.openweathermap.org/data/2.5/weather?"

def convert_kelvin_to_celisus(kelvin):
    celsius = kelvin - 273.15
    return celsius

def convert_kelvin_to_fahrenheit(kelvin):
    fahrenheit = (kelvin - 273.15) * 9 / 5 + 32
    return fahrenheit

def display(data, city):
    temp_kelvin = data["main"]["temp"]
    temp_feel_kelvin = data["main"]["feels_like"]
    temp_fahrenheit = convert_kelvin_to_fahrenheit(temp_kelvin)
    temp_feel_fahrenheit = convert_kelvin_to_fahrenheit(temp_feel_kelvin)
    humdity = data["main"]["humidity"]
    meteo = data["weather"][0]["description"]
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
