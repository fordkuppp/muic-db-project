from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://username:password@server/db"
db = SQLAlchemy()
db.init_app(app)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/user/login", methods=["GET", "POST"])
def login():
    return "LOGIN PAGE"


@app.route("/user/signup", methods=["GET", "POST"])
def signup():
    return "SIGNUP PAGE"


if __name__ == "__main__":
    app.run(debug=True)
