import requests
import json
import datetime

# fetch current weather for 55116 from open-meteo API

response = requests.get("https://api.open-meteo.com/v1/forecast", params={
    "latitude": 44.9833,
    "longitude": -93.2667,
    "wind_speed_unit": "mph",
    "temperature_unit": "fahrenheit",
    "current": "weather_code,temperature_2m,apparent_temperature,relative_humidity_2m,windspeed_10m,wind_gusts_10m,winddirection_10m",
    "daily": "sunrise,sunset",
    "timezone": datetime.datetime.now().astimezone().tzinfo,
    "forecast_days": 1
})

data = response.json()
current_weather = data.get("current", {})

print(json.dumps(data, indent=2))

if datetime.datetime.fromisoformat(data["daily"]["sunrise"][0]).astimezone() < datetime.datetime.now().astimezone() < datetime.datetime.fromisoformat(data["daily"]["sunset"][0]).astimezone():
    print("It's currently daytime.")
else:
    print("It's currently nighttime.")