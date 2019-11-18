from __future__ import print_function
import datetime, re
import googleapiclient.discovery
from show_and_tell.google_tools.google_service import build_credentials

import flask

bp = flask.Blueprint('google_calendar', __name__)
AUTHORIZATION_SCOPE = 'https://www.googleapis.com/auth/calendar'
API_NAME = 'calendar'


def build_drive_api_v3():
    credentials = build_credentials(AUTHORIZATION_SCOPE)
    return googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)


@bp.route('/gcal/view/<num_entries>', methods=['GET'])
def view_upcoming_entries(num_entries=10):
    cal_api = build_drive_api_v3()

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    events_result = cal_api.events().list(calendarId='voma@almende.org', timeMin=now,
                                            maxResults=num_entries, singleEvents=True,
                                            orderBy='startTime', q="Almende show-and-tell").execute()
    events = events_result.get('items', [])

    to_return = []

    for event in events:
        ret_env = {
            "start": event["start"],
            "end": event["end"],
        }

        try:
            ret_env["presenter"], ret_env["topic"] = re.match("[\n.]*Presenter: (.*)\n+Topic: (.*)",
                                                              event["description"]).groups()
        except AttributeError as e:
            ret_env["presenter"], ret_env["topic"] = "ERROR", "ERROR"

        to_return.append(ret_env)

    return flask.jsonify(to_return)
