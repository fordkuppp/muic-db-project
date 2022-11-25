from flask import current_app, g
import mysql.connector
import yaml
import click

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def get_db():
    if "db" not in g:
        cred = yaml.load(open('cred.yaml'), Loader=yaml.Loader)    
        g.db = mysql.connector.connect(
            host=cred["mysql_host"],
            user=cred["mysql_user"],
            password=cred["mysql_password"],
            database=cred["mysql_db"]
        )
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
        
def init_db():
    with current_app.open_resource('schema.sql') as f:
        with get_db().cursor() as cur:
            cur.execute(f.read().decode('utf8'))
        cur.commit()

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')