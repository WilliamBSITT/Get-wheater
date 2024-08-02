import requests
import os
from dotenv import load_dotenv


def convert_kelvin_to_celisus(kelvin):
    celsius = kelvin - 273.15
    return celsius

def convert_kelvin_to_fahrenheit(kelvin):
    fahrenheit = (kelvin - 273.15) * 9 / 5 + 32
    return fahrenheit

def main():
    load_dotenv()
    city = os.getenv("CITY")
    print(city)

    
if __name__ == "__main__":
    main()
