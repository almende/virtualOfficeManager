from __future__ import print_function
import datetime, re
import googleapiclient.discovery
from .google_service import build_credentials
from google.oauth2 import id_token
from google.auth.transport import requests

import flask

bp = flask.Blueprint('google_calendar', __name__)
AUTHORIZATION_SCOPE = 'https://www.googleapis.com/auth/calendar'
API_NAME = 'calendar'
CALENDAR_ID = 'almende.org_1g76kkh3ukueooq7fr4dd3m5p8@group.calendar.google.com'
RE_MATCH_STRING = "[\n.]*Presenter: (.*)\n+Topic: (.*)"
RE_SUB_MATCH_STRING = "([\n.]*Presenter: ).*(\n+Topic: ).*"
RE_SUB_REPLACE_STRING = r"\1{}\2{}"


def build_drive_api_v3():
    credentials = build_credentials(AUTHORIZATION_SCOPE)
    return googleapiclient.discovery.build('calendar', 'v3', credentials=credentials, cache_discovery=False)


def check_token():
    # Get token and verify it
    token = flask.request.headers.get('Authorization').split(' ')[1]
    idinfo = id_token.verify_oauth2_token(token, requests.Request())

    if idinfo['aud'] not in flask.current_app.config['GOOGLE_TOKEN_ACCEPTED_CLIENTIDS']:
        raise ValueError('Could not verify audience.')
    if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
        raise ValueError('Wrong issuer.')
    if idinfo['hd'] not in flask.current_app.config['GOOGLE_TOKEN_ACCEPTED_DOMAINS']:
        raise ValueError('Wrong hosted domain.')


@bp.route('/gcal/event', methods=['PATCH'])
def update_event():
    check_token()

    cal_api = build_drive_api_v3()

    payload = {}

    if "presenter" in flask.request.get_json() or "topic" in flask.request.get_json():
        getresp = cal_api.events().get(calendarId=CALENDAR_ID, eventId=flask.request.get_json()["id"]).execute()
        description = getresp["description"]

        p, t = re.match(RE_MATCH_STRING,description).groups()
        if "presenter" in flask.request.get_json():
            p = flask.request.get_json()["presenter"]
        if "topic" in flask.request.get_json():
            t = flask.request.get_json()["topic"]

        description = re.sub(RE_SUB_MATCH_STRING,
                             RE_SUB_REPLACE_STRING.format('TBD' if p is None else p, t), description)

        payload["description"] = description

    response = cal_api.events().patch(calendarId=CALENDAR_ID, eventId=flask.request.get_json()["id"],
                                      body=payload).execute()

    return flask.jsonify(response)


@bp.route('/gcal/view/<num_entries>', methods=['GET'])
def view_upcoming_entries(num_entries=10):
    check_token()

    cal_api = build_drive_api_v3()

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    events_result = cal_api.events().list(calendarId=CALENDAR_ID, timeMin=now,
                                          maxResults=num_entries, singleEvents=True,
                                          orderBy='startTime', q="Almende show-and-tell").execute()
    events = events_result.get('items', [])

    for event in events:
        try:
            event["presenter"], event["topic"] = re.match(RE_MATCH_STRING,
                                                          event["description"]).groups()
        except AttributeError as e:
            event["presenter"], event["topic"] = "ERROR", "ERROR"

    return flask.jsonify(events)
