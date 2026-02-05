import requests

# fetch current METAR for KMSP
icao_code = "KMSP"
response = requests.get(f"https://aviationweather.gov/api/data/metar?ids={icao_code}&hours=0&sep=true")

if response.status_code == 200:
    metar_data = response.text
    print("Current METAR data:")
    print(metar_data)
else:
    print(f"Failed to retrieve METAR data. Status code: {response.status_code}")