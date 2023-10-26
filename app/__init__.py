from flask import Flask
from gqlalchemy import Memgraph
from config import Config
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config.from_object(Config)
db= Memgraph("127.0.0.1", 7687)

from app import routes