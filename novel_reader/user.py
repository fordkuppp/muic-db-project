from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from novel_reader.db import get_db
from datetime import datetime
from mysql.connector import IntegrityError
import bcrypt

bp = Blueprint("user", __name__, url_prefix="/user")

@bp.route("/register", methods=["POST"])
def register():
    try:
        db = get_db()
        cur = db.cursor()

        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        email = request.form["email"]
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password1.encode("utf-8"), salt)

        if password1 != password2:
            return "Passwords do not match!"

        add_user = (
            "INSERT INTO reader_db.user "
            "(username, email, password, last_login, role_id) "
            "VALUES (%s, %s, %s, %s, 1);"
        )
        data_user = (username, email, hashed_password, time)

        cur.execute(add_user, data_user)
        db.commit()

        cur.execute(
            "SELECT * FROM user WHERE username = %s;",
            (username,)
        )
        
        user = cur.fetchone()
        
        session.clear()
        cur.close()
        session["user_id"] = user[0]
        
        return redirect("/")

    except IntegrityError:
        return "Username or email is already in used!"


@bp.route("/login", methods=["POST"])
def login():
    username = request.form['username']
    password = request.form['password']
    
    db = get_db()
    cur = db.cursor()
    
    cur.execute(
        "SELECT * FROM user WHERE username = %s",
        (username,)
    )
    user = cur.fetchone()
    
    if user is None:
        return "Incorrect username"
    elif not bcrypt.checkpw(password.encode("utf-8"), user[3].encode("utf-8")):
        return "Incorrect password"
    
    session.clear()
    session['user_id'] = user[0]
    return redirect("/")

@bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@bp.route("/forget", methods=["POST"])
def forget():
    pass


@bp.route("/forget/<string:token>/", methods=["POST", "GET"])
def new_pass(token: str):
    print("HI")
    if request.method == "POST":
        pass
    else:
        return render_template("starter/reset.html")
    
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        db = get_db()
        cur = db.cursor()   
        cur.execute(
            "SELECT * FROM user WHERE id = %s",
            (user_id,)
        )
        g.user = cur.fetchone()