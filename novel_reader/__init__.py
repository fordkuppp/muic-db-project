from flask import Flask, render_template

def create_app():
    app = Flask(__name__)   
    app.config['SECRET_KEY'] = 'secret key ;)'    
    
    from . import db, user, home
    db.init_app(app)
    app.register_blueprint(user.bp)
    app.register_blueprint(home.bp)
    
    return app