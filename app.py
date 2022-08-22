from flask import Flask

def initialize_extensions(app):
    from extensions import db, ma, migrate, cors

    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)

def register_blueprints(app):
    from api_v1.api_v1_app import api_v1_bp
    from default.default_app import default_bp
    app.register_blueprint(api_v1_bp, url_prefix='/api/v1')
    app.register_blueprint(default_bp, url_prefix='/api')



def create_app(config_object):
    app = Flask(__name__.split(".")[0], instance_relative_config=True)
    app.config.from_object(config_object)
    initialize_extensions(app)
    register_blueprints(app)
    return app
