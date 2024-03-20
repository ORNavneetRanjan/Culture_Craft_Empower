from flask import Flask, render_template, request
from flask import redirect, url_for, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "Navneet@123"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.sqlite3'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=5)

# db = SQLAlchemy(app)
#
#
# class users(db.Model):
#     _id = db.Column("id", db.Integer, primary_key=True)
#     name = db.Column(db.String(100))
#     email = db.Column(db.String(100))
#
#     def __init__(self, name, email):
#         self.name = name
#         self.email = email


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        y_name = request.form["nm"]
        session["y_name"] = y_name
        flash("Login Successful !")
        return redirect(url_for("user"))
    else:
        if "y_name" in session:
            flash("Already Logged IN")
            return redirect(url_for("user"))
        return render_template("login.html")


@app.route("/user", methods=["POST", "GET"])
def user():
    email = None
    if "y_name" in session:
        y_name = session["y_name"]
        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            flash(f"{email} is saved")
        else:
            if "email" in session:
                email = session["email"]
        return render_template("user.html", user=email)
    else:
        flash("You are not logged in")
        return render_template("user.html")


@app.route("/logout")
def logout():
    session.pop("y_name", None)
    session.pop("email", None)
    flash("You have been logged out!", "info")
    return redirect(url_for("login"))


if __name__ == "__main__":
    # db.create_all()
    app.run(debug=True)
