from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://username:password@server/db"
db = SQLAlchemy()
db.init_app(app)


@app.route("/")
def home():
    return render_template("starter/home.html")


@app.route("/user/login/", methods=["POST"])
def login():
    pass


@app.route("/user/signup/", methods=["POST"])
def signup():
    pass


@app.route("/user/forget/", methods=["POST"])
def forget():
    pass


@app.route("/user/new_pass/", methods=["POST"])
def new_pass():
    pass


@app.route("/latest/")
def latest():
    pass


if __name__ == "__main__":
    app.run(debug=True)
