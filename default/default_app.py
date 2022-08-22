from flask import Blueprint

default_bp = Blueprint('default', __name__)


# TODO:
# Implement Server health check
@default_bp.route('/health-check', methods=['GET'])
def health_check():
    return {"health check":"success"}
