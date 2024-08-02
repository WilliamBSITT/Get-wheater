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
        print(wheater_data)
    else:
        print(f"Error {result.status_code}")

    
if __name__ == "__main__":
    main()
