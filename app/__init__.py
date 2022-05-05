from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


# Initializing 
app = Flask(__name__)
app.config.from_object(Config)

#register Plug-ins
login=LoginManager(app)

#init my Database manager
db = SQLAlchemy(app) #making an instance of the class, it's asking for the app
migrate = Migrate(app, db)  #this helps SQL make changes on the internet face

#Configure Some Settings
login.login_view= 'login' #sends ppl to the login, the name of the function to call
login.login_message= 'Log yourself in you filthy animal' #goes into flash message
login.login_message_category='warning'


from app import routes, models