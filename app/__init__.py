from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
# from flask_moment import Moment

# Init Plug-ins
login = LoginManager()
#init my Database manager
db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):

    # Init the app
    app = Flask(__name__)
    #Link in the Config
    app.config.from_object(config_class)

    #Register Plug-in
    login.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    
    #Configure Some Settings
    login.login_view = 'auth.login'
    login.login_message = 'Login to play!!'
    login.login_message_category='warning'

    from .blueprints.main import bp as main_bp
    app.register_blueprint(main_bp)

    from .blueprints.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    # from .blueprints.social import bp as social_bp
    # app.register_blueprint(social_bp)

    # from .blueprints.api import bp as api_bp
    # app.register_blueprint(api_bp)

    return app