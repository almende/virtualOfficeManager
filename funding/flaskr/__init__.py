from flask import Flask, jsonify
from werkzeug.middleware.proxy_fix import ProxyFix
import os
from flask_cors import CORS
# from logging.config import dictConfig
#
# dictConfig({
#     'version': 1,
#     'formatters': {'default': {
#         'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
#     }},
#     'handlers': {'wsgi': {
#         'class': 'logging.StreamHandler',
#         'stream': 'ext://flask.logging.wsgi_errors_stream',
#         'formatter': 'default'
#     }},
#     'root': {
#         'level': 'DEBUG',
#         'handlers': ['wsgi']
#     }
# })


def handle_error(error):
    return jsonify({'message': error.description}), error.code


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.wsgi_app = ProxyFix(app.wsgi_app)
    cors = CORS(app)

    app.config.from_mapping(
        MONGO_URI=os.environ.get('DB'),
        MONGO_DB='funding'
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # register error handler
    app.register_error_handler(404, handle_error)
    app.register_error_handler(400, handle_error)

    # setup database
    from . import db

    with app.app_context():
        app.db = db.get_db()

    # import api's
    from .controller.apiv1 import blueprint as api1
    app.register_blueprint(api1)

    return app