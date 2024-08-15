from flask import Flask, jsonify, render_template
import psycopg2
import os
from datetime import datetime

app = Flask(__name__)

def get_weather_data():
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
            SELECT city, 
                   AVG(temperature) as avg_temp, 
                   AVG(humidity) as avg_humidity,
                   DATE_TRUNC('minute', timestamp) as minute
            FROM weather
            GROUP BY city, minute
            ORDER BY minute DESC
        ''')
        rows = c.fetchall()
        conn.close()
        
        weather_data = []
        for row in rows:
            weather_data.append({
                'city': row[0],
                'temperature': row[1],
                'humidity': row[2],
                'minute': row[3].isoformat() if isinstance(row[3], datetime) else row[3]
            })
        print(f"Fetched weather data: {weather_data}")
        return weather_data
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/weather', methods=['GET'])
def api_weather():
    weather_data = get_weather_data()
    print(f"API Weather Data: {weather_data}")
    return jsonify(weather_data)

if __name__ == '__main__':
    app.run(debug=True)
