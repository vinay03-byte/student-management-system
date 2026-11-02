from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path

app = Flask(__name__)
app.secret_key = "change-this-secret-key"
DATABASE = Path(__file__).with_name("students.db")


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with get_db_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                course TEXT NOT NULL,
                phone TEXT NOT NULL
            )
        """)


@app.route("/")
def index():
    with get_db_connection() as connection:
        students = connection.execute(
            "SELECT * FROM students ORDER BY id DESC"
        ).fetchall()
    return render_template("index.html", students=students)


@app.route("/add", methods=["POST"])
def add_student():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    course = request.form.get("course", "").strip()
    phone = request.form.get("phone", "").strip()

    if not all([name, email, course, phone]):
        flash("Please fill in all fields.", "error")
        return redirect(url_for("index"))

    try:
        with get_db_connection() as connection:
            connection.execute(
                "INSERT INTO students (name, email, course, phone) VALUES (?, ?, ?, ?)",
                (name, email, course, phone)
            )
        flash("Student added successfully!", "success")
    except sqlite3.IntegrityError:
        flash("That email address is already registered.", "error")

    return redirect(url_for("index"))


@app.route("/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    with get_db_connection() as connection:
        connection.execute("DELETE FROM students WHERE id = ?", (student_id,))
    flash("Student deleted.", "success")
    return redirect(url_for("index"))


@app.route("/edit/<int:student_id>", methods=["GET", "POST"])
def edit_student(student_id):
    with get_db_connection() as connection:
        student = connection.execute(
            "SELECT * FROM students WHERE id = ?", (student_id,)
        ).fetchone()

        if student is None:
            flash("Student not found.", "error")
            return redirect(url_for("index"))

        if request.method == "POST":
            name = request.form.get("name", "").strip()
            email = request.form.get("email", "").strip()
            course = request.form.get("course", "").strip()
            phone = request.form.get("phone", "").strip()

            if not all([name, email, course, phone]):
                flash("Please fill in all fields.", "error")
                return redirect(url_for("edit_student", student_id=student_id))

            try:
                connection.execute(
                    """UPDATE students
                       SET name = ?, email = ?, course = ?, phone = ?
                       WHERE id = ?""",
                    (name, email, course, phone, student_id)
                )
                flash("Student updated successfully!", "success")
                return redirect(url_for("index"))
            except sqlite3.IntegrityError:
                flash("That email address is already used by another student.", "error")

    return render_template("edit.html", student=student)


if __name__ == "__main__":
    initialize_database()
    app.run(debug=True)
