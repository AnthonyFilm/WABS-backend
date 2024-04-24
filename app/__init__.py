from datetime import timedelta
from flask import Flask
# from flask_session import Session
from config import Config
# from .site.routes import site
from .authentication.routes import auth
# from .api.routes import api
# from .dreamapi.routes import dreamobjects

# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from models import db as root_db, login_manager, ma
from flask_cors import CORS
import json
# from helpers import JSONEncoder

# session = Session()

app = Flask(__name__)
# , origins=["http://localhost:5173"]
CORS(app, supports_credentials=True)
# app.config["SESSION_COOKIE_SAMESITE"] = "None"
# app.config["SESSION_COOKIE_SECURE"] = True
# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

# app.register_blueprint(site)
app.register_blueprint(auth)
# app.register_blueprint(api)
# app.register_blueprint(dreamobjects)

# app.json_encoder = JSONEncoder
app.config.from_object(Config)
# root_db.init_app(app)
# login_manager.init_app(app)
# session.init_app(app)
# ma.init_app(app)
# migrate = Migrate(app, root_db)

