This project retrieves and displays weather forecasts for a specified city using the free OpenWeather API. It shows the current weather conditions and the forecast for the 5 upcoming days.

Prerequisites :
  - Python 3.x: Ensure that Python 3.x is installed on your machine.
  - Python Libraries: You will need the following libraries:
      - requests
      - python-dotenv
  You can install these libraries using pip -> "pip install requests python-dotenv"
  - OpenWeather Account: Create an account on OpenWeather (https://openweathermap.org/) to obtain an API key.

Code Details :

  Main Functions :
  
    - convert_kelvin_to_celsius(kelvin): Converts a temperature from Kelvin to Celsius.
    - convert_celsius_to_fahrenheit(celsius): Converts a temperature from Celsius to Fahrenheit.
    - find_gps_localisation(city, api_key): Gets the GPS coordinates (latitude, longitude) and the country of a city.
    - get_current_weather(lat, lon, api_key): Gets the current weather conditions for a given GPS location.
    - get_forecast_data(lat, lon, api_key): Gets the weather forecast for a given GPS location.
    - parse_forecast_data(forecast_data): Parses and organizes the weather forecast data.
    - display_weather(daily_summary, current_weather, lang): Displays the current weather conditions and the forecast.

Weather Condition Translation :

  The meteo_translate dictionary is used to translate weather descriptions from English to French. But you can modify it in order to be in you native language you just need to put your transltaion in the meteo_translate & in display_weater change the condition to your country id

If you encounter errors while running the script:

  Ensure your .env file is correctly configured with a valid API key and an existing city.
  Check that your internet connection is working properly.
  Refer to the error messages for more details on specific issues.

Contributing : 

  Contributions are welcome! If you want to add features or fix bugs, please open an issue or submit a pull request.
