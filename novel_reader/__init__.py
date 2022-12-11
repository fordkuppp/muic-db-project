from flask import Flask
from novel_reader.tags import humantime
from . import db, user, home, admin, novel


app = Flask(__name__)
app.config["SECRET_KEY"] = "secret key ;)"


db.init_app(app)
app.register_blueprint(user.bp)
app.register_blueprint(home.bp)
app.register_blueprint(admin.bp)
app.register_blueprint(novel.bp)
app.jinja_env.globals["humantime"] = humantime


if __name__ == "__main__":
    app.run()
