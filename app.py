from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://username:password@server/db"
db = SQLAlchemy()
db.init_app(app)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/user/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return "signup page"
    return redirect("home")


@app.route("/user/signup/", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        print(request.form)
        return "success"
    return redirect("home")


@app.route("/user/forget/", methods=["GET", "POST"])
def forget():
    if request.method == "POST":
        print(request.form)
        return "success"
    return redirect("home")


if __name__ == "__main__":
    app.run(debug=True)
