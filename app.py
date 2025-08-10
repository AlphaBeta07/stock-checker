from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# --- DB Setup ---
def init_db():
    conn = sqlite3.connect("perfumes.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS perfumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# --- Routes ---
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get")
def get_perfumes():
    conn = sqlite3.connect("perfumes.db")
    c = conn.cursor()
    c.execute("SELECT * FROM perfumes")
    rows = c.fetchall()
    conn.close()

    perfumes = [
        {"id": r[0], "name": r[1], "category": r[2], "price": r[3], "quantity": r[4]}
        for r in rows
    ]
    return jsonify(perfumes)

@app.route("/add", methods=["POST"])
def add_perfume():
    data = request.get_json()
    conn = sqlite3.connect("perfumes.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO perfumes (name, category, price, quantity) VALUES (?, ?, ?, ?)",
        (data["name"], data["category"], float(data["price"]), int(data["quantity"]))
    )
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

@app.route("/update", methods=["POST"])
def update_perfume():
    data = request.get_json()
    conn = sqlite3.connect("perfumes.db")
    c = conn.cursor()
    c.execute(
        "UPDATE perfumes SET name=?, category=?, price=?, quantity=? WHERE id=?",
        (data["name"], data["category"], float(data["price"]), int(data["quantity"]), data["id"])
    )
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

@app.route("/delete", methods=["POST"])
def delete_perfume():
    data = request.get_json()
    conn = sqlite3.connect("perfumes.db")
    c = conn.cursor()
    c.execute("DELETE FROM perfumes WHERE id=?", (data["id"],))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

@app.route("/total")
def total_stock():
    conn = sqlite3.connect("perfumes.db")
    c = conn.cursor()
    c.execute("SELECT SUM(price * quantity) FROM perfumes")
    total = c.fetchone()[0] or 0
    conn.close()
    return jsonify({"total": total})

if __name__ == "__main__":
    app.run(debug=True)
