from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = "2fa676bf6a19fcec3fe90e6a"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pagamentos.db'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'signin_login'
login_manager.login_message_category = 'alert-info'

from pagamentos import routes