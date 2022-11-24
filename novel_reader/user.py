from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from novel_reader.db import get_db
from datetime import datetime
import bcrypt

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/register', methods=["POST"])
def register():   
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    email = request.form["email"]
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password1.encode("utf-8"), salt)
    
    statement = f"INSERT INTO reader_db.user (username, email, password, last_login, role_id) VALUES ('{username}', '{email}', '{hashed_password}', '{time}', 1);"

    db = get_db()
    cur = db.cursor()
    cur.execute(statement)
    db.commit()
    
    
    return redirect("/")

@bp.route("/user/login/", methods=["POST"])
def login():
    pass

@bp.route("/user/forget/", methods=["POST"])
def forget():
    pass


@bp.route("/user/forget/<string:token>", methods=["POST"])
def new_pass(token: str):
    pass