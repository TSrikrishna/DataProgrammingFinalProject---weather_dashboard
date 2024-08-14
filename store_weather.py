import psycopg2

def store_weather_data(weather_data):
    try:
        conn = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password='Krishna@123',
            host='34.173.45.201',
            port='5432'
        )
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS weather (
                id SERIAL PRIMARY KEY,
                city TEXT,
                temperature REAL,
                humidity INTEGER,
                description TEXT,
                timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        c.execute('''
            INSERT INTO weather (city, temperature, humidity, description) VALUES (%s, %s, %s, %s)
        ''', (
            weather_data['name'],
            weather_data['main']['temp'],
            weather_data['main']['humidity'],
            weather_data['weather'][0]['description']
        ))
        conn.commit()
        conn.close()
        print("Weather data stored successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

#if __name__ == '__main__':
#    from fetch_weather import fetch_weather_data
#    api_key = "0cd5195b0230bccd9770892c5e38c5d8"
#    cities = ["Barrie,ca"]
#    for city in cities:
#        weather_data = fetch_weather_data(city, api_key)
#        if weather_data:
#            store_weather_data(weather_data)
