import os
from oauth2client.service_account import ServiceAccountCredentials
from flask import current_app


def build_credentials(scopes):
    return ServiceAccountCredentials.from_json_keyfile_name(
        current_app.config["FN_SERVICE_JSON_FILE"], scopes=scopes)
