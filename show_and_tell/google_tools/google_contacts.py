from __future__ import print_function
import datetime, re
import googleapiclient.discovery
from show_and_tell.google_tools.google_service import build_credentials

import flask

bp = flask.Blueprint('google_contacts', __name__)
AUTHORIZATION_SCOPE = 'https://www.googleapis.com/auth/user.organization.read'


def build_contacts_api_v3():
    credentials = build_credentials(AUTHORIZATION_SCOPE)
    return googleapiclient.discovery.build('people', 'v1', credentials=credentials)


@bp.route('/gcontacts/view/<query>', methods=['GET'])
def view_contact_list(query=''):
    people_service = build_contacts_api_v3()

    connections = people_service.people().connections()\
        .list(resourceName='people/me', personFields="names,emailAddresses,coverPhotos")


    return flask.jsonify(connections)
