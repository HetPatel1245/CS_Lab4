
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from pathlib import Path

app = Flask(__name__)

DATABASE = Path(__file__).with_name("comments.db")


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL
            )
        """)
        conn.commit()


@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":
        comment = request.form.get("comment", "").strip()

        if comment:
            with get_db_connection() as conn:
                conn.execute(
                    "INSERT INTO comments (content) VALUES (?)",
                    (comment,)
                )
                conn.commit()

        return redirect(url_for("index"))

    with get_db_connection() as conn:
        comments = conn.execute(
            "SELECT id, content FROM comments ORDER BY id DESC"
        ).fetchall()

    return render_template("index.html", comments=comments)


if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5000, debug=True)
