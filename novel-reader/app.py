from typing import Any
from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
import yaml
import mysql.connector
from sqlalchemy import text

app = Flask(__name__)

@app.route("/")
def home():
    # This is sample data for showing template
    popular: list[dict[str, str]] = []
    latest: list = []
    for _ in range(18):
        popular.append(
            {
                "name": "Novel Name",
                "image": "/static/cover-default.png",
                "get_absolute_url": "/novel-slug/",
                "alt": "alt",
                "latest_chap": "chapter X",
            }
        )

    for _ in range(30):
        latest.append({
            "name": "Best Novel",
            "image": "/static/cover-default.png",
            "get_absolute_url": "/novel/novel-slug/",
            "alt": "alt",
            "chapters": [
                {"name": "chapter XX", "get_absolute_url": "/chapter/slug/", "get_date": "2 hours ago"}, 
                {"name": "chapter XX", "get_absolute_url": "/chapter/slug/", "get_date": "2 hours ago"}
                ]
            })
    return render_template("starter/home.html", popular=popular, latest=latest)


@app.route("/user/login/", methods=["POST"])
def login():
    pass


@app.route("/user/signup/", methods=["POST"])
def signup():
    data = request.form.get('email')
    app.logger.info(data)
    return data
    pass


@app.route("/user/forget/", methods=["POST"])
def forget():
    pass


@app.route("/user/forget/<string:token>", methods=["POST"])
def new_pass(token: str):
    pass


@app.route("/latest/")
def latest():
    pass


@app.route("/popular/")
def popular():
    pass


@app.route("/status/on_going/")
def on_going():
    pass


@app.route("/status/complete/")
def completed():
    pass


@app.route("/status/hiatus/")
def hiatus():
    pass


@app.route("/dbtest")
def dbtest():
    # statement = f"INSERT INTO reader_db.user (username, email, password, last_login, role_id) VALUES ('fesfsefe', 'test', 'test', '2022-11-24 21:52:50', 2);"
    statement = f"SELECT * FROM user;"

    db = get_db()
    cur = db.cursor()
    cur.execute(statement)
    result = cur.fetchall()
    print(str(result))
    db.commit()

    return str(result)

def get_db():
    cred = yaml.load(open('cred.yaml'), Loader=yaml.Loader)  
    db = mysql.connector.connect(
        host=cred["mysql_host"],
        user=cred["mysql_user"],
        password=cred["mysql_password"],
        database=cred["mysql_db"]
    )
    return db

if __name__ == "__main__":
    app.run(debug=True)
