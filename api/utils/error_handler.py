import werkzeug
import logging
from marshmallow import ValidationError

from api.utils.messages.errors import INVALID_INPUT


def error_handlers(app):
    @app.errorhandler(ValidationError)
    def handle_errors(error):
        if '_schema' in error.messages:
            error.messages = error.messages['_schema']
        return {
                   'errors': error.messages,
                   'message': INVALID_INPUT
               }, 400

    @app.errorhandler(werkzeug.exceptions.NotFound)
    def handle_resource_not_found(error):
        return {'status': 'error', 'message': 'Resource was not found'}, 404

    @app.errorhandler(werkzeug.exceptions.MethodNotAllowed)
    def handle_resource_not_found(error):
        return {'status': 'error', 'message': 'That method is not allowed'}, 405

    @app.errorhandler(Exception)
    def handle_any_other_errors(error):
        logging.exception(error)
        return {
            'status': 'error',
            'message': 'Strange Error occurred. Contact Support'
        }, 500
