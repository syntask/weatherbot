import requests
import json

# fetch current weather for 55116 from open-meteo API

response = requests.get("https://api.open-meteo.com/v1/forecast", params={
    "latitude": 44.9833,
    "longitude": -93.2667,
    "wind_speed_unit": "mph",
    "temperature_unit": "fahrenheit",
    "current": "weather_code,temperature_2m,apparent_temperature,relative_humidity_2m,windspeed_10m,wind_gusts_10m,winddirection_10m",
})

data = response.json()
current_weather = data.get("current", {})

print(json.dumps(current_weather, indent=2))