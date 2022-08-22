from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS


cors = CORS()
db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate(compare_type=True)
ma = Marshmallow()
login_manager = LoginManager()
