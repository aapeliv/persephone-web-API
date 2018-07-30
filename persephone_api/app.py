import connexion
from connexion.resolver import RestyResolver

from . import api_endpoints

from .settings import ProdConfig


def create_app(config_object=ProdConfig):
    """An application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.
    :param config_object: The configuration object to use.
    """
    # Create the API endpoints from YAML specification
    connexion_app = connexion.FlaskApp(__name__, specification_dir='.')
    register_swagger_api(connexion_app)

    # fetch underlying flask app from the connexion app
    app = connexion_app.app
    app.config.from_object(config_object)
    return app

def register_swagger_api(connexion_flask_app):
    """Take a connexion FlaskApp and register swagger API"""
    connexion_flask_app.add_api('api_spec.yaml', resolver=RestyResolver('persephone_api.api_endpoints'))