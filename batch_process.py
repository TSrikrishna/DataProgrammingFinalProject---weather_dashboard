import schedule
import time
from fetch_weather import fetch_weather_data
from store_weather import store_weather_data

def batch_process():
    api_key = "0cd5195b0230bccd9770892c5e38c5d8"
    cities = ["Barrie,ca", "Toronto,ca"]  # List of cities to fetch weather data for
    for city in cities:
        print(f"Fetching weather data for {city}")
        weather_data = fetch_weather_data(city, api_key)
        if weather_data:
            simplified_data = {
                "name": weather_data["name"],
                "main": {
                    "temp": weather_data["main"]["temp"],
                    "humidity": weather_data["main"]["humidity"]
                },
                "weather": [
                    {
                        "description": weather_data["weather"][0]["description"]
                    }
                ]
            }
            print(f"Storing weather data for {city}")
            store_weather_data(simplified_data)
        else:
            print(f"No data to store for {city}")

# Schedule the batch process to run every minute
schedule.every(1).minutes.do(batch_process)

# Keep the script running
if __name__ == '__main__':
    print("Running initial batch process")
    batch_process()  # Run batch process initially
    print("Initial batch process complete, entering scheduling mode")
    while True:
        schedule.run_pending()
        time.sleep(1)
