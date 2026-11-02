
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
from datetime import date

app = Flask(__name__)

# Database stored in the data folder
DB_PATH = "/app/data/expenses.db"


def get_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            expense_date TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


@app.route("/")
def index():
    conn = get_db()

    expenses = conn.execute("""
        SELECT * FROM expenses
        ORDER BY expense_date DESC, id DESC
    """).fetchall()

    total = conn.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM expenses"
    ).fetchone()[0]

    today_total = conn.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM expenses "
        "WHERE expense_date = ?",
        (date.today().isoformat(),)
    ).fetchone()[0]

    categories = conn.execute("""
        SELECT category, SUM(amount) AS total
        FROM expenses
        GROUP BY category
        ORDER BY total DESC
    """).fetchall()

    conn.close()

    return render_template(
        "index.html",
        expenses=expenses,
        total=total,
        today_total=today_total,
        categories=categories,
        today=date.today().isoformat()
    )


@app.route("/add", methods=["POST"])
def add_expense():
    title = request.form.get("title", "").strip()
    category = request.form.get("category", "").strip()
    expense_date = request.form.get("expense_date", "")
    amount_text = request.form.get("amount", "")

    allowed_categories = {
        "Food", "Travel", "Shopping", "Bills",
        "Education", "Health", "Other"
    }

    try:
        amount = float(amount_text)
    except (ValueError, TypeError):
        return "Invalid amount", 400

    try:
        parsed_date = date.fromisoformat(expense_date)
    except (ValueError, TypeError):
        return "Invalid date", 400

    if (
        not title or len(title) > 100
        or amount <= 0 or amount > 100000000
        or category not in allowed_categories
        or parsed_date > date.today()
    ):
        return "Please enter valid expense details.", 400

    conn = get_db()
    conn.execute("""
        INSERT INTO expenses
        (title, amount, category, expense_date)
        VALUES (?, ?, ?, ?)
    """, (title, amount, category, expense_date))
    conn.commit()
    conn.close()

    return redirect(url_for("index"))


@app.route("/delete/<int:expense_id>", methods=["POST"])
def delete_expense(expense_id):
    conn = get_db()
    conn.execute(
        "DELETE FROM expenses WHERE id = ?",
        (expense_id,)
    )
    conn.commit()
    conn.close()

    return redirect(url_for("index"))


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
