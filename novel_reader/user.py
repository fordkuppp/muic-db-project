from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from novel_reader.db import get_db
from datetime import datetime
import bcrypt

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/register', methods=["POST"])
def register(): 
    db = get_db()
    cur = db.cursor()
    
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    email = request.form["email"]
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password1.encode("utf-8"), salt)
    print(hashed_password)
    if (password1 != password2):
        return "Passwords do not match!"
    
    add_user = ("INSERT INTO reader_db.user "
                 "(username, email, password, last_login, role_id) "
                 "VALUES (%s, %s, %s, %s, 1);")
    data_user = (username, email, hashed_password, time)
    
    cur.execute(add_user, data_user)
    db.commit()
    cur.close()
    
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