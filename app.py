from flask import Flask, jsonify, render_template
import psycopg2
import os

app = Flask(__name__)

def get_weather_data():
    try:
        conn = psycopg2.connect(
            dbname=os.environ.get('PGDATABASE'),
            user=os.environ.get('PGUSER'),
            password=os.environ.get('PGPASSWORD'),
            host=os.environ.get('PGHOST')
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
        weather_data = [{'city': row[0], 'temperature': row[1], 'humidity': row[2], 'minute': row[3]} for row in rows]
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
    return jsonify(weather_data)

if __name__ == '__main__':
    app.run(debug=True)
