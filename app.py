import os
import requests
import psycopg2
from flask import Flask, request, jsonify
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        database=os.environ.get("DB_NAME", "animedb"),
        user=os.environ.get("DB_USER", "animeuser"),
        password=os.environ.get("DB_PASSWORD", "animepass")
    )
    return conn

@app.route('/')
def home():
    return 'Anime Lounge Service'

@app.route('/random-anime-quote', methods=['GET'])
def random_anime_quote():
    url = 'https://animechan.vercel.app/api/random'
    response = requests.get(url)
    data = response.json()
    return jsonify({'anime': data.get('anime'), 'character': data.get('character'), 'quote': data.get('quote')})

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    hashed_password = generate_password_hash(data['password'])
    cur.execute('INSERT INTO users (username, email, password) VALUES (%s, %s, %s) RETURNING id', (data['username'], data['email'], hashed_password))
    user_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'user_id': user_id})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, password FROM users WHERE email=%s', (data['email'],))
    user = cur.fetchone()
    if user and check_password_hash(user[1], data['password']):
        return jsonify({'user_id': user[0], 'status': 'authorized'})
    return jsonify({'status': 'unauthorized'}), 401

@app.route('/reviews', methods=['POST'])
def create_review():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO reviews (user_id, anime_title, review_text, rating, created_at) VALUES (%s, %s, %s, %s, %s) RETURNING id',
                (data['user_id'], data['anime_title'], data['review_text'], data['rating'], datetime.utcnow()))
    review_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'review_id': review_id})

@app.route('/reviews/<int:user_id>', methods=['GET'])
def user_reviews(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, anime_title, review_text, rating, created_at FROM reviews WHERE user_id=%s ORDER BY created_at DESC', (user_id,))
    rows = cur.fetchall()
    data = []
    for row in rows:
        data.append({'review_id': row[0], 'anime_title': row[1], 'review_text': row[2], 'rating': row[3], 'created_at': row[4].isoformat()})
    cur.close()
    conn.close()
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
