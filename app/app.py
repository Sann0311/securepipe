from flask import Flask, request, jsonify
import sqlite3
import subprocess
import os

app = Flask(__name__)

# FIX 1: No hardcoded secret — read from environment variable
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-default")
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


# FIX 2: Parameterized query prevents SQL injection
@app.route("/user")
def get_user():
    username = request.args.get("username", "")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Safe: parameterized query with ? placeholder
    query = "SELECT * FROM users WHERE username = ?"
    c.execute(query, (username,))
    result = c.fetchall()
    conn.close()
    return jsonify({"users": result})


# FIX 3: Remove shell=True, use list args to prevent command injection
@app.route("/ping")
def ping():
    host = request.args.get("host", "localhost")
    # Safe: list args, no shell interpolation
    result = subprocess.run(
        ["ping", "-c", "1", host],
        capture_output=True,
        text=True,
        timeout=5
    )
    return jsonify({"output": result.stdout})


# Safe endpoint — parameterized query
@app.route("/users")
def list_users():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, username FROM users")
    result = c.fetchall()
    conn.close()
    return jsonify({"users": [{"id": r[0], "username": r[1]} for r in result]})


if __name__ == "__main__":
    init_db()
    # FIX 4: debug=False in production
    app.run(host="0.0.0.0", port=5000, debug=False)