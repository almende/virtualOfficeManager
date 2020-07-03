import os

import flask
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

from .google_tools import google_calendar, google_drive, google_contacts
from .controller.apiv1 import blueprint as api1


def create_app(test_config=None):
    # create and configure the app
    app = flask.Flask(__name__, instance_relative_config=True)
    app.wsgi_app = ProxyFix(app.wsgi_app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py')
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    CORS(app, resources={
        r"/gcal/event": {"origins": "*"},
        r"/gcal/view/*": {"origins": "*"},
        r"/gcontacts/view/*": {"origins": "*"}
    })
    app.secret_key = os.environ.get("FN_FLASK_SECRET_KEY", default=False)

    # app.register_blueprint(google_auth.bp)
    # app.register_blueprint(google_drive.bp)
    app.register_blueprint(google_calendar.bp)
    # app.register_blueprint(google_contacts.bp)

    # app.register_blueprint(api1)


    return app
