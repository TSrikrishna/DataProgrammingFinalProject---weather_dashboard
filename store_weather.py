import psycopg2

def store_weather_data(weather_data):
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
            description TEXT
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

if __name__ == '__main__':
    weather_data = {
        "name": "London",
        "main": {
            "temp": 291.11,
            "humidity": 72
        },
        "weather": [
            {
                "description": "clear sky"
            }
        ]
    }
    store_weather_data(weather_data)
