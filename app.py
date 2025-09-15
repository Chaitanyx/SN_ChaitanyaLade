from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import secrets
from datetime import datetime, timedelta

app = Flask(__name__)
DATABASE = 'cloud.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    username = data['username']
    password = generate_password_hash(data['password'])
    role = data['role']
    email = data.get('email', '')

    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO users (username, password_hash, role, email) VALUES (?, ?, ?, ?)',
                   (username, password, role, email))
    db.commit()
    return jsonify({"status": "user added"}), 201

@app.route('/create_session', methods=['POST'])
def create_session():
    data = request.json
    username = data['username']
    password = data['password']

    db = get_db()
    cursor = db.cursor()
    user = cursor.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

    if user and check_password_hash(user['password_hash'], password):
        token = secrets.token_hex(16)
        expires_at = datetime.utcnow() + timedelta(hours=1)
        cursor.execute('INSERT INTO sessions (user_id, token, expires_at) VALUES (?, ?, ?)',
                       (user['id'], token, expires_at))
        db.commit()
        return jsonify({"token": token, "expires_at": str(expires_at)})
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/add_policy', methods=['POST'])
def add_policy():
    data = request.json
    user_id = data['user_id']
    folder_path = data['folder_path']
    permissions = data['permissions']
    valid_until = datetime.strptime(data['valid_until'], '%Y-%m-%dT%H:%M:%S')

    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO access_policies (user_id, folder_path, permissions, valid_until) VALUES (?, ?, ?, ?)',
                   (user_id, folder_path, permissions, valid_until))
    db.commit()
    return jsonify({"status": "policy added"}), 201

if __name__ == '__main__':
    app.run(debug=True)
