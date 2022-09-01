from lib2to3.pytree import Base
from app import create_app
from decouple import config as dotconfig
from config import ProdConfig, DevConfig

environment = dotconfig("ENVIRONMENT")
if environment == 'Production':
    app = create_app(ProdConfig)
elif environment == 'Development':
    app = create_app(DevConfig)


if __name__ == "__main__":
    app.run(host='0.0.0.0')