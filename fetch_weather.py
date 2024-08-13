import requests

def fetch_weather_data(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch data")
        return None

if __name__ == '__main__':
    api_key = "0cd5195b0230bccd9770892c5e38c5d8"
    city = "London,uk"
    weather_data = fetch_weather_data(city, api_key)
    print(weather_data)
