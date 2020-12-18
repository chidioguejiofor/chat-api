"""API Initialization Module"""
from flask import Flask, jsonify, Blueprint

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import dotenv
from api.utils.error_handler import error_handlers
from .configs import ENV_MAPPER

db = SQLAlchemy()
dotenv.load_dotenv()
api_blueprint = Blueprint('api_bp', __name__, url_prefix='/api')
endpoint = api_blueprint.route


def register_blueprints(application):
    """Registers all blueprints
    
    Args:
        application (Obj): Flask Instance

    Returns:
        None
    """

    application.register_blueprint(api_blueprint)


def create_app(current_env='development'):
    """Creates the flask application instance

    Args:
        current_env (string): The current environment

    Returns:
        (Object, socketIO): Flask instance
    """

    app = Flask(__name__)

    if current_env == 'development':
        import logging
        logging.basicConfig()
        logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    app.config.from_object(ENV_MAPPER[current_env])
    db.init_app(app)
    migrate = Migrate(app, db)
    import api.features 

    register_blueprints(app)
    error_handlers(app)

    @app.route('/', methods=['GET'])
    def health():
        """Index Route"""

        return jsonify(data={
            "status": 'success',
            "message": 'API service is healthy, Goto to /api/'
        }, )

    return app
