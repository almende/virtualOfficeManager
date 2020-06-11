from __future__ import print_function
import googleapiclient.discovery
from .google_service import build_credentials

from flask_restx import Namespace

import flask

api = Namespace('contacts', description='Contact related operations')
bp = flask.Blueprint('google_contacts', __name__)
AUTHORIZATION_SCOPE = 'https://www.googleapis.com/auth/user.organization.read'


def build_contacts_api_v3():
    credentials = build_credentials(AUTHORIZATION_SCOPE)
    return googleapiclient.discovery.build('people', 'v1', credentials=credentials)


@bp.route('/gcontacts/view/<query>', methods=['GET'])
def view_contact_list(query=''):
    people_service = build_contacts_api_v3()

    connections = people_service.people().connections() \
        .list(resourceName='people/me', personFields="names,emailAddresses,coverPhotos")

    return flask.jsonify([] if connections.body is None else connections.body)

