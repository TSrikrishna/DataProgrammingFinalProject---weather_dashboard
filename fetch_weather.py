import requests

def fetch_weather_data(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data for {city}: {response.status_code}")
        return None

if __name__ == '__main__':
    api_key = "0cd5195b0230bccd9770892c5e38c5d8"
    cities = ["Barrie,ca", "Toronto,ca"]
    for city in cities:
        weather_data = fetch_weather_data(city, api_key)
        print(weather_data)
