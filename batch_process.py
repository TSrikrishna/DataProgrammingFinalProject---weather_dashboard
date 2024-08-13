import schedule
import time
from fetch_weather import fetch_weather_data
from store_weather import store_weather_data

def batch_process():
    api_key = "0cd5195b0230bccd9770892c5e38c5d8"
    city = "London,uk"
    weather_data = fetch_weather_data(city, api_key)
    if weather_data:
        store_weather_data(weather_data)
    else:
        print("No data to store")

# Schedule the batch process to run every 24 hours
schedule.every(24).hours.do(batch_process)

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)
