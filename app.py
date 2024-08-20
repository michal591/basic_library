from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Secret key for session management


# Function to get the list of books from the database
def get_books():
    conn = sqlite3.connect("library.db")
    conn.row_factory = sqlite3.Row  # This makes rows behave like dictionaries
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Books")
    books = cursor.fetchall()
    conn.close()
    return books


# Function to verify user credentials
def verify_user(email, password):
    conn = sqlite3.connect("library.db")
    conn.row_factory = sqlite3.Row  # Ensure dictionary-like row access
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM Users WHERE Email = ? AND Password = ?", (email, password)
    )
    user = cursor.fetchone()
    conn.close()
    return user


@app.route("/")
def book_list():
    if "user_id" in session:
        books = get_books()
        return render_template("books.html", books=books)
    else:
        return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = verify_user(email, password)

        if user:
            session["user_id"] = user["UserID"]  # Safely access the UserID
            session["user_name"] = user["Name"]  # Safely access the Name
            return redirect(url_for("book_list"))
        else:
            flash("Invalid email or password. Please try again.", "danger")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("user_name", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
