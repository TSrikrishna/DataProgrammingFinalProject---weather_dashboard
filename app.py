from flask import Flask, jsonify, render_template
import psycopg2

app = Flask(__name__)

# Database connection details
host = '34.173.45.201'
dbname = 'postgres'
user = 'postgres'
password = 'Krishna@123'
port = '5432'

def get_weather_data():
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    c = conn.cursor()
    c.execute('SELECT * FROM weather')
    data = c.fetchall()
    conn.close()
    return data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/weather', methods=['GET'])
def api_weather():
    data = get_weather_data()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
