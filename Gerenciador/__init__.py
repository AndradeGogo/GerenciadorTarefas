from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config['SECRET_KEY'] = '21d66295c19bfd59cdae4d95c951098ce5dd2acbe19de3544a6556828f51bf10'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Gerenciador.db'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'homepage'

from Gerenciador import routes, models
