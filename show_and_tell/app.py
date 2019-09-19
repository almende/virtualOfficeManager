import os

import flask

from google_tools import google_drive, google_auth, google_calendar

app = flask.Flask(__name__)
app.secret_key = os.environ.get("FN_FLASK_SECRET_KEY", default=False)

app.register_blueprint(google_auth.bp)
app.register_blueprint(google_drive.bp)
app.register_blueprint(google_calendar.bp)


@app.route('/')
def index():
    if google_auth.is_logged_in():
        drive_fields = "files(id,name,mimeType,createdTime,modifiedTime,shared,webContentLink)"
        items = google_drive.build_drive_api_v3().list(
                        pageSize=20, orderBy="folder", q='trashed=false',
                        fields=drive_fields
                    ).execute()

        return flask.render_template('list.html', files=items['files'], user_info=google_auth.get_user_info())

    return 'You are not currently logged in.'
