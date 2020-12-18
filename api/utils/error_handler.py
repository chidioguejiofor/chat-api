import werkzeug
import logging


def error_handlers(app):

    @app.errorhandler(werkzeug.exceptions.NotFound)
    def handle_resource_not_found(error):
        return {'status': 'error', 'message': 'Resource was not found'}, 404

    @app.errorhandler(Exception)
    def handle_any_other_errors(error):
        logging.exception(error)
        return {
            'status': 'error',
            'message': 'Strange Error occurred. Contact Support'
        }, 500
