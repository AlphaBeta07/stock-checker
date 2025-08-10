from flask import Flask, render_template, request, jsonify
import os
import psycopg2
from urllib.parse import urlparse

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

# Initialize table if not exists
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS perfumes (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

init_db()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get")
def get_perfumes():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, category, price, quantity FROM perfumes")
    data = [
        {"id": row[0], "name": row[1], "category": row[2], "price": row[3], "quantity": row[4]}
        for row in cur.fetchall()
    ]
    cur.close()
    conn.close()
    return jsonify(data)

@app.route("/add", methods=["POST"])
def add_perfume():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO perfumes (name, category, price, quantity) VALUES (%s, %s, %s, %s)",
                (data["name"], data["category"], data["price"], data["quantity"]))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"status": "success"})

@app.route("/update", methods=["POST"])
def update_perfume():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""UPDATE perfumes 
                   SET name = %s, category = %s, price = %s, quantity = %s 
                   WHERE id = %s""",
                (data["name"], data["category"], data["price"], data["quantity"], data["id"]))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"status": "success"})

@app.route("/delete", methods=["POST"])
def delete_perfume():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM perfumes WHERE id = %s", (data["id"],))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"status": "success"})

@app.route("/total")
def total_value():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT SUM(price * quantity) FROM perfumes")
    total = cur.fetchone()[0] or 0
    cur.close()
    conn.close()
    return jsonify({"total": total})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
