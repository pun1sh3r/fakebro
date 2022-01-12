from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap



db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()



def create_app():
    app = Flask(__name__)
    bootstrap = Bootstrap(app)
    app.secret_key = 'secretkeyhardcoded'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    migrate.init_app(app,db)
    login_manager.init_app(app)
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app