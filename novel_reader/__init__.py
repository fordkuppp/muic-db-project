from flask import Flask, render_template

def create_app():
    app = Flask(__name__)   
    app.config['SECRET_KEY'] = 'secret key ;)'    
    
    from . import db, user, home, admin, novel
    db.init_app(app)
    app.register_blueprint(user.bp)
    app.register_blueprint(home.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(novel.bp)
    
    return app