from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_caching import Cache

db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()
cache = Cache()