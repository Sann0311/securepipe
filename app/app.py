from flask import Flask, request, jsonify
import sqlite3
import subprocess
import os

app = Flask(__name__)

# !! INTENTIONAL VULNERABILITY 1: Hardcoded secret (Bandit will catch this)
SECRET_KEY = "hardcoded_super_secret_123"
DB_PATH = "/app/data/users.db"
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, email TEXT)")
    c.execute("INSERT OR IGNORE INTO users VALUES (1, 'alice', 'alice@example.com')")
    c.execute("INSERT OR IGNORE INTO users VALUES (2, 'bob', 'bob@example.com')")
    conn.commit()
    conn.close()


@app.route("/")
def index():
    return jsonify({"message": "Welcome to SecurePipe demo app", "status": "running"})


@app.route("/health")
def health():
    return jsonify({"status": "healthy"})


# !! INTENTIONAL VULNERABILITY 2: SQL Injection (Bandit + ZAP will catch this)
@app.route("/user")
def get_user():
    username = request.args.get("username", "")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Vulnerable: direct string formatting in SQL query
    query = f"SELECT * FROM users WHERE username = '{username}'"
    c.execute(query)
    result = c.fetchall()
    conn.close()
    return jsonify({"users": result})


# !! INTENTIONAL VULNERABILITY 3: Command injection (Bandit will catch this)
@app.route("/ping")
def ping():
    host = request.args.get("host", "localhost")
    # Vulnerable: shell=True with user input
    result = subprocess.run(f"ping -c 1 {host}", shell=True, capture_output=True, text=True)
    return jsonify({"output": result.stdout})


# Safe endpoint — shows contrast
@app.route("/users")
def list_users():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Safe: parameterized query
    c.execute("SELECT id, username FROM users")
    result = c.fetchall()
    conn.close()
    return jsonify({"users": [{"id": r[0], "username": r[1]} for r in result]})


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
