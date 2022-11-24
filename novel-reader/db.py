from flask import current_app, g
import mysql.connector
import yaml

cred = yaml.load(open('cred.yaml'), Loader=yaml.Loader)    

def get_db():
    # if "db" not in g:
    db = mysql.connector.connect(
        host=cred["mysql_host"],
        user=cred["mysql_user"],
        password=cred["mysql_password"],
        database=cred["mysql_db"]
    )
    return db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
    
db = get_db()
statement = f"INSERT INTO reader_db.user (username, email, password, last_login, role_id) VALUES ('asfe', 'test', 'test', '2022-11-24 21:52:50', 2);"
# statement = f"SELECT * FROM user"
                
cur = db.cursor()
cur.execute(statement)
print(str(cur.fetchall()))
db.commit()