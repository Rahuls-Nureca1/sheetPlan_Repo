from flask import Flask


def initialize_extensions(app):
    from extensions import db, ma, migrate, cors,seeder

    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)
    seeder.init_app(app,db)


def register_blueprints(app):
    from api_v1.api_v1_app import api_v1_bp
    from api_v1.nin_ingredient import nin_ingredient_bp
    from default.default_app import default_bp
    from api_v1.plan_management import plan_management_bp
    from api_v1.recipe_management import recipe_management_bp
    from api_v1.user_management import user_management_bp

    app.register_blueprint(api_v1_bp, url_prefix='/api/v1')
    app.register_blueprint(default_bp, url_prefix='/api')
    app.register_blueprint(nin_ingredient_bp, url_prefix='/api/v1/nin')
    app.register_blueprint(recipe_management_bp, url_prefix='/api/v1/recipe_management')
    app.register_blueprint(plan_management_bp, url_prefix='/api/v1/plan_management')
    app.register_blueprint(user_management_bp, url_prefix='/api/v1/user_management')



def create_app(config_object):
    app = Flask(__name__.split(".")[0], instance_relative_config=True)
    app.config.from_object(config_object)
    initialize_extensions(app)
    register_blueprints(app)
    return app
