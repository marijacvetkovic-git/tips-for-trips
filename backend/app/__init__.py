from flask import Flask
from gqlalchemy import Memgraph
from config import Config
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager


app = Flask(__name__)
ma = Marshmallow(app)

bcrypt = Bcrypt(app)
login_menager=LoginManager(app)

app.config.from_object(Config)
# jwtM=JWTManager(app)
db= Memgraph("127.0.0.1", 7687)

from app import routes