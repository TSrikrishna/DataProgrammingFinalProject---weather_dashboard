from flask import Flask, jsonify, render_template, request
import psycopg2
import os
from datetime import datetime

app = Flask(__name__)


def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password='Krishna@123',
            host='34.173.45.201',
            port='5432'
        )
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None


def get_weather_data(city=None, start_time=None, end_time=None):
    try:
        conn = get_db_connection()
        if not conn:
            return []

        c = conn.cursor()

        query = '''
            SELECT city, 
                   AVG(temperature) as avg_temp, 
                   AVG(humidity) as avg_humidity,
                   DATE_TRUNC('minute', timestamp) as minute
            FROM weather
            WHERE (%s IS NULL OR city = %s)
            AND (%s IS NULL OR timestamp >= %s)
            AND (%s IS NULL OR timestamp <= %s)
            GROUP BY city, minute
            ORDER BY minute DESC
        '''
        c.execute(query, (city, city, start_time, start_time, end_time, end_time))
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
        return weather_data
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/weather', methods=['GET'])
def api_weather():
    city = request.args.get('city')
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    weather_data = get_weather_data(city, start_time, end_time)
    return jsonify(weather_data)


@app.route('/api/weather/<int:id>', methods=['GET'])
def api_weather_by_id(id):
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500

        c = conn.cursor()
        c.execute('SELECT * FROM weather WHERE id = %s', (id,))
        row = c.fetchone()
        conn.close()

        if row:
            weather_data = {
                'id': row[0],
                'city': row[1],
                'temperature': row[2],
                'humidity': row[3],
                'description': row[4],
                'timestamp': row[5].isoformat()
            }
            return jsonify(weather_data)
        else:
            return jsonify({'error': 'Weather data not found'}), 404
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/api/weather/range', methods=['GET'])
def api_weather_range():
    start_time = request.args.get('start')
    end_time = request.args.get('end')

    if not start_time or not end_time:
        return jsonify({'error': 'Missing start or end time'}), 400

    try:
        start_time = datetime.fromisoformat(start_time)
        end_time = datetime.fromisoformat(end_time)
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400

    weather_data = get_weather_data(start_time=start_time, end_time=end_time)
    return jsonify(weather_data)


if __name__ == '__main__':
    app.run(debug=True)