from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS
from flask_seeder import FlaskSeeder


cors = CORS()
db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate(compare_type=True)
ma = Marshmallow()
login_manager = LoginManager()
seeder = FlaskSeeder()
